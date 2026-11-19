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
      const call=async(n,u,m,bd)=>{try{const o={method:m,headers:{'Content-Type':'application/json','lang':'zh-CN'}};if(bd!==null)o.body=JSON.stringify(bd);const r=await fetch(u,o);const ct=r.headers.get('content-type')||'';const t=await r.text();out[n]=r.status+'|'+ct.slice(0,20)+'|'+(t.length>180?t.slice(0,180):t);}catch(e){out[n]='ERR '+String(e).slice(0,80);}};
      await call('c_empty','/api/v1/order/contract/','POST',{});
      await call('c_id','/api/v1/order/contract/','POST',{id:1});
      await call('c_orderId','/api/v1/order/contract/','POST',{orderId:1});
      await call('c_orderSn','/api/v1/order/contract/','POST',{orderSn:'20250101001'});
      await call('c_ids','/api/v1/order/contract/','POST',{orderIds:[1]});
      await call('c_get','/api/v1/order/contract/1','GET',null);
      await call('leadtime','/api/v1/product/leadtime/1','GET',null);
      await call('prod_id','/api/v1/product/1','GET',null);
      await call('prod_show_id','/api/v1/product/show?id=1','GET',null);
      await call('quote_get','/api/v1/order/quote/1','POST',{});
      await call('dl_options','/api/v1/order/downloadOptions/1','GET',null);
      await call('fb_types','/api/v1/feedback/types','GET',null);
      await call('fb_hist','/api/v1/feedback','GET',null);
      return out;
    }""")
    print('===== CONTRACT =====',flush=True)
    for k,v in res.items(): print('%-14s %s'%(k,v),flush=True)
    b.close()
