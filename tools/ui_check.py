import asyncio, sys, json
sys.path.insert(0,__import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from golos_route import install
from playwright.async_api import async_playwright
FILE=__import__('os').path.abspath(sys.argv[1] if len(sys.argv)>1 else 'index.html')
WIDTHS=[360,390,720,768,1024,1440]
OVER_JS="""()=>{
 const vw=document.documentElement.clientWidth; const res=[];
 if(document.documentElement.scrollWidth>vw+1) res.push('DOC scrollWidth '+document.documentElement.scrollWidth+' > '+vw);
 const pg=document.querySelector('.page.on');
 for(const el of pg.querySelectorAll('*')){
   if(el.closest('.scroll')&&!el.classList.contains('scroll')) continue;
   if(el.closest('svg')&&el.tagName.toLowerCase()!=='svg') continue;
   const r=el.getBoundingClientRect(); if(!r.width) continue;
   if(r.right>vw+1||r.left<-1){ res.push(el.tagName+'.'+(el.className&&el.className.baseVal===undefined?el.className:'')+' L'+Math.round(r.left)+' R'+Math.round(r.right)+' :'+(el.textContent||'').trim().slice(0,40)); }
   if(res.length>8) break;
 }
 // text clipped inside fixed-height boxes
 for(const el of pg.querySelectorAll('.cell,.chip,.btn,.fchip,.navpn a,.toc a')){ if(el.scrollWidth>el.clientWidth+2) res.push('CLIP '+el.className+': '+el.textContent.trim().slice(0,30)); if(res.length>14)break;}
 return res;}"""
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/usr/bin/google-chrome",args=["--no-sandbox"])
        report={}
        for w in WIDTHS:
            pg=await b.new_page(viewport={"width":w,"height":800})
            await install(pg)
            errs=[]; pg.on("pageerror", lambda e: errs.append(str(e)))
            await pg.goto("file://"+FILE); await pg.wait_for_timeout(400)
            ids=await pg.evaluate("[...document.querySelectorAll('section.page')].map(s=>s.id)")
            for pid in ids:
                await pg.evaluate(f"location.hash='{pid}'"); await pg.wait_for_timeout(120)
                await pg.evaluate("document.querySelectorAll('.page.on details').forEach(d=>d.open=true)")
                await pg.wait_for_timeout(60)
                r=await pg.evaluate(OVER_JS)
                if r: report[f"{w}/{pid}"]=r
            # anchor under sticky header
            await pg.evaluate("location.hash='m5-3'"); await pg.wait_for_timeout(200)
            t=await pg.evaluate("[document.getElementById('m5-3').getBoundingClientRect().top, document.querySelector('.top').getBoundingClientRect().bottom]")
            if t[0] < t[1]: report[f"{w}/anchor"]=f"h2 top {t[0]} under header {t[1]}"
            if errs: report[f"{w}/errors"]=errs[:3]
            await pg.close()
        print(json.dumps(report,ensure_ascii=False,indent=1) if report else "OK: no overflow, no errors")
        await b.close()
asyncio.run(main())
