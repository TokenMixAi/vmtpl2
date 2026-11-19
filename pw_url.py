import os, base64, json
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
      const get=async(n,u)=>{try{const r=await fetch(u,{headers:{'lang':'zh-CN'}});const t=await r.text();out[n]=r.status+'|'+(t.length>260?t.slice(0,260):t);}catch(e){out[n]='ERR';}};
      await get('qn_base','/api/v1/complaint/qiniuToken');
      await get('qn_img','/api/v1/complaint/qiniuToken?bucket=image-lbtek');
      await get('qn_file','/api/v1/complaint/qiniuToken?bucket=file-lbtek');
      await get('qn_priv','/api/v1/complaint/qiniuToken?bucket=lbtek');
      await get('qn_other','/api/v1/complaint/qiniuToken?bucket=test');
      await get('qn_empty','/api/v1/complaint/qiniuToken?bucket=');
      await get('qn_scope','/api/v1/complaint/qiniuToken?scope=file-lbtek');
      await get('qn_key','/api/v1/complaint/qiniuToken?key=probe9137.php');
      await get('rec','/api/v1/search/recommend');
      return out;
    }""")
    print('===== QN2 =====',flush=True)
    for k,v in res.items(): print('%-10s %s'%(k,v),flush=True)
    b.close()
