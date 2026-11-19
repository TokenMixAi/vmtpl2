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
      const req=async(n,method,u,body)=>{try{const opt={method,headers:{'lang':'zh-CN'}};if(body){opt.headers['Content-Type']='application/json';opt.body=JSON.stringify(body);}const r=await fetch(u,opt);const ct=r.headers.get('content-type')||'';const t=await r.text();out[n]=r.status+'|'+ct.slice(0,20)+'|'+(t.length>200?t.slice(0,200):t);}catch(e){out[n]='ERR '+String(e).slice(0,60);}};
      await req('fb_list','GET','/api/v1/feedback');
      await req('fb_list_p1','GET','/api/v1/feedback?page=1');
      await req('fb_list_p1s','GET','/api/v1/feedback?page=1&pageSize=10');
      await req('fb_hist','GET','/api/v1/feedback?page=1&limit=20');
      await req('cmp_export','GET','/api/v1/compare/exportToExcel');
      await req('cmp_export_ids','GET','/api/v1/compare/exportToExcel?ids=131');
      await req('cmp_export_ids2','GET','/api/v1/compare/exportToExcel?listIds=131');
      await req('cmp_get','GET','/api/v1/compare');
      await req('cmp_get_ids','GET','/api/v1/compare?ids=131');
      await req('cmp_get_list','GET','/api/v1/compare?listIds=131');
      await req('cmp_show_list','GET','/api/v1/compare/show?listIds=131');
      await req('curves','GET','/api/v1/product/curves/9376');
      await req('dlcurve','GET','/api/v1/product/downloadCurve?productId=9376');
      await req('filt','GET','/api/v1/category/filterSameProducts/131');
      await req('cs_tickets','GET','/api/v1/cs/tickets');
      await req('cs_msg','GET','/api/v1/cs/messages');
      await req('acc_1','GET','/api/v1/acceptance/1');
      return out;
    }""")
    print('===== PII =====',flush=True)
    for k,v in res.items(): print('%-16s %s'%(k,v),flush=True)
    b.close()
