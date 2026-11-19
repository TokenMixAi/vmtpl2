from playwright.sync_api import sync_playwright
import json,urllib.request,ssl,random,string
c0=ssl.create_default_context(); c0.check_hostname=False; c0.verify_mode=ssl.CERT_NONE
def req(url,data=None,hdr=None):
    r=urllib.request.Request(url,data=json.dumps(data).encode() if data else None,headers=hdr or {'Content-Type':'application/json'},method='POST' if data else 'GET')
    return json.loads(urllib.request.urlopen(r,timeout=15,context=c0).read().decode())
dom=req('https://api.mail.tm/domains')['hydra:member'][0]['domain']
u=''.join(random.choices(string.ascii_lowercase+string.digits,k=10)); ADDR=f'{u}@{dom}'
req('https://api.mail.tm/accounts',{'address':ADDR,'password':'Probe12345!'})
JWT=req('https://api.mail.tm/token',{'address':ADDR,'password':'Probe12345!'})['token']
print('EMAIL='+ADDR,flush=True)
cap={}; ver={}; send={}
def on_resp(r):
    try:
        j=r.json()
        if '/captcha/click/verify' in r.url: ver['d']=j
        elif '/captcha/click' in r.url: cap['d']=j
        elif '/sendRegisterEmail' in r.url: send['d']=j
    except: pass
UA='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
with sync_playwright() as p:
    b=p.chromium.launch(headless=False, args=['--disable-blink-features=AutomationControlled','--no-sandbox','--disable-dev-shm-usage'])
    c=b.new_context(user_agent=UA, viewport={'width':1366,'height':900}, locale='en-US')
    c.add_init_script("Object.defineProperty(navigator,'webdriver',{get:()=>undefined});window.chrome={runtime:{}};")
    page=c.new_page(); page.on('response',on_resp)
    page.goto('https://en.lbtek.com/register', wait_until='domcontentloaded', timeout=60000)
    page.wait_for_timeout(4500)
    try: page.locator('input[placeholder*="mail" i]').first.fill(ADDR, timeout=6000); print('filled',flush=True)
    except Exception as e: print('fill fail',str(e)[:60],flush=True)
    for t in ['Send','Verification Code']:
        try: page.get_by_text(t, exact=False).first.click(timeout=3000); print('clicked',t,flush=True); break
        except: continue
    page.wait_for_timeout(6000)
    # 检查 canvas / 背景图 / 所有元素含 data:image
    info=page.evaluate("""() => {
      const out=[];
      document.querySelectorAll('canvas').forEach(el=>{const r=el.getBoundingClientRect();out.push({t:'canvas',w:Math.round(r.width),h:Math.round(r.height),x:Math.round(r.x),y:Math.round(r.y)});});
      document.querySelectorAll('*').forEach(el=>{const bg=getComputedStyle(el).backgroundImage;if(bg&&bg.includes('data:image')){const r=el.getBoundingClientRect();out.push({t:'bg',w:Math.round(r.width),h:Math.round(r.height),x:Math.round(r.x),y:Math.round(r.y),bg:bg.slice(0,30)});}});
      return out;
    }""")
    print('CANVAS_BG:',json.dumps(info)[:600],flush=True)
    d=cap.get('d',{}).get('data',{})
    print('pos_n',len(d.get('pos',[])),flush=True)
    # 若找到尺寸接近 450x200 的 canvas/bg → 点击
    tgt=None
    for x in info:
        if x['w']>200 and 100<x['h']<300: tgt=x; break
    if tgt:
        print('TGT',json.dumps(tgt),flush=True)
        sx=tgt['w']/450.0; sy=tgt['h']/200.0
        for q in d.get('pos',[]):
            page.mouse.click(tgt['x']+(q['x']+q['width']/2)*sx, tgt['y']+(q['y']+q['height']/2)*sy); page.wait_for_timeout(400)
        page.wait_for_timeout(3500)
        print('verify:',json.dumps(ver.get('d',{}),ensure_ascii=False)[:200],flush=True)
        print('send:',json.dumps(send.get('d',{}),ensure_ascii=False)[:200],flush=True)
    else: print('NO_CANVAS',flush=True)
    b.close()
