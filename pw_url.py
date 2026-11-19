from playwright.sync_api import sync_playwright
import json,time
UA='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
captured={}
def on_resp(r):
    if '/api/v1/captcha/click' in r.url and 'verify' not in r.url:
        try: captured['cap']=r.json()
        except: pass
with sync_playwright() as p:
    b=p.chromium.launch(headless=False, args=['--disable-blink-features=AutomationControlled','--no-sandbox','--disable-dev-shm-usage'])
    ctx=b.new_context(user_agent=UA, viewport={'width':1366,'height':900}, locale='en-US', timezone_id='Asia/Shanghai')
    ctx.add_init_script("Object.defineProperty(navigator,'webdriver',{get:()=>undefined});window.chrome={runtime:{}};")
    page=ctx.new_page(); page.on('response',on_resp)
    page.goto('https://en.lbtek.com/register', wait_until='domcontentloaded', timeout=60000)
    page.wait_for_timeout(5000)
    print('title:',page.title()[:60],flush=True)
    # 找 email 输入
    try:
        page.fill('input[type="email"], input[placeholder*="mail" i]', 'probe@example.com', timeout=8000)
        print('email filled',flush=True)
    except Exception as e: print('email fill err',str(e)[:80],flush=True)
    # 触发验证码（点“发送验证码”按钮）
    clicked=False
    for txt in ['Send','send','Verification Code','获取验证码','发送验证码']:
        try:
            page.get_by_text(txt, exact=False).first.click(timeout=3000); clicked=True; print('clicked',txt,flush=True); break
        except: continue
    if not clicked:
        # 用 suffix 里的按钮
        try: page.locator('button').filter(has_text='Send').first.click(timeout=3000); clicked=True
        except: pass
    page.wait_for_timeout(4000)
    cap=captured.get('cap')
    print('captcha captured:', bool(cap),flush=True)
    if cap:
        d=cap.get('data',{})
        print('cid',d.get('captcha_id'),'positions',d.get('positions'),flush=True)
        img=d.get('image','')
        # 点选：在页面上找到验证码图片元素，点击对应坐标
        try:
            el=page.locator('img[src^="data:image"]').first
            box=el.bounding_box()
            print('img box',box,flush=True)
            # 原图 450x200，页面显示可能缩放
            scale_x=box['width']/450.0; scale_y=box['height']/200.0
            for p_ in d.get('pos',[]):
                cx=box['x']+(p_['x']+p_['width']/2)*scale_x
                cy=box['y']+(p_['y']+p_['height']/2)*scale_y
                page.mouse.click(cx,cy); page.wait_for_timeout(300)
            print('clicked all pos',flush=True)
        except Exception as e: print('click err',str(e)[:100],flush=True)
        page.wait_for_timeout(3000)
        print('after click body snippet:', page.content()[:200].replace('\n',' '),flush=True)
    b.close()
