import json, os, sys
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
        html=page.content()
        if 'arg1=' not in html and 'renderData' not in html: break
    print('page title=',page.title(),'len=',len(page.content()), flush=True)
    res=page.evaluate("""async () => {
      const out={};
      const calls=[
        ['loginInfo','/api/v1/auth/loginInfo','GET',null],
        ['tokenTtl','/api/v1/auth/tokenTtl','GET',null],
        ['unifiedLogin','/api/v1/auth/unifiedLogin','POST',{}],
        ['smsLogin','/api/v1/auth/smsLogin','POST',{}],
        ['sendLoginSms','/api/v1/auth/sendLoginSms','POST',{}],
        ['fuliSms','/api/v1/fuli/sms','POST',{phone:'19999999999'}],
        ['fuliExchange','/api/v1/fuli/exchange','POST',{fuliAmount:50,phone:'19999999999',smsCode:'000000',requestId:'probe9137'}],
        ['home','/api/v1/home','GET',null],
        ['category','/api/v1/category','GET',null],
        ['clickCap','/api/v1/captcha/click','POST',{}],
      ];
      for(const [n,u,m,bd] of calls){
        try{
          const r=await fetch(u,{method:m,headers:{'Content-Type':'application/json','lang':'zh-CN','api-token':''},body:bd===null?undefined:JSON.stringify(bd)});
          out[n]=r.status+'|'+(await r.text()).slice(0,400);
        }catch(e){out[n]='ERR '+String(e).slice(0,120);}
      }
      return out;
    }""")
    print('\n===== API RESULTS =====', flush=True)
    for k,v in res.items(): print('%-14s %s'%(k,v), flush=True)
    b.close()
