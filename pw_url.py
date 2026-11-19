import os
from playwright.sync_api import sync_playwright
IP="120.24.242.147"
UA='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
reqs=[]
with sync_playwright() as p:
    b=p.chromium.launch(headless=False, args=['--disable-blink-features=AutomationControlled','--no-sandbox','--disable-dev-shm-usage','--ignore-certificate-errors','--host-resolver-rules=MAP m.lbtek.com 120.24.242.147'])
    ctx=b.new_context(user_agent=UA, viewport={'width':1366,'height':768}, locale='zh-CN', ignore_https_errors=True)
    ctx.add_init_script("Object.defineProperty(navigator,'webdriver',{get:()=>undefined});window.chrome={runtime:{}};")
    page=ctx.new_page()
    page.on("request", lambda r: reqs.append((r.method, r.url, (r.post_data or "")[:200])))
    try:
        page.goto("https://m.lbtek.com/", wait_until="domcontentloaded", timeout=45000)
        page.wait_for_timeout(6000)
        print("URL:", page.url, "title:", page.title(), flush=True)
        html=page.content()
        print("len:", len(html), flush=True)
        import re
        # 表单字段
        for m in re.finditer(r'<input[^>]*>', html):
            print("  INPUT:", m.group(0)[:160], flush=True)
        print("--- form ---", flush=True)
        for m in re.finditer(r'<form[^>]*>', html): print("  ", m.group(0)[:160], flush=True)
        # 尝试登录
        try:
            page.fill('input[type=text], input[name*=user], input[placeholder*="用户名"]', "admin", timeout=5000)
            page.fill('input[type=password]', "Zz9137Probe", timeout=5000)
            page.wait_for_timeout(800)
            page.keyboard.press("Enter")
            page.wait_for_timeout(5000)
            print("after-submit URL:", page.url, flush=True)
        except Exception as e:
            print("fill/enter err:", str(e)[:200], flush=True)
    except Exception as e:
        print("FATAL", str(e)[:300], flush=True)
    print("===== REQUESTS =====", flush=True)
    seen=set()
    for m,u,pd in reqs:
        if '/api/' in u or 'login' in u.lower() or 'captcha' in u.lower():
            k=(m,u[:120])
            if k in seen: continue
            seen.add(k)
            print("  %-6s %-90s | body=%s"%(m,u[:90],pd[:120]), flush=True)
    b.close()
