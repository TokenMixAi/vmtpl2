from playwright.sync_api import sync_playwright
import json
cap={}
def on_resp(r):
    if '/api/v1/captcha/click' in r.url and 'verify' not in r.url:
        try: cap['d']=r.json()
        except: pass
UA='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
with sync_playwright() as p:
    b=p.chromium.launch(headless=False, args=['--disable-blink-features=AutomationControlled','--no-sandbox','--disable-dev-shm-usage'])
    c=b.new_context(user_agent=UA, viewport={'width':1366,'height':900}, locale='en-US')
    c.add_init_script("Object.defineProperty(navigator,'webdriver',{get:()=>undefined});window.chrome={runtime:{}};")
    page=c.new_page(); page.on('response',on_resp)
    page.goto('https://en.lbtek.com/register', wait_until='domcontentloaded', timeout=60000)
    page.wait_for_timeout(4000)
    page.fill('input[type="email"]', 'probe@example.com')
    for txt in ['Send','Verification Code']:
        try: page.get_by_text(txt, exact=False).first.click(timeout=3000); break
        except: continue
    page.wait_for_timeout(5000)
    print('CAP:', bool(cap.get('d')), flush=True)
    # dump 所有可见 img / canvas / 含 data:image 的元素
    info=page.evaluate("""() => {
      const out=[];
      document.querySelectorAll('img,canvas,[style*="data:image"]').forEach((el,i)=>{
        const r=el.getBoundingClientRect();
        const st=getComputedStyle(el);
        out.push({tag:el.tagName, cls:(el.className||'').toString().slice(0,40),
                  w:Math.round(r.width),h:Math.round(r.height),x:Math.round(r.x),y:Math.round(r.y),
                  src:(el.src||'').slice(0,40), bg:(st.backgroundImage||'').slice(0,40)});
      });
      return out;
    }""")
    for x in info: print(json.dumps(x,ensure_ascii=False),flush=True)
    # dump dialogs
    html=page.evaluate("""() => {
      const d=document.querySelectorAll('.el-dialog,.ant-modal,.el-overlay-dialog,[role="dialog"],.van-popup,.modal');
      return Array.from(d).map(e=>e.outerHTML.slice(0,1200));
    }""")
    print('DIALOGS:',len(html),flush=True)
    for h in html[:2]: print(h[:1200],flush=True)
    b.close()
