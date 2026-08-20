import json,os,io,urllib.request as ur,urllib.parse as up,random,traceback,subprocess
API='https://api.telegram.org/bot'+os.environ['TOKEN'];CHAT='227491135'
def post(p,d,ct='application/json'):
    return ur.urlopen(ur.Request(API+p,data=d,headers={'Content-Type':ct}),timeout=40).read()
def txt(t):post('/sendMessage',json.dumps({'chat_id':CHAT,'text':t}).encode())
def get(u,t=40):return ur.urlopen(ur.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=t).read()
def fa(n):
    d=''.join(chr(1776+i) for i in range(10));s=format(int(n),',');o=''
    for c in s:o+=d[int(c)] if c.isdigit() else ('٬' if c==',' else c)
    return o
def part(s,a,b):
    i=s.find(a)
    if i<0:return ''
    j=s.find(b,i+1)
    return s[i+len(a):j if j>0 else len(s)].strip()
def wrap(s,n):
    out=[];cur=''
    for w in s.split(' '):
        if len(cur)+len(w)+1>n:out.append(cur);cur=w
        else:cur=(cur+' '+w).strip()
    if cur:out.append(cur)
    return out
def send_file(path,ff,fname,fdata,fctype,caption):
    b='----fxB';body=b''
    body+=('--'+b+'\r\n').encode()+b'Content-Disposition: form-data; name="chat_id"\r\n\r\n'+CHAT.encode()+b'\r\n'
    if caption:
        body+=('--'+b+'\r\n').encode()+b'Content-Disposition: form-data; name="caption"\r\n\r\n'+caption[:1024].encode()+b'\r\n'
    body+=('--'+b+'\r\n').encode()+('Content-Disposition: form-data; name="%s"; filename="%s"\r\nContent-Type: %s\r\n\r\n'%(ff,fname,fctype)).encode()+fdata+('\r\n--'+b+'--\r\n').encode()
    post(path,body,'multipart/form-data; boundary='+b)
try:
    usdt=0;ounce=0.0
    try:usdt=int(json.loads(get('https://mbms-1356.github.io/forexin-site-/price.json',10)).get('usdt',0))
    except Exception:pass
    try:ounce=float(json.loads(get('https://api.gold-api.com/price/XAU',10)).get('price',0))
    except Exception:pass
    g18=int(usdt*ounce/31.1035*0.75) if usdt and ounce else 0
    T=[('روانشناسی معاملات: احساسات دشمن تریدر','trader emotions dark desk cinematic'),
    ('استاپ‌لاس: بیمهٔ حرفه‌ای‌ها','golden shield protecting coins, dark luxury'),
    ('اهرم؛ شمشیر دو لبه','golden double edged sword on chart'),
    ('سشن لندن یا نیویورک؟','london new york night skyline trading'),
    ('پرایس اکشن یا اندیکاتور؟','candlestick chart versus indicators'),
    ('قانون ۲٪ مدیریت سرمایه','golden vault small coin dark'),
    ('لیکوییدیتی: شکارگاه پول هوشمند','golden waves around candlestick chart'),
    ('ریسک به ریوارد مهم‌تر از وین‌ریت','golden balance scale dark'),
    ('۵ اشتباه مرگبار تازه‌کارها','broken chess pieces trading desk'),
    ('صبر؛ سلاح حرفه‌ای‌ها','golden hourglass dark desk'),
    ('ترس و طمع: دو دشمن اصلی','fear greed masks dark desk'),
    ('چرا ۹۰٪ تریدرها ضرر می‌کنند؟','crowd walking off cliff one stands back')]
    f,e=random.choice(T)
    sysp='تو استودیو هوش فارکسین هستی؛ برند فارکسین ترک اصلانی؛ سبک LIT پول هوشمند؛ لحن حرفه‌ای صمیمی بدون وعدهٔ سود. خروجی فارسی با برچسب‌ها: [اینستا] هوک+کپشن+CTA+۸هشتگ  [یوتیوب] تایتل سئو+توضیح+۶تگ  [لینکدین] ۳خط حرفه‌ای  [تلگرام] پست+سوال تعاملی  [آموزش] یک توصیهٔ آموزشی کوتاه  [ریلز] ایدهٔ ۳صحنه. پایان: این توصیهٔ مالی نیست.'
    usr='موضوع: '+f+' | انس: '+str(ounce)
    ai=''
    try:
        dk=os.environ.get('DEEPSEEK_KEY','')
        if dk:
            q=json.dumps({'model':'deepseek-chat','messages':[{'role':'system','content':sysp},{'role':'user','content':usr}]}).encode()
            r=ur.urlopen(ur.Request('https://api.deepseek.com/chat/completions',data=q,headers={'Content-Type':'application/json','Authorization':'Bearer '+dk}),timeout=60).read().decode()
            ai=json.loads(r)['choices'][0]['message']['content']
    except Exception:pass
    if not ai:
        try:
            gh=os.environ.get('GH_PAT','')
            if gh:
                q=json.dumps({'model':'gpt-4o-mini','messages':[{'role':'system','content':sysp},{'role':'user','content':usr}],'temperature':0.8,'max_tokens':1800}).encode()
                r=ur.urlopen(ur.Request('https://models.inference.ai.azure.com/chat/completions',data=q,headers={'Content-Type':'application/json','Authorization':'Bearer '+gh}),timeout=60).read().decode()
                ai=json.loads(r)['choices'][0]['message']['content']
        except Exception:pass
    if not ai:
        try:
            q=json.dumps({'messages':[{'role':'system','content':sysp},{'role':'user','content':usr}],'model':'openai'}).encode()
            r=ur.urlopen(ur.Request('https://text.pollinations.ai/',data=q,headers={'Content-Type':'application/json'}),timeout=60).read().decode('utf-8','ignore')
            if len(r)>100 and 'error' not in r[:30].lower():ai=r
        except Exception:pass
    if not ai or '[اینستا]' not in ai:
        ai='[اینستا] 🔥 '+f+'\nاین اصل، تفاوت تریدر حرفه‌ای و آماتور است. تجربه‌ات را بنویس 👇\n#فارکس #ترید #مدیریت_سرمایه #LIT #فارکسین #پرایس_اکشن #طلا #روانشناسی_معاملات\n\n[یوتیوب] '+f+' | آموزش کاربردی فارکس\nدر این ویدیو «'+f+'» را ساده و عملی بررسی می‌کنیم.\n#فارکس #آموزش_فارکس #طلا #ترید #LIT #پرایس_اکشن\n\n[لینکدین] '+f+'؛ اصلی که حرفه‌ای‌های بازار فراموش نمی‌کنند. در معامله‌گری، بقا از سود مهم‌تر است. #Forex #SmartMoney #RiskManagement\n\n[تلگرام] 🔥 '+f+'\nشما این اصل را رعایت می‌کنید؟ در گروه بنویسید.\n\n[آموزش] امروز یک معاملهٔ تمرینی با رعایت کامل این اصل انجام بده و نتیجه را در ژورنال یادداشت کن.\n\n[ریلز] ۱) هوک روی چارت ۲) توضیح ۱۵ ثانیه‌ای ۳) CTA'
    img=None
    for u in ['https://image.pollinations.ai/prompt/'+up.quote(e+', 4k, no text'),'https://image.pollinations.ai/prompt/'+up.quote('luxury dark forex gold chart, no text')]:
        try:
            d=get(u,30)
            if len(d)>15000 and (d[:2]==b'\xff\xd8' or d[:4]==b'\x89PNG'):img=d;break
        except Exception:pass
    logo=None
    try:logo=get('https://mbms-1356.github.io/forexin-site-/logo.png',20)
    except Exception:pass
    from PIL import Image,ImageDraw,ImageFont,ImageOps
    im=None;img_sq=None
    if img:
        im=Image.open(io.BytesIO(img)).convert('RGBA')
        if logo:
            lg=Image.open(io.BytesIO(logo)).convert('RGBA')
            w=max(int(im.width*0.2),60);lg=lg.resize((w,int(w*lg.height/max(lg.width,1))))
            im.alpha_composite(lg,(im.width-w-15,im.height-lg.height-15))
        o=io.BytesIO();ImageOps.fit(im,(1080,1080)).convert('RGB').save(o,'JPEG',quality=88);img_sq=o.getvalue()
        o=io.BytesIO();ImageOps.fit(im,(720,900)).convert('RGB').save(o,'JPEG',quality=88);img_vert=o.getvalue()
    video=None
    if img:
        try:
            open('v.jpg','wb').write(img_vert)
            subprocess.run(['ffmpeg','-y','-loop','1','-i','v.jpg','-t','10','-vf','zoompan=z=min(zoom+0.0012,1.25):d=250:s=720x900:fps=25','-c:v','libx264','-pix_fmt','yuv420p','v.mp4'],timeout=180,check=True,capture_output=True)
            video=open('v.mp4','rb').read()
        except Exception:pass
    cardimg=None
    try:
        W,H=1080,1350
        cim=Image.new('RGB',(W,H),(18,18,24));dr=ImageDraw.Draw(cim)
        try:
            fd=get('https://cdn.jsdelivr.net/gh/rastikerdar/vazirmatn@v33.003/fonts/ttf/Vazirmatn-Bold.ttf',20)
            f1=ImageFont.truetype(io.BytesIO(fd),52);f2=ImageFont.truetype(io.BytesIO(fd),38)
        except Exception:
            f1=ImageFont.load_default();f2=f1
        dr.rectangle((40,40,W-40,H-40),outline=(212,175,55),width=6)
        dr.text((W//2,130),'FOREXIN SMART STUDIO',fill=(212,175,55),font=f1,anchor='mm')
        y=280
        for line in wrap('امروز: '+f,24):
            dr.text((W//2,y),line,fill=(255,255,255),font=f1,anchor='mm');y+=75
        y+=30;dr.line((90,y,W-90,y),fill=(212,175,55),width=3);y+=90
        for line in wrap(part(ai,'[آموزش]','[ریلز]') or 'مدیریت ریسک، اول از همه.',30):
            dr.text((W//2,y),line,fill=(230,230,230),font=f2,anchor='mm');y+=62
            if y>H-260:break
        if logo:
            lg=Image.open(io.BytesIO(logo)).convert('RGBA');lg=lg.resize((280,int(280*lg.height/max(lg.width,1))))
            cim.paste(lg,((W-lg.width)//2,H-lg.height-70),lg)
        o=io.BytesIO();cim.save(o,'JPEG',quality=88);cardimg=o.getvalue()
    except Exception:pass
    footer='\n\n━ ━ ━  ━ ━\n تتر: nobitex.ir/price/usdt\n🪙 طلای ۱۸: '+fa(g18)+' تومان/گرم | 🌍 انس: '+str(ounce)+' دلار\n\n🎓 یوتیوب: youtube.com/@Forexin.turkaslani\n📢 کانال: t.me/forexin_turkaslanifree\n🤖 ربات: t.me/TurkaslaniSiteBot\n🔥 استارت بزن، قیمت لحظه‌ای ببین!'
    head='📝 بستهٔ روز | استودیو هوش فارکسین\n🎯 '+f+'\n\n'
    if img_sq:send_file('/sendPhoto','photo','insta.jpg',img_sq,'image/jpeg',head+'📸 اینستاگرام:\n'+part(ai,'[اینستا]','[یوتیوب]'))
    if video:send_file('/sendVideo','video','reel.mp4',video,'video/mp4','🎬 ریلز آماده:\n'+part(ai,'[ریلز]',''))
    if img:send_file('/sendPhoto','photo','cover.jpg',img_vert,'image/jpeg','▶️ یوتیوب:\n'+part(ai,'[یوتیوب]','[لینکدین]')+'\n\n💼 لینکدین:\n'+part(ai,'[لینکدین','[تلگرام]'))
    if cardimg:send_file('/sendPhoto','photo','card.jpg',cardimg,'image/jpeg','💡 کارت آموزشی:\n'+part(ai,'[آموزش]','[ریلز]'))
    txt('📢 تلگرام:\n'+part(ai,'[تلگرام]','[آموزش]')+footer)
    print('OK')
except Exception:
    try:txt('🛠 DEBUG:\n'+traceback.format_exc()[-1200:])
    except Exception:print(traceback.format_exc())
