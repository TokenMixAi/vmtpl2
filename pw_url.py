import json, re, os, sys
from playwright.sync_api import sync_playwright
URLS=[u.strip() for u in os.environ.get('PROBE_URL','').split(',') if u.strip()]
if not URLS:
    print('NO_PROBE_URL'); sys.exit(1)
UA='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
reqs=[]; console=[]
with sync_playwright() as p:
    b=p.chromium.launch(headless=False, args=['--disable-blink-features=AutomationControlled','--no-sandbox','--disable-dev-shm-usage'])
    ctx=b.new_context(user_agent=UA, viewport={'width':1366,'height':768}, locale='zh-CN', timezone_id='Asia/Shanghai', java_script_enabled=True)
    ctx.add_init_script("Object.defineProperty(navigator,'webdriver',{get:()=>undefined});window.chrome={runtime:{}};")
    page=ctx.new_page()
    page.on("request", lambda r: reqs.append((r.method, r.url, r.resource_type)))
    page.on("console", lambda m: console.append(m.text[:200]))
    for U in URLS:
        print('\n===== VISIT =====', flush=True)
        try:
            resp=page.goto(U, wait_until='domcontentloaded', timeout=60000)
            print('goto status=%s'%(resp.status if resp else None), flush=True)
            for i in range(15):
                page.wait_for_timeout(2000)
                try: page.mouse.move(200+i*13,200+i*7)
                except: pass
                html=page.content()
                if 'arg1=' not in html and 'acw_sc__v2' not in html and 'renderData' not in html: break
            html=page.content()
            print('len=%d title=%s'%(len(html), page.title()), flush=True)
            print('--- NUXT REFS ---')
            for m in sorted(set(re.findall(r'/_nuxt/[A-Za-z0-9._~-]+\.(?:js|mjs|css|json)', html))): print('  ',m)
            print('--- API REFS in HTML ---')
            for m in sorted(set(re.findall(r'["\x27](/[a-zA-Z][a-zA-Z0-9_/-]*(?:api|Api)[a-zA-Z0-9_/-]*)["\x27]', html)))[:20]: print('  ',m)
            txt=page.evaluate("()=>document.body?document.body.innerText.slice(0,600):''")
            print('--- TEXT ---'); print(txt.replace('\n',' | ')[:600])
        except Exception as e: print('FATAL', str(e)[:300], flush=True)
    print('\n===== INTERESTING REQUESTS =====', flush=True)
    seen=set()
    for m,u,t in reqs:
        if ('/_nuxt/' in u or '/api/' in u or '/mallApi/' in u) and u not in seen:
            seen.add(u); print('  %-6s %-12s %s'%(m,t,u[:220]), flush=True)
    print('\n===== COOKIES =====', flush=True)
    print(json.dumps([(c['name'],c['value'][:40]) for c in ctx.cookies()]))
    b.close()
