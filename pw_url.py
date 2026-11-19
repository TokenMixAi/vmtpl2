from playwright.sync_api import sync_playwright
import json
TOKEN='c0e313cef2e76d00f48e310eed21a036'
UA='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
with sync_playwright() as p:
    b=p.chromium.launch(headless=False, args=['--disable-blink-features=AutomationControlled','--no-sandbox','--disable-dev-shm-usage'])
    c=b.new_context(user_agent=UA, viewport={'width':1366,'height':900}, locale='zh-CN', timezone_id='Asia/Shanghai')
    c.add_init_script("Object.defineProperty(navigator,'webdriver',{get:()=>undefined});window.chrome={runtime:{}};")
    page=c.new_page()
    page.goto('https://m.lbtek.com/points-mall', wait_until='domcontentloaded', timeout=60000)
    for i in range(15):
        page.wait_for_timeout(2000); h=page.content()
        if 'arg1=' not in h and 'renderData' not in h: break
    print('ready',flush=True)
    r=page.evaluate("""async (tok) => {
      const out={};
      const H={'lang':'zh-CN','Content-Type':'application/json','api-token':tok};
      const post=async(n,u,body)=>{try{const r=await fetch(u,{method:'POST',headers:H,body:JSON.stringify(body)});const t=await r.text();out[n]=r.status+'|'+(t.length>260?t.slice(0,260):t);}catch(e){out[n]='ERR '+String(e).slice(0,50);}};
      const get=async(n,u)=>{try{const r=await fetch(u,{headers:H});const t=await r.text();out[n]=r.status+'|'+(t.length>200?t.slice(0,200):t);}catch(e){out[n]='ERR '+String(e).slice(0,50);}};
      await get('loginInfo','/api/v1/auth/loginInfo');
      await post('fuli_sms','/api/v1/fuli/sms',{phone:'19900000001'});
      await post('fuli_ex1','/api/v1/fuli/exchange',{fuliAmount:50,phone:'19900000001',smsCode:'123456',requestId:'x1'});
      await post('fuli_ex2','/api/v1/fuli/exchange',{fuli_amount:50,phone:'19900000001',sms_code:'123456',request_id:'x2'});
      await get('integral','/api/v1/user/integral');
      await post('int_order','/api/v1/integral/order',{});
      return out;
    }""", TOKEN)
    print('===== CROSS =====',flush=True)
    for k,v in r.items(): print('%-12s %s'%(k,v),flush=True)
    b.close()
