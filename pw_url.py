import os
from playwright.sync_api import sync_playwright
UA='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
with sync_playwright() as p:
    b=p.chromium.launch(headless=False, args=['--disable-blink-features=AutomationControlled','--no-sandbox','--disable-dev-shm-usage'])
    ctx=b.new_context(user_agent=UA, viewport={'width':1366,'height':768}, locale='zh-CN', timezone_id='Asia/Shanghai')
    ctx.add_init_script("Object.defineProperty(navigator,'webdriver',{get:()=>undefined});window.chrome={runtime:{}};")
    page=ctx.new_page(); page.goto("https://m.lbtek.com/points-mall", wait_until="domcontentloaded", timeout=60000)
    for i in range(12):
        page.wait_for_timeout(2000); c=page.content()
        if 'arg1=' not in c and 'renderData' not in c: break
    print('ready',flush=True)
    res=page.evaluate("""async () => {
      const out={};
      const get=async(n,u)=>{try{const r=await fetch(u,{headers:{'lang':'zh-CN'}});const ct=r.headers.get('content-type')||'';const t=await r.text();out[n]=r.status+'|'+ct.slice(0,22)+'|'+(t.length>200?t.slice(0,200):t);}catch(e){out[n]='ERR '+String(e).slice(0,60);}};
      await get('prod_1395','/api/v1/product/1395');
      await get('prod_131','/api/v1/product/131');
      await get('ps_listId','/api/v1/product/show?listId=131');
      await get('ps_listIds','/api/v1/product/show?listIds=131');
      await get('ps_productIds','/api/v1/product/show?productIds=131');
      await get('ps_sn','/api/v1/product/show?productSn=AMM-1B');
      await get('ct_48028','/api/v1/order/contract/48028');
      await get('ct_48029','/api/v1/order/contract/48029');
      await get('ct_20261115001','/api/v1/order/contract/20261115001');
      await get('lt_1395','/api/v1/product/leadtime/1395?num=1');
      await get('lt_131','/api/v1/product/leadtime/131?num=1');
      return out;
    }""")
    print('===== PRECISE =====',flush=True)
    for k,v in res.items(): print('%-16s %s'%(k,v),flush=True)
    b.close()
