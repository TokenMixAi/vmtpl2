from playwright.sync_api import sync_playwright
import json,time,urllib.request,ssl,random,string
ctx0=ssl.create_default_context(); ctx0.check_hostname=False; ctx0.verify_mode=ssl.CERT_NONE
def req(url,data=None):
    r=urllib.request.Request(url,data=json.dumps(data).encode() if data else None,headers={'Content-Type':'application/json'},method='POST' if data else 'GET')
    return json.loads(urllib.request.urlopen(r,timeout=15,context=ctx0).read().decode())
dom=req('https://api.mail.tm/domains')['hydra:member'][0]['domain']
u=''.join(random.choices(string.ascii_lowercase+string.digits,k=10)); ADDR=f'{u}@{dom}'; PW='Probe12345!'
req('https://api.mail.tm/accounts',{'address':ADDR,'password':PW})
JWT=req('https://api.mail.tm/token',{'address':ADDR,'password':PW})['token']
print('EMAIL='+ADDR,flush=True)
cap={}; send_resp={}
def on_resp(r):
    try:
        if '/api/v1/captcha/click' in r.url and 'verify' not in r.url: cap['d']=r.json()
        if '/api/v1/register/sendRegisterEmail' in r.url: send_resp['d']=r.json()
    except: pass
UA='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
with sync_playwright() as p:
    b=p.chromium.launch(headless=False, args=['--disable-blink-features=AutomationControlled','--no-sandbox','--disable-dev-shm-usage'])
    c=b.new_context(user_agent=UA, viewport={'width':1366,'height':900}, locale='en-US')
    c.add_init_script("Object.defineProperty(navigator,'webdriver',{get:()=>undefined});window.chrome={runtime:{}};")
    page=c.new_page(); page.on('response',on_resp)
    page.goto('https://en.lbtek.com/register', wait_until='domcontentloaded', timeout=60000)
    page.wait_for_timeout(4000)
    try: page.fill('input[type="email"], input[placeholder*="mail" i]', ADDR, timeout=8000)
    except Exception as e: print('fill err',str(e)[:60],flush=True)
    for txt in ['Send','Verification Code']:
        try: page.get_by_text(txt, exact=False).first.click(timeout=3000); break
        except: continue
    page.wait_for_timeout(4000)
    d=cap.get('d',{}).get('data',{})
    print('cid',d.get('captcha_id'),'pos_n',len(d.get('pos',[])),flush=True)
    # 找所有图片，选最大
    best=None
    for el in page.locator('img').all():
        try:
            bb=el.bounding_box()
            if bb and bb['width']>50 and bb['height']>20:
                if not best or bb['width']*bb['height']>best[0]: best=(bb['width']*bb['height'],bb,el)
        except: pass
    if not best:
        print('no img found',flush=True)
    else:
        _,box,el=best
        print('picked img box',box,flush=True)
        sx=box['width']/450.0; sy=box['height']/200.0
        for q in d.get('pos',[]):
            cx=box['x']+(q['x']+q['width']/2)*sx; cy=box['y']+(q['y']+q['height']/2)*sy
            page.mouse.click(cx,cy); page.wait_for_timeout(350)
        print('clicked',flush=True)
        page.wait_for_timeout(3500)
        print('send_resp:',json.dumps(send_resp.get('d',{}),ensure_ascii=False)[:200],flush=True)
    # 若发码成功则收信
    if send_resp.get('d',{}).get('success'):
        for i in range(6):
            time.sleep(5)
            M=req('https://api.mail.tm/messages') if False else None
            r=urllib.request.Request('https://api.mail.tm/messages',headers={'Authorization':'Bearer '+JWT})
            M=json.loads(urllib.request.urlopen(r,timeout=15,context=ctx0).read().decode())
            if M.get('hydra:member'):
                import re
                txt=' '.join((m.get('intro') or '') for m in M['hydra:member'])
                mm=re.search(r'(\d{4,8})',txt)
                print('MAIL_CODE='+(mm.group(1) if mm else 'none'),flush=True); break
    b.close()
