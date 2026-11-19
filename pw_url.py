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
      const req=async(n,method,u,body,hdrs)=>{
        try{
          const h=Object.assign({'lang':'zh-CN'},hdrs||{});
          let opt={method,headers:h};
          if(body){h['Content-Type']='application/json';opt.body=JSON.stringify(body);}
          const r=await fetch(u,opt);const t=await r.text();
          out[n]=r.status+'|'+(t.length>230?t.slice(0,230):t);
        }catch(e){out[n]='ERR '+String(e).slice(0,70);}
      };
      const FAKE={'api-token':'00000000000000000000000000000000'};
      await req('A1_fuli_sms_noTok','POST','/api/v1/fuli/sms',{phone:'19900000001'});
      await req('A2_fuli_exch_noTok','POST','/api/v1/fuli/exchange',{fuliAmount:50,phone:'19900000001',smsCode:'123456',requestId:'probe1'});
      await req('A3_fuli_exch_fakeTok','POST','/api/v1/fuli/exchange',{fuliAmount:50,phone:'19900000001',smsCode:'123456',requestId:'probe2'},FAKE);
      await req('B1_smsLogin_full','POST','/api/v1/auth/smsLogin',{phone:'19900000001',code:'123456'});
      await req('B2_smsLogin_emptyCode','POST','/api/v1/auth/smsLogin',{phone:'19900000001',code:''});
      await req('B3_smsLogin_nocode','POST','/api/v1/auth/smsLogin',{phone:'19900000001'});
      await req('B4_smsLogin_empty','POST','/api/v1/auth/smsLogin',{});
      await req('B5_unified_fake','POST','/api/v1/auth/unifiedLogin',{identifier:'19900000001',password:'123456'});
      await req('B6_sendLoginSms','POST','/api/v1/auth/sendLoginSms',{phone:'19900000001'});
      await req('C1_register','POST','/api/v1/auth/register',{phone:'19900000001',code:'123456',password:'Test123456'});
      await req('C2_signup','POST','/api/v1/auth/signup',{phone:'19900000001'});
      await req('D1_loginInfo_noTok','GET','/api/v1/auth/loginInfo');
      await req('D2_loginInfo_fakeTok','GET','/api/v1/auth/loginInfo',null,FAKE);
      await req('E1_home','GET','/api/v1/home');
      await req('E2_userIntegral','GET','/api/v1/user/integral');
      return out;
    }""")
    print('===== API2 =====',flush=True)
    for k,v in res.items(): print('%-24s %s'%(k,v),flush=True)
    b.close()
