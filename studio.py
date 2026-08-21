import json,os,io,time,urllib.request as ur,urllib.parse as up,random,traceback,subprocess,base64
API='https://api.telegram.org/bot'+os.environ['TOKEN'];CHAT='227491135'
LOGO='https://mbms-1356.github.io/forexin-site-/logo.png'
VAULT='https://mbms-1356.github.io/forexin-site-/vault.json'
FONT='https://cdn.jsdelivr.net/gh/rastikerdar/vazirmatn@v33.003/fonts/ttf/Vazirmatn-Bold.ttf'
PAT=os.environ.get('GH_PAT','');OR=os.environ.get('OPENROUTER_KEY','');GK=os.environ.get('GROQ_KEY','')
CUSTOM=os.environ.get('CUSTOM','')
LINKS='\n🔗 لینک‌ها: nobitex.ir/price/usdt | t.me/forexin_turkaslanifree | youtube.com/@Forexin.turkaslani'
seed=int(time.time())%100000
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
        if len(cur)+len(w)+1>n:
            if cur:out.append(cur)
            cur=w
        else:cur=(cur+' '+w).strip()
    if cur:out.append(cur)
    return out
def short(t,k=6):
    ws=t.split(' ')
    return ' '.join(ws[:k])+('…' if len(ws)>k else '')
def send_file(path,ff,fname,fdata,fctype,caption):
    b='----fxB';body=b''
    body+=('--'+b+'\r\n').encode()+b'Content-Disposition: form-data; name="chat_id"\r\n\r\n'+CHAT.encode()+b'\r\n'
    if caption:
        body+=('--'+b+'\r\n').encode()+b'Content-Disposition: form-data; name="caption"\r\n\r\n'+caption[:1024].encode()+b'\r\n'
    body+=('--'+b+'\r\n').encode()+('Content-Disposition: form-data; name="%s"; filename="%s"\r\nContent-Type: %s\r\n\r\n'%(ff,fname,fctype)).encode()+fdata+('\r\n--'+b+'--\r\n').encode()
    post(path,body,'multipart/form-data; boundary='+b)
def commit_site(path,content):
    try:
        body={'message':'update '+path,'content':base64.b64encode(content.encode()).decode()}
        try:
            old=json.loads(get('https://api.github.com/repos/Mbms-1356/forexin-site-/contents/'+path,15))
            body['sha']=old.get('sha')
        except Exception:pass
        ur.urlopen(ur.Request('https://api.github.com/repos/Mbms-1356/forexin-site-/contents/'+path,data=json.dumps(body).encode(),headers={'Authorization':'token '+PAT,'User-Agent':'studio','Accept':'application/vnd.github+json'},method='PUT'),timeout=30).read()
    except Exception:pass
models=[]
if OR:
    try:
        ml=json.loads(get('https://openrouter.ai/api/v1/models',20))
        free=[m.get('id','') for m in ml.get('data',[]) if m.get('pricing',{}).get('prompt')=='0' and m.get('pricing',{}).get('completion')=='0']
        pref=[m for m in free if any(k in m.lower() for k in ['qwen','llama','mistral','deepseek','gemini','alpha'])]
        models=(pref or free)[:3]
    except Exception:pass
def ask(s,u):
    for m in models:
        try:
            r=ur.urlopen(ur.Request('https://openrouter.ai/api/v1/chat/completions',data=json.dumps({'model':m,'messages':[{'role':'system','content':s},{'role':'user','content':u}],'temperature':0.9,'max_tokens':1600}).encode(),headers={'Content-Type':'application/json','Authorization':'Bearer '+OR,'User-Agent':'forexin'}),timeout=60).read().decode()
            c=json.loads(r)['choices'][0]['message']['content']
            if c:return c
        except Exception:pass
    if GK:
        try:
            r=ur.urlopen(ur.Request('https://api.groq.com/openai/v1/chat/completions',data=json.dumps({'model':'llama-3.3-70b-versatile','messages':[{'role':'system','content':s},{'role':'user','content':u}],'temperature':0.9,'max_tokens':1600}).encode(),headers={'Content-Type':'application/json','Authorization':'Bearer '+GK}),timeout=60).read().decode()
            c=json.loads(r)['choices'][0]['message']['content']
            if c:return c
        except Exception:pass
    return ''
def R(name,train,task):
    return 'تو '+name+' هستی.\nآموزش: '+train+'\nوظیفهٔ تو حالا: '+task
try:
    from PIL import Image,ImageDraw,ImageFont,ImageChops
    F=None;F2=None;F3=None
    try:
        fd=get(FONT,20)
        F=ImageFont.truetype(io.BytesIO(fd),58);F2=ImageFont.truetype(io.BytesIO(fd),38);F3=ImageFont.truetype(io.BytesIO(fd),30)
    except Exception:pass
    logo=None
    try:
        lg=Image.open(io.BytesIO(get(LOGO,20))).convert('RGB')
        for c in [(0,0),(lg.width-1,0),(0,lg.height-1),(lg.width-1,lg.height-1),(lg.width//2,0),(0,lg.height//2),(lg.width-1,lg.height//2),(lg.width//2,lg.height-1)]:
            try:ImageDraw.floodfill(lg,c,(255,0,255),thresh=80)
            except Exception:pass
        lg=lg.convert('RGBA')
        px=lg.load()
        for y in range(lg.height):
            for x in range(lg.width):
                r,g,b,a=px[x,y]
                if r>200 and g<120 and b>200:px[x,y]=(r,g,b,0)
        bb=lg.getbbox()
        if bb:lg=lg.crop(bb)
        logo=lg
    except Exception:pass
    def lres(w):
        ratio=logo.height/max(logo.width,1)
        return logo.resize((w,int(w*ratio)))
    def putlogo(im,wrel,yoff):
        if logo:
            lw=max(int(im.width*wrel),70);l2=lres(lw)
            im.paste(l2,(im.width-l2.width-24,im.height-l2.height-yoff),l2)
    def overlay(im,hook,sub):
        dr=ImageDraw.Draw(im)
        if F:
            y=110
            for line in wrap(hook,18):
                dr.text((im.width//2,y),line,font=F,fill=(255,205,70),stroke_width=5,stroke_fill=(0,0,0),anchor='mm');y+=85
        if F3 and sub:dr.text((im.width//2,im.height-160),sub,font=F3,fill=(255,255,255),stroke_width=3,stroke_fill=(0,0,0),anchor='mm')
        if F3:dr.text((30,im.height-60),'@Forexin.turkaslani',font=F3,fill=(255,200,60),anchor='lm')
        putlogo(im,0.15,30)
        return im
    def gen_img(prompt,w,h,sd):
        try:
            u='https://image.pollinations.ai/prompt/'+up.quote(prompt+', dark cinematic golden, no text')+'?width=%d&height=%d&nologo=true&seed=%d'%(w,h,sd)
            d=get(u,40)
            if len(d)>15000 and (d[:2]==b'\xff\xd8' or d[:4]==b'\x89PNG'):
                return Image.open(io.BytesIO(d)).convert('RGBA')
        except Exception:pass
        return None
    def chart(w,h,hook,sub,sd,style=0):
        im=Image.new('RGBA',(w,h),(10,12,18,255));dr=ImageDraw.Draw(im)
        for x in range(0,w,90):dr.line((x,0,x,h),fill=(22,27,38,255),width=1)
        for y in range(0,h,90):dr.line((0,y,w,y),fill=(22,27,38,255),width=1)
        rnd=random.Random(sd)
        n=26;cw=(w-120)//n;x0=60;p=h*0.55;closes=[]
        for i in range(n):
            o=p;p=max(h*0.25,min(h*0.8,p+rnd.uniform(-h*0.06,h*0.062)))
            closes.append((o,p))
        pts=[(x0+i*cw+cw//2,int(c[1])) for i,c in enumerate(closes)]
        if style==1:
            acc=(64,200,255)
            for x,y in pts:dr.line((x,y,x,h),fill=(acc[0],acc[1],acc[2],26),width=max(cw//2,4))
            dr.line(pts,fill=acc,width=5)
        elif style==2:
            for i,(o,p) in enumerate(closes):
                cx=x0+i*cw+cw//2
                col=(46,200,110,255) if p<o else (230,70,70,255)
                bw=max(cw*0.55,6)
                dr.rectangle((cx-bw/2,min(o,p),cx+bw/2,max(o,p)),fill=col)
            dr.line(pts,fill=(255,200,60,255),width=3)
        else:
            for i,(o,p) in enumerate(closes):
                cx=x0+i*cw+cw//2
                hi=min(o,p)-rnd.uniform(4,h*0.03);lo=max(o,p)+rnd.uniform(4,h*0.03)
                col=(46,200,110,255) if p<o else (230,70,70,255)
                dr.line((cx,int(hi),cx,int(lo)),fill=col,width=3)
                bw=max(cw*0.55,6)
                dr.rectangle((cx-bw/2,min(o,p),cx+bw/2,max(o,p)),fill=col)
            dr.line(pts,fill=(255,200,60,255),width=4)
        lp=int(closes[-1][1])
        for x in range(0,w,24):dr.line((x,lp,x+12,lp),fill=(255,200,60,255),width=2)
        return overlay(im,hook,sub)
    def cta(w,h):
        im=Image.new('RGB',(w,h),(10,12,18));dr=ImageDraw.Draw(im)
        dr.rectangle((30,30,w-30,h-30),outline=(212,175,55),width=5)
        if logo:
            l2=lres(int(w*0.35));im.paste(l2,((w-l2.width)//2,180),l2)
        if F:dr.text((w//2,h//2+80),'به ما بپیوندید',font=F,fill=(255,205,70),stroke_width=4,stroke_fill=(0,0,0),anchor='mm')
        if F2:
            dr.text((w//2,h//2+170),'خانوادهٔ فارکسین ترک اصلانی',font=F2,fill=(235,235,235),anchor='mm')
            dr.text((w//2,h//2+230),'t.me/forexin_turkaslanifree',font=F2,fill=(120,200,255),anchor='mm')
            dr.text((w//2,h-120),'یوتیوب: @Forexin.turkaslani',font=F2,fill=(235,235,235),anchor='mm')
        return im
    vault={'principles':[],'quotes':[],'hooks':[],'lit_facts':[]}
    try:vault.update(json.loads(get(VAULT,15)))
    except Exception:pass
    notes=''
    try:notes=get('https://mbms-1356.github.io/forexin-site-/notes.txt',15)[:3000]
    except Exception:pass
    used=[]
    try:used=json.loads(get('https://mbms-1356.github.io/forexin-site-/used.json',15))
    except Exception:pass
    custom_topic='';custom_text='';custom_img=''
    if CUSTOM:
        try:
            cj=json.loads(CUSTOM)
            custom_topic=cj.get('topic','') or ''
            custom_text=cj.get('text','') or ''
            custom_img=cj.get('img','') or ''
        except Exception:custom_topic=CUSTOM
    pool=[p for p in vault['principles'] if p not in used] or vault['principles'] or ['مدیریت سرمایه: اول بقا، بعد سود']
    topic=custom_topic or random.choice(pool)
    if not custom_topic:
        used.append(topic);used=used[-30:]
        commit_site('used.json',json.dumps(used,ensure_ascii=False))
    hookT=random.choice(vault['hooks'] or ['قبل از هر ترید این را ببین'])
    quote=random.choice(vault['quotes'] or ['اول بقا، بعد سود.'])
    facts=' '.join(vault['lit_facts'])+' '+notes
    usdt=0;ounce=0.0
    try:usdt=int(json.loads(get('https://mbms-1356.github.io/forexin-site-/price.json',10)).get('usdt',0))
    except Exception:pass
    try:ounce=float(json.loads(get('https://api.gold-api.com/price/XAU',10)).get('price',0))
    except Exception:pass
    g18=int(usdt*ounce/31.1035*0.75) if usdt and ounce else 0
    TRAIN='دانش برند: '+facts+' | لحن: حرفه‌ای، صمیمی، مطمئن، انسانی و احساسی، بدون وعدهٔ سود.'
    IMGTRAIN='تصاویر: dark cinematic gold، مرتبط با فارکس/چارت، بدون متن، هر سه متمایز.'
    # نقش۱ تحلیلگر
    an=ask(R('تحلیلگر ارشد بازار فارکسین',TRAIN,'[تحلیل] ۲خط، [زاویه] داستانی احساسی، [هدف] مخاطب و درد او بنویس.'),'موضوع: '+topic+' | انس: '+str(ounce))
    analysis=part(an,'[تحلیل]','[زاویه]') or topic
    angle=part(an,'[زاویه]','[هدف]');target=part(an,'[هدف]','')
    # نقش۲ کارگردان هنری
    ar=ask(R('کارگردان هنری استودیو فارکسین',TRAIN+' | '+IMGTRAIN,'سه پرامپت تصویر انگلیسی متمایز با | جدا: (۱) نمای نزدیک چارت کندلی (۲) میز تریدر با مانیتور (۳) نماد گاو/خرس.'),'موضوع: '+topic+' | تحلیل: '+analysis)
    tpl=['closeup of golden candlestick trading chart on dark screen','professional trader desk with glowing monitors showing charts','golden bull and bear statues facing each other, dark cinematic']
    img0=[x.strip() for x in part(ar,'[imgs]','').split('|') if x.strip()]
    img0=[(img0[i] if i<len(img0) else tpl[i]) for i in range(3)]
    # نقش۳ کپی‌رایتر
    cp=ask(R('کپی‌رایتر ارشد فارکسین',TRAIN,'بخش‌های [اینستا][یوتیوب][لینکدین][تلگرام][آموزش][ریلز] را با هوک عدددار، سئو و لینک بنویس.'),'موضوع: '+topic+' | تحلیل: '+analysis+' | زاویه: '+angle+' | هدف: '+target+' | انس: '+str(ounce))
    # نقش۴ نگهبان QC: متن + تصویر
    gd=ask(R('نگهبان کیفیت (QC) فارکسین','متن: انسانی/احساسی/بدون جملهٔ تکراری/لحن برند. تصویر: مرتبط با موضوع، متمایز از هم، شامل چارت/عنصر فارکس، dark cinematic gold.','هر دو ورودی را تحلیل و اصلاح کن. خروجی: [imgs] سه پرامپت تصویر نهایی با | جدا، سپس بخش‌های متن نهایی [اینستا] تا [ریلز]. پایان: این توصیهٔ مالی نیست.'),'پرامپت‌های تصویر: '+' | '.join(img0)+'\nپیش‌نویس متن:\n'+cp)
    ai=gd if (gd and '[اینستا]' in gd) else cp
    if not ai or '[اینستا]' not in ai:
        ai='[اینستا] 🔥 '+hookT+'\n'+topic+'؛ اصلی که ۹۰٪ نادیده می‌گیرند.\n'+quote+' تجربه‌ات را بنویس 👇'+LINKS+'\n#فارکس #ترید #مدیریت_سرمایه #LIT #فارکسین #پرایس_اکشن #طلا #روانشناسی_معاملات\n\n[یوتیوب] '+topic+' | آموزش کاربردی فارکس'+LINKS+'\n#فارکس #آموزش_فارکس #طلا #ترید #LIT #پرایس_اکشن\n\n[لینکدین] '+topic+'؛ اصلی که حرفه‌ای‌ها فراموش نمی‌کنند. #Forex #SmartMoney\n\n[تلگرام] 🔥 '+topic+'\nشما رعایت می‌کنید؟ بنویسید.\n\n[آموزش] یک معاملهٔ تمرینی با این اصل بزن و یادداشت کن.\n\n[ریلز] صحنه۱ هوک صحنه۲ توضیح صحنه۳ دعوت'
    imglist=[x.strip() for x in part(ai,'[imgs]','[اینستا]').split('|') if x.strip()]
    imglist=[(imglist[i] if i<len(imglist) else img0[i]) for i in range(3)]
    cover=None
    if custom_img:
        try:
            d=get(custom_img,30)
            if len(d)>10000:cover=overlay(Image.open(io.BytesIO(d)).convert('RGBA'),short(topic,7),topic)
        except Exception:pass
    if cover is None:
        g=gen_img(imglist[0],1080,1080,seed)
        cover=overlay(g,short(topic,7),topic) if g else chart(1080,1080,short(topic,7),topic,seed,0)
    o=io.BytesIO();cover.convert('RGB').save(o,'JPEG',quality=88);cover_b=o.getvalue()
    o=io.BytesIO();Image.open(io.BytesIO(cover_b)).convert('RGB').resize((1080,608)).save(o,'JPEG',quality=88);wide_b=o.getvalue()
    g1=gen_img(imglist[1],720,900,seed+11)
    r1=overlay(g1,short(hookT,5),'') if g1 else chart(720,900,short(hookT,5),'',seed+11,1)
    g2=gen_img(imglist[2],720,900,seed+7)
    r2=overlay(g2,short(topic,6),'راه‌حل: متد LIT') if g2 else chart(720,900,short(topic,6),'راه‌حل: متد LIT',seed+7,2)
    video=None;verr=''
    try:
        scenes=[r1,r2,cta(720,900)]
        ok=True
        for i,im in enumerate(scenes):
            o=io.BytesIO();im.convert('RGB').save(o,'JPEG',quality=86);open('s%d.jpg'%i,'wb').write(o.getvalue())
            p=subprocess.run(['ffmpeg','-y','-loop','1','-i','s%d.jpg'%i,'-t','4','-vf','scale=720:900,fps=25','-c:v','libx264','-pix_fmt','yuv420p','s%d.mp4'%i],timeout=120,capture_output=True)
            if p.returncode!=0:ok=False;verr=p.stderr.decode()[-150:];break
        if ok:
            open('list.txt','w').write("file 's0.mp4'\nfile 's1.mp4'\nfile 's2.mp4'\n")
            p=subprocess.run(['ffmpeg','-y','-f','concat','-safe','0','-i','list.txt','-c','copy','reel.mp4'],timeout=120,capture_output=True)
            if p.returncode==0:video=open('reel.mp4','rb').read()
            else:verr=p.stderr.decode()[-150:]
        if not video:
            p=subprocess.run(['ffmpeg','-y','-loop','1','-i','s0.jpg','-t','5','-vf','scale=720:900,fps=25','-c:v','libx264','-pix_fmt','yuv420p','reel.mp4'],timeout=120,capture_output=True)
            if p.returncode==0:video=open('reel.mp4','rb').read()
            else:verr=p.stderr.decode()[-150:]
    except Exception as ex:
        verr=str(ex)[:150]
    if verr:
        try:txt('🎬 خطای ریلز: '+verr)
        except Exception:pass
    cardimg=None
    try:
        W,H=1080,1350
        bg=gen_img(imglist[2],W,H,seed+5)
        if bg:
            dark=Image.new('RGBA',(W,H),(5,5,10,170))
            cim=Image.alpha_composite(bg,dark)
        else:
            cim=Image.new('RGBA',(W,H),(18,18,24,255))
        dr=ImageDraw.Draw(cim)
        dr.rectangle((40,40,W-40,H-40),outline=(212,175,55),width=6)
        dr.text((W//2,130),'FOREXIN SMART STUDIO',fill=(212,175,55),font=F,anchor='mm')
        y=300
        for line in wrap('امروز: '+topic,22):
            dr.text((W//2,y),line,fill=(255,255,255),font=F2,anchor='mm');y+=60
        y+=40;dr.line((90,y,W-90,y),fill=(212,175,55),width=3);y+=90
        for line in wrap(part(ai,'[آموزش]','[ریلز]') or quote,28):
            dr.text((W//2,y),line,fill=(235,235,235),font=F2,anchor='mm');y+=58
            if y>H-260:break
        if logo:
            l3=lres(280);cim.paste(l3,((W-l3.width)//2,H-l3.height-70),l3)
        o=io.BytesIO();cim.convert('RGB').save(o,'JPEG',quality=88);cardimg=o.getvalue()
    except Exception:pass
    footer='\n\n━ ━ ━  ━ ━\n تتر: nobitex.ir/price/usdt\n🪙 طلای ۱۸: '+fa(g18)+' تومان/گرم | 🌍 انس: '+str(ounce)+' دلار\n\n🎓 یوتیوب: youtube.com/@Forexin.turkaslani\n📢 کانال: t.me/forexin_turkaslanifree\n🤖 ربات: t.me/TurkaslaniSiteBot\n🔥 استارت بزن، قیمت لحظه‌ای ببین!'
    head='📝 بسته روز | استودیو هوش فارکسین\n🎯 '+topic+'\n\n'
    send_file('/sendPhoto','photo','insta.jpg',cover_b,'image/jpeg',head+'📸 اینستاگرام:\n'+part(ai,'[اینستا]','[یوتیوب]')+LINKS)
    if video:send_file('/sendVideo','video','reel.mp4',video,'video/mp4','🎬 ریلز ۳صحنه‌ای:\n'+part(ai,'[ریلز]',''))
    send_file('/sendPhoto','photo','cover.jpg',wide_b,'image/jpeg','▶️ یوتیوب:\n'+part(ai,'[یوتیوب]','[لینکدین]')+LINKS+'\n\n💼 لینکدین:\n'+part(ai,'[لینکدین','[تلگرام]'))
    if cardimg:send_file('/sendPhoto','photo','card.jpg',cardimg,'image/jpeg','💡 کارت آموزشی:\n'+part(ai,'[آموزش]','[ریلز]'))
    txt('📢 تلگرام:\n'+part(ai,'[تلگرام]','[آموزش]')+'\n\n🦁 '+quote+footer)
    print('OK')
except Exception:
    try:txt('🛠 DEBUG:\n'+traceback.format_exc()[-1200:])
    except Exception:print(traceback.format_exc())
