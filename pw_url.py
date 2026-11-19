import os
from playwright.sync_api import sync_playwright
UA='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
reqs=[]
with sync_playwright() as p:
    b=p.chromium.launch(headless=False, args=['--disable-blink-features=AutomationControlled','--no-sandbox','--disable-dev-shm-usage'])
    ctx=b.new_context(user_agent=UA, viewport={'width':1366,'height':768}, locale='zh-CN', timezone_id='Asia/Shanghai')
    ctx.add_init_script("Object.defineProperty(navigator,'webdriver',{get:()=>undefined});window.chrome={runtime:{}};")
    page=ctx.new_page()
    page.on("request", lambda r: reqs.append((r.method,r.url,(r.post_data or '')[:120])))
    for path in ["/pay/1","/pay/99999999","/product-file/curve","/checkout/1","/acceptance/1"]:
        reqs.clear()
        try:
            r=page.goto("https://m.lbtek.com"+path, wait_until="domcontentloaded", timeout=45000)
            for i in range(6):
                page.wait_for_timeout(1500)
                c=page.content()
                if 'arg1=' not in c and 'renderData' not in c: break
            if 'arg1=' in page.content() or 'renderData' in page.content():
                print("%-24s => CHALLENGE(未过)"%path, flush=True); continue
            txt=page.evaluate("()=>document.body?document.body.innerText.slice(0,300):''")
            print("%-24s => status=%s title=%s len=%d"%(path, r.status if r else '?', page.title(), len(page.content())), flush=True)
            print("   TEXT: %s"%txt.replace("\n"," | ")[:280], flush=True)
            api=[u for m,u,pd in reqs if '/api/' in u]
            for u in api[:8]: print("   API: %s"%u[:150], flush=True)
        except Exception as e:
            print("%-24s => ERR %s"%(path,str(e)[:150]), flush=True)
    b.close()
