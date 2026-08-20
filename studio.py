import json,os,io,time,urllib.request as ur,random,traceback,subprocess
API='https://api.telegram.org/bot'+os.environ['TOKEN'];CHAT='227491135'
LOGO='https://mbms-1356.github.io/forexin-site-/logo.png'
VAULT='https://mbms-1356.github.io/forexin-site-/vault.json'
FONT='https://cdn.jsdelivr.net/gh/rastikerdar/vazirmatn@v33.003/fonts/ttf/Vazirmatn-Bold.ttf'
day=int(time.time()//86400)
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
    from PIL import Image,ImageDraw,ImageFont,ImageChops
    F=None;F2=None
    try:
        fd=get(FONT,20)
        F=ImageFont.truetype(io.BytesIO(fd),64);F2=ImageFont.truetype(io.BytesIO(fd),38)
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
    def putlogo(im,wrel,yoff):
        if logo:
            lw=max(int(im.width*wrel),70);l2=logo.resize((lw,lw))
            im.paste(l2,(im.width-lw-24,im.height-lw-yoff),l2)
    def chart(w,h,hook,sub,seed):
        im=Image.new('RGB',(w,h),(10,12,18));dr=ImageDraw.Draw(im)
        for x in range(0,w,90):dr.line((x,0,x,h),fill=(22,27,38),width=1)
        for y in range(0,h,90):dr.line((0,y,w,y),fill=(22,27,38),width=1)
        rnd=random.Random(seed)
        n=26;cw=(w-120)//n;x0=60;p=h*0.55;closes=[]
        for i in range(n):
            o=p;p=max(h*0.25,min(h*0.8,p+rnd.uniform(-h*0.06,h*0.062)))
            hi=min(o,p)-rnd.uniform(4,h*0.03);lo=max(o,p)+rnd.uniform(4,h*0.03)
            col=(46,200,110) if p<o else (230,70,70)
            cx=x0+i*cw+cw//2
            dr.line((cx,int(hi),cx,int(lo)),fill=col,width=3)
            bw=max(cw*0.55,6)
            dr.rectangle((cx-bw/2,min(o,p),cx+bw/2,max(o,p)),fill=col)
            closes.append(p)
        pts=[(x0+i*cw+cw//2,sum(closes[max(i-4,0):i+1])/len(closes[max(i-4,0):i+1])) for i in range(n)]
        dr.line(pts,fill=(255,200,60),width=4)
        lp=int(closes[-1])
        for x in range(0,w,24):dr.line((x,lp,x+12,lp),fill=(255,200,60),width=2)
        if F:
            y=100
            for line in wrap(hook,20):
                dr.text((w//2,y),line,font=F,fill=(255,205,70),stroke_width=4,stroke_fill=(0,0,0),anchor='mm');y+=90
        if F2 and sub:dr.text((w//2,h-150),sub,font=F2,fill=(235,235,235),stroke_width=3,stroke_fill=(0,0,0),anchor='mm')
        if F2:dr.text((30,h-70),'@Forexin.turkaslani',font=F2,fill=(255,200,60),anchor='lm')
        putlogo(im,0.16,40)
        return im
    def cta(w,h):
        im=Image.new('RGB',(w,h),(10,12,18));dr=ImageDraw.Draw(im)
        dr.rectangle((30,30,w-30,h-30),outline=(212,175,55),width=5)
        if logo:
            lw=int(w*0.4);l2=logo.resize((lw,lw));im.paste(l2,((w-lw)//2,h//2-lw//2-120),l2)
        if F:dr.text((w//2,h-260),'فالو کن: فارکسین',font=F,fill=(255,205,70),stroke_width=4,stroke_fill=(0,0,0),anchor='mm')
        if F2:dr.text((w//2,h-170),'یوتیوب: @Forexin.turkaslani',font=F2,fill=(235,235,235),anchor='mm')
        return im
    vault={'principles':[],'quotes':[],'hooks':[],'lit_facts':[]}
    try:vault.update(json.loads(get(VAULT,15)))
    except Exception:pass
    topic=random.choice(vault['principles'] or ['مدیریت سرمایه: اول بقا، بعد سود'])
    hookT=random.choice(vault['hooks'] or ['قبل از هر ترید این را ببین'])
    quote=random.choice(vault['quotes'] or ['اول بقا، بعد سود.'])
    facts=' '.join(vault['lit_facts'])
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
    sysp='تو استودیو هوش فارکسین هستی؛ برند فارکسین ترک اصلانی؛ متد LIT. دانش برند: '+facts+' لحن حرفه‌ای صمیمی بدون وعدهٔ سود. هوک‌ها کنجکاوی/ترس از دست دادن بسازند و عدد/زمان داشته باشند. خروجی فارسی با برچسب‌ها: [اینستا] هوک+کپشن ۳خط+CTA+۸هشتگ  [یوتیوب] تایتل سئو+توضیح+۶تگ  [لینکدین] ۳خط  [تلگرام] پست+سوال  [آموزش] توصیه کوتاه  [ریلز] ۳صحنه با دیالوگ. پایان: این توصیهٔ مالی نیست.'
    usr='موضوع: '+topic+' | انس: '+str(ounce)+' | ترندهای جهانی: '+trends
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
        ai='[اینستا] 🔥 '+hookT+'\n'+topic+'؛ اصلی که ۹۰٪ نادیده می‌گیرند و همان ۹۰٪ ضرر می‌کنند.\n'+quote+' تجربه‌ات را بنویس 👇\n#فارکس #ترید #مدیریت_سرمایه #LIT #فارکسین #پرایس_اکشن #طلا #روانشناسی_معاملات\n\n[یوتیوب] '+topic+' | آموزش کاربردی فارکس\nدر این ویدیو «'+topic+'» را ساده و عملی با متد LIT بررسی می‌کنیم.\n#فارکس #آموزش_فارکس #طلا #ترید #LIT #پرایس_اکشن\n\n[لینکدین] '+topic+'؛ اصلی که حرفه‌ای‌های بازار فراموش نمی‌کنند. بقا از سود مهم‌تر است. #Forex #SmartMoney #RiskManagement\n\n[تلگرام] 🔥 '+topic+'\nشما این اصل را رعایت می‌کنید؟ در گروه بنویسید.\n\n[آموزش] امروز یک معاملهٔ تمرینی با رعایت کامل این اصل انجام بده و نتیجه را در ژورنال یادداشت کن.\n\n[ریلز] صحنه۱: «'+hookT+'» صحنه۲: توضیح روی چارت صحنه۳: «فالو کن: فارکسین»'
    video=None
    try:
        scenes=[chart(720,900,hookT,'',day+1),chart(720,900,topic,'راه‌حل: متد LIT',day+2),cta(720,900)]
        for i,im in enumerate(scenes):
            o=io.BytesIO();im.convert('RGB').save(o,'JPEG',quality=86);open('s%d.jpg'%i,'wb').write(o.getvalue())
            subprocess.run(['ffmpeg','-y','-loop','1','-i','s%d.jpg'%i,'-t','4','-vf','zoompan=z=min(zoom+0.002,1.3):d=100:s=720x900:fps=25','-c:v','libx264','-pix_fmt','yuv420p','s%d.mp4'%i],timeout=120,check=True,capture_output=True)
        open('list.txt','w').write("file 's0.mp4'\nfile 's1.mp4'\nfile 's2.mp4'\n")
        subprocess.run(['ffmpeg','-y','-f','concat','-safe','0','-i','list.txt','-c','copy','reel.mp4'],timeout=120,check=True,capture_output=True)
        video=open('reel.mp4','rb').read()
    except Exception as ex:
        print('video fail',ex)
    o=io.BytesIO();chart(1080,1080,hookT,topic,day).convert('RGB').save(o,'JPEG',quality=88);cover=o.getvalue()
    o=io.BytesIO();chart(1080,608,'▶ '+topic,'',day+3).convert('RGB').save(o,'JPEG',quality=88);wide=o.getvalue()
    cardimg=None
    try:
        W,H=1080,1350
        cim=Image.new('RGB',(W,H),(18,18,24));dr=ImageDraw.Draw(cim)
        dr.rectangle((40,40,W-40,H-40),outline=(212,175,55),width=6)
        dr.text((W//2,130),'FOREXIN SMART STUDIO',fill=(212,175,55),font=F,anchor='mm')
        y=300
        for line in wrap('امروز: '+topic,22):
            dr.text((W//2,y),line,fill=(255,255,255),font=F2,anchor='mm');y+=60
        y+=40;dr.line((90,y,W-90,y),fill=(212,175,55),width=3);y+=90
        for line in wrap(part(ai,'[آموزش]','[ریلز]') or quote,28):
            dr.text((W//2,y),line,fill=(230,230,230),font=F2,anchor='mm');y+=58
            if y>H-260:break
        if logo:
            l3=logo.resize((280,280));cim.paste(l3,((W-280)//2,H-350),l3)
        o=io.BytesIO();cim.save(o,'JPEG',quality=88);cardimg=o.getvalue()
    except Exception:pass
    footer='\n\n━ ━ ━  ━ ━\n تتر: nobitex.ir/price/usdt\n🪙 طلای ۱۸: '+fa(g18)+' تومان/گرم | 🌍 انس: '+str(ounce)+' دلار\n\n🎓 یوتیوب: youtube.com/@Forexin.turkaslani\n📢 کانال: t.me/forexin_turkaslanifree\n🤖 ربات: t.me/TurkaslaniSiteBot\n🔥 استارت بزن، قیمت لحظه‌ای ببین!'
    head='📝 بسته روز | استودیو هوش فارکسین\n🎯 '+topic+'\n\n'
    send_file('/sendPhoto','photo','insta.jpg',cover,'image/jpeg',head+'📸 اینستاگرام:\n'+part(ai,'[اینستا]','[یوتیوب]'))
    if video:send_file('/sendVideo','video','reel.mp4',video,'video/mp4','🎬 ریلز ۳صحنه‌ای:\n'+part(ai,'[ریلز]',''))
    send_file('/sendPhoto','photo','cover.jpg',wide,'image/jpeg','▶️ یوتیوب:\n'+part(ai,'[یوتیوب]','[لینکدین]')+'\n\n💼 لینکدین:\n'+part(ai,'[لینکدین','[تلگرام]'))
    if cardimg:send_file('/sendPhoto','photo','card.jpg',cardimg,'image/jpeg','💡 کارت آموزشی:\n'+part(ai,'[آموزش]','[ریلز]'))
    txt('📢 تلگرام:\n'+part(ai,'[تلگرام]','[آموزش]')+'\n\n🦁 '+quote+footer)
    print('OK')
except Exception:
    try:txt('🛠 DEBUG:\n'+traceback.format_exc()[-1200:])
    except Exception:print(traceback.format_exc())
