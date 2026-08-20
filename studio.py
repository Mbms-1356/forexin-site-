import json,os,io,urllib.request as ur,urllib.parse as up,random,traceback,subprocess
API='https://api.telegram.org/bot'+os.environ['TOKEN'];CHAT='227491135'
LOGO='https://mbms-1356.github.io/forexin-site-/logo.png'
FONT='https://cdn.jsdelivr.net/gh/rastikerdar/vazirmatn@v33.003/fonts/ttf/Vazirmatn-Bold.ttf'
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
    from PIL import Image,ImageDraw,ImageFont,ImageOps,ImageChops
    F=None
    try:F=ImageFont.truetype(io.BytesIO(get(FONT,20)),64)
    except Exception:pass
    F2=None
    try:F2=ImageFont.truetype(io.BytesIO(get(FONT,20)),40)
    except Exception:pass
    logo=None
    try:
        lg=Image.open(io.BytesIO(get(LOGO,20))).convert('RGBA')
        px=lg.load()
        for y in range(lg.height):
            for x in range(lg.width):
                r,g,b,a=px[x,y]
                if r>225 and g>225 and b>225:px[x,y]=(255,255,255,0)
        m=Image.new('L',lg.size,0);ImageDraw.Draw(m).ellipse((0,0,lg.width,lg.height),fill=255)
        lg.putalpha(ImageChops.multiply(lg.split()[3],m))
        logo=lg
    except Exception:pass
    def stamp(im,hook):
        if logo:
            w=max(int(im.width*0.18),60);l2=logo.resize((w,w))
            im.alpha_composite(l2.convert('RGBA'),(im.width-w-20,im.height-w-20))
        if F:
            dr=ImageDraw.Draw(im)
            y=110
            for line in wrap(hook,22):
                dr.text((im.width//2,y),line,font=F,fill=(255,200,60),stroke_width=4,stroke_fill=(0,0,0),anchor='mm')
                y+=95
        return im
    usdt=0;ounce=0.0
    try:usdt=int(json.loads(get('https://mbms-1356.github.io/forexin-site-/price.json',10)).get('usdt',0))
    except Exception:pass
    try:ounce=float(json.loads(get('https://api.gold-api.com/price/XAU',10)).get('price',0))
    except Exception:pass
    g18=int(usdt*ounce/31.1035*0.75) if usdt and ounce else 0
    trends=''
    try:
        rj=json.loads(get('https://www.reddit.com/r/Forex/hot.json?limit=5',15))
        trends=' | '.join([c['data']['title'][:60] for c in rj['data']['children']])
    except Exception:pass
    T=[('روانشناسی معاملات: احساسات دشمن تریدر','trader emotions dark desk cinematic candlestick chart background'),
    ('استاپ‌لاس: بیمهٔ حرفه‌ای‌ها','golden shield over candlestick trading chart, dark'),
    ('اهرم؛ شمشیر دو لبه','golden double edged sword over trading chart candles'),
    ('سشن لندن یا نیویورک؟','london new york skyline night with candlestick chart overlay'),
    ('پرایس اکشن یا اندیکاتور؟','naked candlestick chart versus messy indicators screen'),
    ('قانون ۲٪ مدیریت سرمایه','golden vault and small coin on trading chart background'),
    ('لیکوییدیتی: شکارگاه پول هوشمند','golden liquid waves over candlestick chart, smart money'),
    ('ریسک به ریوارد مهم‌تر از وین‌ریت','golden balance scale over dark trading chart'),
    ('۵ اشتباه مرگبار تازه‌کارها','broken chess pieces on trading desk with chart screens'),
    ('صبر؛ سلاح حرفه‌ای‌ها','golden hourglass on trading desk, chart glow'),
    ('ترس و طمع: دو دشمن اصلی','fear greed masks on trading desk, dark chart'),
    ('چرا ۹۰٪ تریدرها ضرر می‌کنند؟','crowd walking off cliff edge, one trader stands back, dark')]
    f,e=random.choice(T)
    sysp='تو استودیو هوش فارکسین هستی؛ برند فارکسین ترک اصلانی؛ سبک LIT پول هوشمند؛ لحن حرفه‌ای صمیمی بدون وعدهٔ سود. هوک‌ها باید کنجکاوی یا ترس از دست دادن بسازند و عدد/زمان داشته باشند. خروجی فارسی با برچسب‌ها: [اینستا] هوک قوی+کپشن ۳خط+CTA+۸هشتگ  [یوتیوب] تایتل سئو+توضیح+۶تگ  [لینکدین] ۳خط  [تلگرام] پست+سوال  [آموزش] توصیه کوتاه  [ریلز] ۳صحنه با دیالوگ. پایان: این توصیهٔ مالی نیست.'
    usr='موضوع: '+f+' | انس: '+str(ounce)+' | ترندهای جهانی: '+trends
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
                q=json.dumps({'model':'gpt-4o-mini','messages':[{'role':'system','content':sysp},{'role':'user','content':usr}],'temperature':0.9,'max_tokens':2200}).encode()
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
        ai='[اینستا] 🔥 '+f+'\n۹۰٪ تریدرها این را نادیده می‌گیرند و همان ۹۰٪ ضرر می‌کنند.\nاین اصل، تفاوت حرفه‌ای و آماتور است؛ تجربه‌ات را بنویس 👇\n#فارکس #ترید #مدیریت_سرمایه #LIT #فارکسین #پرایس_اکشن #طلا #روانشناسی_معاملات\n\n[یوتیوب] '+f+' | آموزش کاربردی فارکس\nدر این ویدیو «'+f+'» را ساده و عملی بررسی می‌کنیم.\n#فارکس #آموزش_فارکس #طلا #ترید #LIT #پرایس_اکشن\n\n[لینکدین] '+f+'؛ اصلی که حرفه‌ای‌های بازار فراموش نمی‌کنند. بقا از سود مهم‌تر است. #Forex #SmartMoney #RiskManagement\n\n[تلگرام] 🔥 '+f+'\nشما این اصل را رعایت می‌کنید؟ در گروه بنویسید.\n\n[آموزش] امروز یک معاملهٔ تمرینی با رعایت کامل این اصل انجام بده و نتیجه را در ژورنال یادداشت کن.\n\n[ریلز] صحنه۱: «۹۰٪ ضرر می‌کنند چون...» صحنه۲: توضیح روی چارت صحنه۳: «فالو کن: فارکسین»'
    hook=(part(ai,'[اینستا]','[یوتیوب]').split('\n')[0] or f)[:60]
    imgs={}
    for k,u in [('sq','https://image.pollinations.ai/prompt/'+up.quote(e+', 4k, cinematic, no text')),
    ('v1','https://image.pollinations.ai/prompt/'+up.quote('closeup dramatic face of trader, '+e+', cinematic, no text')),
    ('v2','https://image.pollinations.ai/prompt/'+up.quote('candlestick trading chart glowing, '+e+', cinematic, no text')),
    ('v3','https://image.pollinations.ai/prompt/'+up.quote('victorious trader silhouette in golden light, cinematic, no text'))]:
        try:
            d=get(u,30)
            if len(d)>15000 and (d[:2]==b'\xff\xd8' or d[:4]==b'\x89PNG'):imgs[k]=d
        except Exception:pass
    img_sq=None;im0=None
    if 'sq' in imgs:
        im0=Image.open(io.BytesIO(imgs['sq'])).convert('RGBA')
        im0=stamp(ImageOps.fit(im0,(1080,1080)),f)
        o=io.BytesIO();im0.convert('RGB').save(o,'JPEG',quality=88);img_sq=o.getvalue()
    video=None
    if 'v1' in imgs and 'v2' in imgs and 'v3' in imgs:
        try:
            scenes=[('v1','۹۰٪ این‌جا ضرر می‌کنند!'),('v2',f),('v3','فالو کن: فارکسین 🦁')]
            for i,(k,cap) in enumerate(scenes):
                im=stamp(ImageOps.fit(Image.open(io.BytesIO(imgs[k])).convert('RGBA'),(720,900)),cap)
                o=io.BytesIO();im.convert('RGB').save(o,'JPEG',quality=86);open('s%d.jpg'%i,'wb').write(o.getvalue())
                subprocess.run(['ffmpeg','-y','-loop','1','-i','s%d.jpg'%i,'-t','4','-vf','zoompan=z=min(zoom+0.002,1.3):d=100:s=720x900:fps=25','-c:v','libx264','-pix_fmt','yuv420p','s%d.mp4'%i],timeout=120,check=True,capture_output=True)
            open('list.txt','w').write("file 's0.mp4'\nfile 's1.mp4'\nfile 's2.mp4'\n")
            subprocess.run(['ffmpeg','-y','-f','concat','-safe','0','-i','list.txt','-c','copy','reel.mp4'],timeout=120,check=True,capture_output=True)
            video=open('reel.mp4','rb').read()
        except Exception as ex:
            print('video fail',ex)
    cardimg=None
    try:
        W,H=1080,1350
        cim=Image.new('RGB',(W,H),(18,18,24));dr=ImageDraw.Draw(cim)
        dr.rectangle((40,40,W-40,H-40),outline=(212,175,55),width=6)
        dr.text((W//2,130),'FOREXIN SMART STUDIO',fill=(212,175,55),font=F,anchor='mm')
        y=300
        for line in wrap('امروز: '+f,22):
            dr.text((W//2,y),line,fill=(255,255,255),font=F2,anchor='mm');y+=65
        y+=40;dr.line((90,y,W-90,y),fill=(212,175,55),width=3);y+=90
        for line in wrap(part(ai,'[آموزش]','[ریلز]') or 'مدیریت ریسک، اول از همه.',28):
            dr.text((W//2,y),line,fill=(230,230,230),font=F2,anchor='mm');y+=60
            if y>H-260:break
        if logo:
            l3=logo.resize((280,280))
            cim.paste(l3,((W-280)//2,H-350),l3)
        o=io.BytesIO();cim.save(o,'JPEG',quality=88);cardimg=o.getvalue()
    except Exception:pass
    footer='\n\n━ ━ ━  ━ ━\n💹 تتر: nobitex.ir/price/usdt\n🪙 طلای ۱۸: '+fa(g18)+' تومان/گرم | 🌍 انس: '+str(ounce)+' دلار\n\n🎓 یوتیوب: youtube.com/@Forexin.turkaslani\n📢 کانال: t.me/forexin_turkaslanifree\n🤖 ربات: t.me/TurkaslaniSiteBot\n🔥 استارت بزن، قیمت لحظه‌ای ببین!'
    head='📝 بستهٔ روز | استودیو هوش فارکسین\n🎯 '+f+'\n\n'
    if img_sq:send_file('/sendPhoto','photo','insta.jpg',img_sq,'image/jpeg',head+'📸 اینستاگرام:\n'+part(ai,'[اینستا]','[یوتیوب]'))
    if video:send_file('/sendVideo','video','reel.mp4',video,'video/mp4','🎬 ریلز ۳صحنه‌ای آماده:\n'+part(ai,'[ریلز]',''))
    if 'v2' in imgs:
        imv=stamp(ImageOps.fit(Image.open(io.BytesIO(imgs['v2'])).convert('RGBA'),(1080,608)),'▶ '+f)
        o=io.BytesIO();imv.convert('RGB').save(o,'JPEG',quality=88)
        send_file('/sendPhoto','photo','cover.jpg',o.getvalue(),'image/jpeg','▶️ یوتیوب:\n'+part(ai,'[یوتیوب]','[لینکدین]')+'\n\n💼 لینکدین:\n'+part(ai,'[لینکدین','[تلگرام]'))
    if cardimg:send_file('/sendPhoto','photo','card.jpg',cardimg,'image/jpeg','💡 کارت آموزشی:\n'+part(ai,'[آموزش]','[ریلز]'))
    txt('📢 تلگرام:\n'+part(ai,'[تلگرام]','[آموزش]')+footer)
    print('OK')
except Exception:
    try:txt('🛠 DEBUG:\n'+traceback.format_exc()[-1200:])
    except Exception:print(traceback.format_exc())
