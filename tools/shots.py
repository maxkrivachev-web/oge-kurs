import asyncio, sys
sys.path.insert(0,__import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from golos_route import install
from playwright.async_api import async_playwright
OUT=sys.argv[1]; FILE=sys.argv[2] if len(sys.argv)>2 else '/home/claude/oge-kurs/index.html'
PAGES=[('start',''),('m0',''),('m5',''),('m10',''),('glossary',''),('progress','')]
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/usr/bin/google-chrome",args=["--no-sandbox"])
        for w,h in [(390,844),(1440,900)]:
            pg=await b.new_page(viewport={"width":w,"height":h})
            await install(pg)
            await pg.goto("file://"+FILE)
            await pg.wait_for_timeout(500)
            for pid,_ in PAGES:
                await pg.evaluate(f"location.hash='{pid}'"); await pg.wait_for_timeout(250)
                await pg.screenshot(path=f"{OUT}/{pid}_{w}.png")
            # one scrolled shot in m5 to show plaques
            await pg.evaluate("location.hash='m5'"); await pg.wait_for_timeout(200)
            await pg.evaluate("window.scrollTo(0, document.querySelector('#m5 .c')?.getBoundingClientRect().top + scrollY - 120)"); await pg.wait_for_timeout(200)
            await pg.screenshot(path=f"{OUT}/m5plaques_{w}.png")
            await pg.close()
        await b.close()
asyncio.run(main())
