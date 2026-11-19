import asyncio, sys
sys.path.insert(0,__import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from golos_route import install
from playwright.async_api import async_playwright
TEXT=("Социализация - процесс усвоения человеком знаний, норм и ценностей общества, который продолжается всю жизнь. "
"Первичная социализация проходит в семье и среди сверстников, вторичная - в школе, на работе, в армии. "
"Государство обеспечивает поддержание правопорядка, оказание населению медицинских и образовательных услуг, "
"а также регулирует экономику с помощью налогов, бюджета и законов. Несовершеннолетние с четырнадцати лет "
"вправе самостоятельно распоряжаться своим заработком, стипендией и иными доходами, вносить вклады в банки.")*3
HTML="""<!doctype html><html><head><link href="https://fonts.googleapis.com/css2?family=Golos+Text:wght@400;700&display=swap" rel="stylesheet">
<style>body{margin:0;font-family:'Golos Text';} p{font-size:%dpx;line-height:1.65;width:%s;margin:0}</style></head><body><p id=p>%s</p></body></html>"""
JS="""()=>{const p=document.getElementById('p');const t=p.firstChild;const r=document.createRange();let lines={};
for(let i=0;i<t.length;i++){r.setStart(t,i);r.setEnd(t,i+1);const b=r.getBoundingClientRect();const y=Math.round(b.top);lines[y]=(lines[y]||0)+1;}
const v=Object.values(lines);v.pop();return [v.length, Math.round(v.reduce((a,b)=>a+b,0)/v.length), Math.min(...v), Math.max(...v), document.fonts.check('18px "Golos Text"')];}"""
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/usr/bin/google-chrome",args=["--no-sandbox"])
        pg=await b.new_page()
        await install(pg)
        for fs,w in [(18,'600px'),(18,'640px'),(18,'660px'),(18,'680px'),(18,'720px'),(17,'358px'),(18,'358px'),(17,'343px')]:
            await pg.set_content(HTML%(fs,w,TEXT)); await pg.wait_for_timeout(300)
            print(fs,w,await pg.evaluate(JS))
        await b.close()
asyncio.run(main())
