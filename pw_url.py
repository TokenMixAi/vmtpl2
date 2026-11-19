from playwright.sync_api import sync_playwright
import re
UA='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
with sync_playwright() as p:
    b=p.chromium.launch(headless=False, args=['--disable-blink-features=AutomationControlled','--no-sandbox','--disable-dev-shm-usage'])
    ctx=b.new_context(user_agent=UA, viewport={'width':1366,'height':768}, locale='zh-CN', timezone_id='Asia/Shanghai')
    ctx.add_init_script("Object.defineProperty(navigator,'webdriver',{get:()=>undefined});window.chrome={runtime:{}};")
    page=ctx.new_page()
    for u in ['https://www.lubon.com/','https://www.lubon.com/join-us']:
        try:
            page.goto(u, wait_until='domcontentloaded', timeout=45000)
            page.wait_for_timeout(6000)
            html=page.content()
            print('===== %s | len=%d | title=%s =====' % (u, len(html), page.title()[:80]), flush=True)
            txt=re.sub(r'<script[\s\S]*?</script>','',html); txt=re.sub(r'<style[\s\S]*?</style>','',txt); txt=re.sub(r'<[^>]+>',' ',txt); txt=re.sub(r'\s+',' ',txt)
            print('TEXT:', txt[:1500].encode('utf-8','replace').decode('utf-8'), flush=True)
            em=set(re.findall(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}', html))
            print('EMAILS:', sorted(em)[:20], flush=True)
            links=sorted(set(re.findall(r'href="(/[^"#]{1,60})"', html)))
            print('LINKS:', links[:40], flush=True)
        except Exception as e:
            print('ERR', u, str(e)[:100], flush=True)
    b.close()
