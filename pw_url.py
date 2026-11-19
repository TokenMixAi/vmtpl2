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
      const call=async(n,u,m,bd)=>{try{const o={method:m,headers:{'Content-Type':'application/json','lang':'zh-CN'}};if(bd!==null)o.body=JSON.stringify(bd);const r=await fetch(u,o);const t=await r.text();out[n]=r.status+'|'+(t.length>200?t.slice(0,200):t);}catch(e){out[n]='ERR '+String(e).slice(0,80);}};
      await call('cart_list','/api/v1/cart/list','GET',null);
      await call('cart_export','/api/v1/cart/export','POST',{});
      await call('cart_dl_tpl','/api/v1/cart/downloadTemplate','GET',null);
      await call('cart_bags','/api/v1/cart/bags','GET',null);
      await call('cart_quote','/api/v1/cart/quote','POST',{});
      await call('order_list','/api/v1/order/list','GET',null);
      await call('order_pending','/api/v1/order/pendingCount','GET',null);
      await call('order_contract','/api/v1/order/contract/1','GET',null);
      await call('order_contract_sn','/api/v1/order/contract/20250101001','GET',null);
      await call('order_reasons','/api/v1/order/cancel/reasons','GET',null);
      await call('order_express','/api/v1/order/express/routes','GET',null);
      await call('product_show','/api/v1/product/show','GET',null);
      await call('compare_show','/api/v1/compare/show','GET',null);
      await call('compare_exp','/api/v1/compare/exportToExcel','POST',{});
      await call('invoice_apply','/api/v1/invoiceApply/apply','POST',{});
      await call('invoice_chg','/api/v1/invoiceChangeConfirm/check','POST',{});
      await call('feedback','/api/v1/feedback','POST',{});
      await call('question','/api/v1/question','GET',null);
      await call('area','/api/v1/area','GET',null);
      await call('calc','/api/v1/calculator/rules','GET',null);
      await call('home_cart','/api/v1/home/cartCount','GET',null);
      return out;
    }""")
    print('===== SWEEP =====',flush=True)
    for k,v in res.items(): print('%-16s %s'%(k,v),flush=True)
    b.close()
