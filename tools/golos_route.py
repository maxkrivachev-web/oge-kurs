import base64, glob, os
FD="/home/claude/fonttmp/package/files"
def font_css():
    css=[]
    for w in (400,500,600,700,800):
        for sub,rng in (("cyrillic","U+0301,U+0400-045F,U+0490-0491,U+04B0-04B1,U+2116"),("latin","U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD")):
            f=f"{FD}/golos-text-{sub}-{w}-normal.woff2"
            if not os.path.exists(f): continue
            b=base64.b64encode(open(f,'rb').read()).decode()
            css.append(f"@font-face{{font-family:'Golos Text';font-style:normal;font-weight:{w};font-display:block;src:url(data:font/woff2;base64,{b}) format('woff2');unicode-range:{rng}}}")
    return "\n".join(css)
CSS=font_css()
async def install(page):
    async def handler(route):
        await route.fulfill(status=200, content_type="text/css", body=CSS)
    await page.route("**/fonts.googleapis.com/**", handler)
    await page.route("**/fonts.gstatic.com/**", lambda r: r.abort())
