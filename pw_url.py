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
      const call=async(n,u,m,bd,h)=>{try{const o={method:m,headers:Object.assign({'Content-Type':'application/json','lang':'zh-CN'},h||{})};if(bd!==null)o.body=JSON.stringify(bd);const r=await fetch(u,o);const t=await r.text();out[n]=r.status+'|'+(t.length>260?t.slice(0,260):t);}catch(e){out[n]='ERR '+String(e).slice(0,100);}};
      await call('island_idx','/__nuxt_island/page_index','GET',null);
      await call('island_pm','/__nuxt_island/page_points-mall','GET',null);
      await call('island_empty','/__nuxt_island/empty','GET',null);
      await call('pct2f_api','/api/v1/home%2F','GET',null);
      await call('pct3f_api','/api/v1/home%3F','GET',null);
      await call('test_get','/api/v1/test','GET',null);
      await call('notfound','/api/v1/not-found-log','POST',{url:'https://m.lbtek.com/x',path:'/x',from:'https://m.lbtek.com/'});
      await call('membervisit','/api/v1/member-visit','GET',null);
      await call('clickrec','/api/v1/home/clickRecord','POST',{productId:1,type:1});
      await call('otherexp','/api/v1/product/leadTime','POST',{});
      return out;
    }""")
    print('===== NUXT =====',flush=True)
    for k,v in res.items(): print('%-12s %s'%(k,v),flush=True)
    b.close()
