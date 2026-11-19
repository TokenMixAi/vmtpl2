from playwright.sync_api import sync_playwright
import json,time,urllib.request,ssl,random,string
c0=ssl.create_default_context(); c0.check_hostname=False; c0.verify_mode=ssl.CERT_NONE
def req(url,data=None):
    r=urllib.request.Request(url,data=json.dumps(data).encode() if data else None,headers={'Content-Type':'application/json'},method='POST' if data else 'GET')
    return json.loads(urllib.request.urlopen(r,timeout=15,context=c0).read().decode())
dom=req('https://api.mail.tm/domains')['hydra:member'][0]['domain']
u=''.join(random.choices(string.ascii_lowercase+string.digits,k=10)); ADDR=f'{u}@{dom}'; PW='Probe12345!'
req('https://api.mail.tm/accounts',{'address':ADDR,'password':PW})
JWT=req('https://api.mail.tm/token',{'address':ADDR,'password':PW})['token']
print('EMAIL='+ADDR,flush=True)
cap={}; send={}
def on_resp(r):
    try:
        if '/captcha/click' in r.url and 'verify' not in r.url: cap['d']=r.json()
        if '/register/sendRegisterEmail' in r.url: send['d']=r.json()
    except: pass
UA='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
with sync_playwright() as p:
    b=p.chromium.launch(headless=False, args=['--disable-blink-features=AutomationControlled','--no-sandbox','--disable-dev-shm-usage'])
    c=b.new_context(user_agent=UA, viewport={'width':1366,'height':900}, locale='en-US')
    c.add_init_script("Object.defineProperty(navigator,'webdriver',{get:()=>undefined});window.chrome={runtime:{}};")
    page=c.new_page(); page.on('response',on_resp)
    page.goto('https://en.lbtek.com/register', wait_until='domcontentloaded', timeout=60000)
    page.wait_for_timeout(4500)
    # 宽松选择器填邮箱
    filled=False
    for sel in ['input[placeholder*="mail" i]','input[type="text"]','input']:
        try:
            page.locator(sel).first.fill(ADDR, timeout=5000); filled=True; print('filled via',sel,flush=True); break
        except: continue
    if not filled: print('FILL_FAIL',flush=True)
    for txt in ['Send','Verification Code','Get Code']:
        try: page.get_by_text(txt, exact=False).first.click(timeout=3000); print('clicked',txt,flush=True); break
        except: continue
    page.wait_for_timeout(4500)
    d=cap.get('d',{}).get('data',{})
    print('cid',d.get('captcha_id'),'pos_n',len(d.get('pos',[])),flush=True)
    # 在页面里找 naturalWidth==450 的图片
    info=page.evaluate("""() => {
      const out=[]; document.querySelectorAll('img').forEach(el=>{
        const r=el.getBoundingClientRect();
        out.push({nw:el.naturalWidth,nh:el.naturalHeight,w:Math.round(r.width),h:Math.round(r.height),x:Math.round(r.x),y:Math.round(r.y),src:(el.src||'').slice(0,30)});
      }); return out;
    }""")
    print('IMGS:',json.dumps(info)[:800],flush=True)
    target=None
    for im in info:
        if im['nw']>=400 and im['nh']>=150: target=im; break
    if target:
        print('TARGET',json.dumps(target),flush=True)
        sx=target['w']/target['nw']; sy=target['h']/target['nh']
        for q in d.get('pos',[]):
            cx=target['x']+(q['x']+q['width']/2)*sx; cy=target['y']+(q['y']+q['height']/2)*sy
            page.mouse.click(cx,cy); page.wait_for_timeout(400)
        print('clicked',flush=True); page.wait_for_timeout(4000)
        print('send_resp:',json.dumps(send.get('d',{}),ensure_ascii=False)[:200],flush=True)
    else:
        print('NO_TARGET_IMG',flush=True)
    b.close()
