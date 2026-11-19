import json, os
from playwright.sync_api import sync_playwright
U=os.environ.get('PROBE_URL','https://m.lbtek.com/points-mall')
UA='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
with sync_playwright() as p:
    b=p.chromium.launch(headless=False, args=['--disable-blink-features=AutomationControlled','--no-sandbox','--disable-dev-shm-usage'])
    ctx=b.new_context(user_agent=UA, viewport={'width':1366,'height':768}, locale='zh-CN', timezone_id='Asia/Shanghai')
    ctx.add_init_script("Object.defineProperty(navigator,'webdriver',{get:()=>undefined});window.chrome={runtime:{}};")
    page=ctx.new_page()
    page.goto(U, wait_until='domcontentloaded', timeout=60000)
    for i in range(12):
        page.wait_for_timeout(2000)
        if 'arg1=' not in page.content() and 'renderData' not in page.content(): break
    print('ready title=',page.title(), flush=True)
    res=page.evaluate("""async () => {
      const out={};
      const post=async(n,u,bd)=>{
        try{const r=await fetch(u,{method:'POST',headers:{'Content-Type':'application/json','lang':'zh-CN'},body:JSON.stringify(bd)});
          out[n]=r.status+'|'+(await r.text()).slice(0,300);}catch(e){out[n]='ERR '+String(e).slice(0,100);}
      };
      await post('u_admin','/api/v1/auth/unifiedLogin',{identifier:'admin',password:'Zz9137Probe'});
      await post('u_nouser','/api/v1/auth/unifiedLogin',{identifier:'zz9137nonexist',password:'Zz9137Probe'});
      await post('u_phone','/api/v1/auth/unifiedLogin',{identifier:'19999999999',password:'Zz9137Probe'});
      await post('u_realphone','/api/v1/auth/unifiedLogin',{identifier:'18890012718',password:'Zz9137Probe'});
      await post('u_email','/api/v1/auth/unifiedLogin',{identifier:'hr@lbtek.com',password:'Zz9137Probe'});
      await post('u_noPwd','/api/v1/auth/unifiedLogin',{identifier:'admin'});
      await post('u_type','/api/v1/auth/unifiedLogin',{identifier:'admin',password:'Zz9137Probe',type:'password'});
      await post('sms_fake','/api/v1/auth/smsLogin',{phone:'19999999999',smsCode:'000000'});
      await post('sendsms_fake','/api/v1/auth/sendLoginSms',{phone:'19999999999'});
      return out;
    }""")
    print('\n===== LOGIN PROBE =====', flush=True)
    for k,v in res.items(): print('%-14s %s'%(k,v), flush=True)
    b.close()
