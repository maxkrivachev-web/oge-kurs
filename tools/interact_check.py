import asyncio, sys, json
sys.path.insert(0,__import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from golos_route import install
from playwright.async_api import async_playwright
FILE=__import__('os').path.abspath(sys.argv[1] if len(sys.argv)>1 else 'index.html')
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/usr/bin/google-chrome",args=["--no-sandbox"])
        ctx=await b.new_context(viewport={"width":390,"height":844}, has_touch=True)
        pg=await ctx.new_page(); await install(pg)
        errs=[]; pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto("file://"+FILE+"#m1"); await pg.wait_for_timeout(400)
        out={}
        out['where']=await pg.evaluate("document.getElementById('where').textContent")
        # menu open
        await pg.click('#menuBtn'); await pg.wait_for_timeout(350)
        out['menu_open']=await pg.evaluate("document.body.classList.contains('nav') && getComputedStyle(document.getElementById('side')).visibility")
        # back button closes
        await pg.go_back(); await pg.wait_for_timeout(350)
        out['menu_after_back']=await pg.evaluate("document.body.classList.contains('nav')")
        out['hash_after_back']=await pg.evaluate("location.hash")
        # open and pick m5
        await pg.click('#menuBtn'); await pg.wait_for_timeout(300)
        await pg.click('.side a[href="#m5"]'); await pg.wait_for_timeout(600)
        out['after_pick']=await pg.evaluate("[location.hash, document.body.classList.contains('nav'), document.querySelector('.page.on').id]")
        # back should go to m1 (not stuck)
        await pg.go_back(); await pg.wait_for_timeout(400)
        out['back_after_pick']=await pg.evaluate("[location.hash, document.querySelector('.page.on').id]")
        # tap outside closes
        await pg.click('#menuBtn'); await pg.wait_for_timeout(300)
        await pg.mouse.click(370,500); await pg.wait_for_timeout(400)
        out['scrim_close']=await pg.evaluate("document.body.classList.contains('nav')")
        # quiz verdict
        await pg.evaluate("location.hash='m1'"); await pg.wait_for_timeout(300)
        mc=await pg.query_selector('#m1 .mc')
        await mc.scroll_into_view_if_needed()
        lis=await mc.query_selector_all('ol li'); await lis[0].click(); await pg.wait_for_timeout(400)
        out['quiz']=await mc.evaluate("q=>[q.querySelector('.verdict').textContent, q.querySelector('details').open, !!q.querySelector('li .ic')]")
        # details animation keeps summary in place
        d=await pg.query_selector('#m1 details:not([open])')
        s=await d.query_selector('summary'); await s.scroll_into_view_if_needed(); await pg.wait_for_timeout(200)
        y0=await s.evaluate("e=>e.getBoundingClientRect().top")
        await s.click(); await pg.wait_for_timeout(120)
        mid=await d.evaluate("d=>d.querySelector('.dbody').getBoundingClientRect().height")
        await pg.wait_for_timeout(300)
        y1=await s.evaluate("e=>e.getBoundingClientRect().top")
        out['details']=dict(open=await d.evaluate("d=>d.open"), mid_height=mid, y0=y0, y1=y1)
        await s.click(); await pg.wait_for_timeout(400)
        out['details_closed']=await d.evaluate("d=>d.open")
        # to top button
        await pg.evaluate("window.scrollTo(0,1500)"); await pg.wait_for_timeout(200)
        out['toTop_visible']=await pg.evaluate("getComputedStyle(document.getElementById('toTop')).display")
        # continue button on start
        await pg.evaluate("location.hash='m5-3'"); await pg.wait_for_timeout(700)
        await pg.evaluate("location.hash='start'"); await pg.wait_for_timeout(300)
        out['cont']=await pg.evaluate("document.getElementById('cont').innerText")
        out['navpn_m5']=await pg.evaluate("(location.hash='m5', [...document.querySelectorAll('#m5 .navpn a')].map(a=>a.innerText.replace(/\\n/g,' ')))")
        out['expand_all']=await pg.evaluate("!!document.querySelector('#m5 .dtools button')")
        # trainer
        await pg.evaluate("location.hash='lines'"); await pg.wait_for_timeout(300)
        await pg.evaluate("document.querySelector('#lines a.trlink[data-line=\"4\"]').click()"); await pg.wait_for_timeout(500)
        out['tr_link']=await pg.evaluate("[location.hash, document.querySelector('#trF .fchip[aria-pressed=true]').dataset.l, document.querySelectorAll('#trList .trc').length]")
        c=await pg.query_selector('#trList .trc'); li=await c.query_selector('ol li:nth-child(2)'); await li.click(); await pg.wait_for_timeout(200)
        out['tr_choice']=await c.evaluate("c=>[c.querySelector('.verdict').textContent.trim().slice(0,30), !!c.querySelector('li.ok .ic')]")
        await pg.click('#trF .fchip[data-l="14"]'); await pg.wait_for_timeout(200)
        out['tr_match']=await pg.evaluate("""(()=>{const c=document.querySelector('#trList .trc');const i=c.querySelector('input');i.value='11111';c.querySelector('.chk').click();return c.querySelector('.fb').innerText.split('\\n').slice(0,2)})()""")
        await pg.click('#trF .fchip[data-l="17"]'); await pg.wait_for_timeout(200)
        out['tr_ext']=await pg.evaluate("""(()=>{const c=document.querySelector('#trList .trc');c.querySelector('textarea').value='черновик';c.querySelector('.show').click();c.querySelector('.grade button[data-g="1"]').click();return [!c.querySelector('.out').hidden, c.querySelectorAll('.grade button').length]})()""")
        await pg.click('#trM button[data-m="bad"]'); await pg.wait_for_timeout(200)
        out['tr_bad']=await pg.evaluate("[document.querySelectorAll('#trList .trc').length, document.getElementById('trEmpty').hidden]")
        await pg.reload(); await pg.wait_for_timeout(500)
        out['tr_store']=await pg.evaluate("Object.keys(JSON.parse(localStorage.getItem('oge27-trainer-v1')||'{}')).length")
        await pg.evaluate("location.hash='trainer'"); await pg.wait_for_timeout(300)
        await pg.click('#trM button[data-m="bad"]'); await pg.wait_for_timeout(200)
        out['tr_bad_all']=await pg.evaluate("document.querySelectorAll('#trList .trc').length")
        out['errors']=errs
        print(json.dumps(out,ensure_ascii=False,indent=1))
        await b.close()
asyncio.run(main())
