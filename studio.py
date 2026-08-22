import json,os,io,re,time,urllib.request as ur,urllib.parse as up,random,traceback,subprocess,base64,math,sys
API='https://api.telegram.org/bot'+os.environ['TOKEN'];CHAT='227491135'
LOGO='https://mbms-1356.github.io/forexin-site-/logo.png'
VAULT='https://mbms-1356.github.io/forexin-site-/vault.json'
SITEB='https://mbms-1356.github.io/forexin-site-'
FONT='https://cdn.jsdelivr.net/gh/rastikerdar/vazirmatn@v33.003/fonts/ttf/Vazirmatn-Bold.ttf'
PAT=os.environ.get('GH_PAT','');OR=os.environ.get('OPENROUTER_KEY','');GK=os.environ.get('GROQ_KEY','')
CUSTOM=os.environ.get('CUSTOM','')
LINKS='\n🔗 لینک‌ها: nobitex.ir/price/usdt | t.me/forexin_turkaslanifree | youtube.com/@Forexin.turkaslani'
seed=int(time.time())%100000
PALS=[(255,200,60),(64,200,255),(120,220,120),(255,110,110),(190,140,255),(255,160,60)]
BGS=[(10,12,18),(16,10,26),(8,16,18),(20,12,10),(12,12,22)]
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
            r=ur.urlopen(ur.Request('https://openrouter.ai/api/v1/chat/completions',data=json.dumps({'model':m,'messages':[{'role':'system','content':s},{'role':'user','content':u}],'temperature':1.0,'max_tokens':1600}).encode(),headers={'Content-Type':'application/json','Authorization':'Bearer '+OR,'User-Agent':'forexin'}),timeout=60).read().decode()
            c=json.loads(r)['choices'][0]['message']['content']
            if c:return c
        except Exception:pass
    if GK:
        try:
            r=ur.urlopen(ur.Request('https://api.groq.com/openai/v1/chat/completions',data=json.dumps({'model':'llama-3.3-70b-versatile','messages':[{'role':'system','content':s},{'role':'user','content':u}],'temperature':1.0,'max_tokens':1600}).encode(),headers={'Content-Type':'application/json','Authorization':'Bearer '+GK}),timeout=60).read().decode()
            c=json.loads(r)['choices'][0]['message']['content']
            if c:return c
        except Exception:pass
    return ''
def R(name,train,task):
    return 'تو '+name+' هستی.\nآموزش: '+train+'\nوظیفهٔ تو حالا: '+task
def pick_icon(t):
    t=t.lower()
    if any(k in t for k in ['استاپ','ریسک','بقا','بیمه']):return 'shield'
    if any(k in t for k in ['ریوارد','تراز','تعادل']):return 'scale'
    if any(k in t for k in ['صبر','زمان','سشن','ساعت']):return 'clock'
    if any(k in t for k in ['لیکوی','نقدینگی','موج','fvg','شکاف']):return 'wave'
    if any(k in t for k in ['اهرم','شمشیر']):return 'sword'
    if any(k in t for k in ['سرمایه','سود','٪','درصد','خزانه']):return 'coin'
    if any(k in t for k in ['روان','ترس','طمع','احساس']):return 'brain'
    return 'chart'
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
    def gen_img(prompt,w,h,sd):
        try:
            u='https://image.pollinations.ai/prompt/'+up.quote(prompt)+'?width=%d&height=%d&nologo=true&model=flux&seed=%d'%(w,h,sd)
            d=get(u,40)
            if len(d)>15000 and (d[:2]==b'\xff\xd8' or d[:4]==b'\x89PNG'):
                return Image.open(io.BytesIO(d)).convert('RGBA')
        except Exception:pass
        return None
    REPO_IMGS=[]
    for path in ['','media/']:
        try:
            lst=json.loads(get('https://api.github.com/repos/Mbms-1356/forexin-site-/contents/'+path))
            for f in lst:
                n=f['name'].lower()
                if n.endswith(('.jpg','.jpeg','.png','.webp')) and n!='logo.png':
                    REPO_IMGS.append(f['download_url'])
        except Exception:pass
    last_img=''
    try:last_img=json.loads(get(SITEB+'img_used.json')).get('last','')
    except Exception:pass
    def crop_to(im,w,h):
        iw,ih=im.size;ta=w/h;ia=iw/ih
        if ia>ta:
            nw=int(ih*ta);x=(iw-nw)//2;im=im.crop((x,0,x+nw,ih))
        else:
            nh=int(iw/ta);y=(ih-nh)//2;im=im.crop((0,y,iw,y+nh))
        return im.resize((w,h))
    def media_img(w,h,sd):
        if not REPO_IMGS:return None,None
        rnd=random.Random(sd)
        pool=[u for u in REPO_IMGS if u!=last_img] or REPO_IMGS
        u=rnd.choice(pool)
        try:
            im=Image.open(io.BytesIO(get(u,30))).convert('RGBA')
            return crop_to(im,w,h),u
        except Exception:pass
        return None,None
    def brand(im,hook,sub):
        dr=ImageDraw.Draw(im)
        if F:
            y=110
            for line in wrap(hook,16):
                for ox,oy in [(3,3),(-3,3),(3,-3),(-3,-3)]:
                    dr.text((im.width//2+ox,y+oy),line,font=F,fill=(0,0,0,255),anchor='mm')
                dr.text((im.width//2,y),line,font=F,fill=(255,205,70,255),anchor='mm');y+=85
        if F3:
            dr.rounded_rectangle((30,30,360,86),radius=28,fill=(212,175,55,255))
            dr.text((48,58),'FOREXIN | LIT',font=F3,fill=(10,12,18,255),anchor='lm')
        if F3 and sub:dr.text((im.width//2,im.height-160),sub,font=F3,fill=(255,255,255,255),stroke_width=3,stroke_fill=(0,0,0,255),anchor='mm')
        if F3:dr.text((30,im.height-60),'@Forexin.turkaslani',font=F3,fill=(255,200,60,255),anchor='lm')
        putlogo(im,0.15,30)
        return im
    def draw_icon(dr,name,cx,cy,s,col):
        c=col+(255,)
        try:
            if name=='shield':
                dr.polygon([(cx,cy-s),(cx+s*0.8,cy-s*0.4),(cx+s*0.8,cy+s*0.2),(cx,cy+s),(cx-s*0.8,cy+s*0.2),(cx-s*0.8,cy-s*0.4)],outline=c,width=6)
                dr.line((cx-s*0.3,cy),(cx-s*0.05,cy+s*0.3),(cx+s*0.4,cy-s*0.3),fill=c,width=6)
            elif name=='scale':
                dr.line((cx,cy-s),(cx,cy+s*0.7),fill=c,width=6)
                dr.line((cx-s,cy-s*0.4,cx+s,cy-s*0.4),fill=c,width=6)
                dr.arc((cx-s-s*0.35,cy-s*0.4,cx-s+s*0.35,cy+s*0.3),0,180,fill=c,width=5)
                dr.arc((cx+s-s*0.35,cy-s*0.4,cx+s+s*0.35,cy+s*0.3),0,180,fill=c,width=5)
                dr.line((cx-s*0.5,cy+s*0.7,cx+s*0.5,cy+s*0.7),fill=c,width=6)
            elif name=='clock':
                dr.ellipse((cx-s,cy-s,cx+s,cy+s),outline=c,width=6)
                dr.line((cx,cy,cx,cy-s*0.6),fill=c,width=6)
                dr.line((cx,cy,cx+s*0.5,cy+s*0.2),fill=c,width=6)
            elif name=='wave':
                pts=[(cx-s+int(2*s*i/20),cy+int(s*0.5*math.sin(i*0.9))) for i in range(21)]
                dr.line(pts,fill=c,width=6)
                dr.line((cx-s,cy+s*0.8,cx+s,cy+s*0.8),fill=c,width=4)
            elif name=='sword':
                dr.line((cx,cy-s,cx,cy+s*0.6),fill=c,width=7)
                dr.polygon([(cx,cy-s),(cx-s*0.2,cy-s*0.6),(cx+s*0.2,cy-s*0.6)],fill=c)
                dr.line((cx-s*0.4,cy-s*0.5,cx+s*0.4,cy-s*0.5),fill=c,width=6)
            elif name=='coin':
                dr.ellipse((cx-s,cy-s,cx+s,cy+s),outline=c,width=6)
                dr.ellipse((cx-s*0.6,cy-s*0.6,cx+s*0.6,cy+s*0.6),outline=c,width=4)
                dr.line((cx,cy-s*0.4,cx,cy+s*0.4),fill=c,width=5)
            elif name=='brain':
                dr.ellipse((cx-s,cy-s*0.8,cx+s,cy+s*0.8),outline=c,width=6)
                dr.arc((cx-s*0.6,cy-s*0.5,cx,cy+s*0.2),0,360,fill=c,width=4)
                dr.arc((cx,cy-s*0.2,cx+s*0.6,cy+s*0.5),0,360,fill=c,width=4)
            else:
                for i in range(5):
                    x=cx-s+int(2*s*i/5);hgt=int(s*(0.4+0.5*abs(math.sin(i+1))))
                    colr=(46,200,110,255) if i%2 else (230,70,70,255)
                    dr.rectangle((x,cy+hgt//2,x+s*0.25,cy-hgt//2),fill=colr)
        except Exception:pass
    def spark(dr,x0,y0,w,h,rnd,pal):
        n=24;p=y0+h*0.5;pts=[]
        for i in range(n):
            p=max(y0+h*0.1,min(y0+h*0.9,p+rnd.uniform(-h*0.12,h*0.12)))
            pts.append((x0+int(w*i/(n-1)),int(p)))
        for wd,al in [(8,40),(4,140),(2,255)]:dr.line(pts,fill=pal+(al,),width=wd)
        return pts
    def designbg(w,h,sd,icon):
        rnd=random.Random(sd)
        pal=rnd.choice(PALS);c1=rnd.choice(BGS);c2=rnd.choice(BGS)
        im=Image.new('RGBA',(w,h));dr=ImageDraw.Draw(im)
        for y in range(h):
            t=y/h
            dr.line((0,y,w,y),fill=(int(c1[0]+(c2[0]-c1[0])*t),int(c1[1]+(c2[1]-c1[1])*t),int(c1[2]+(c2[2]-c1[2])*t),255))
        for i in range(3):
            x=rnd.randint(0,w);sw=rnd.randint(40,120)
            dr.polygon([(x,0),(x+sw,0),(x+sw-int(h*0.3),h),(x-int(h*0.3),h)],fill=pal+(rnd.randint(15,40),))
        for x in range(0,w,120):dr.line((x,0,x,h),fill=(255,255,255,10),width=1)
        spark(dr,int(w*0.08),int(h*0.66),int(w*0.84),int(h*0.24),rnd,pal)
        ix,iy=rnd.choice([(w//2,int(h*0.42)),(int(w*0.3),int(h*0.42)),(int(w*0.7),int(h*0.42))])
        dr.ellipse((ix-int(min(w,h)*0.2),iy-int(min(w,h)*0.2),ix+int(min(w,h)*0.2),iy+int(min(w,h)*0.2)),fill=(0,0,0,90))
        draw_icon(dr,icon,ix,iy,int(min(w,h)*0.14),pal)
        return im
    def design(w,h,hook,sub,sd,icon):
        return brand(designbg(w,h,sd,icon),hook,sub)
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
    cj={}
    try:cj=json.loads(CUSTOM)
    except Exception:cj={'topic':CUSTOM}
    custom_topic=cj.get('topic','') or '';custom_text=cj.get('text','') or '';custom_img=cj.get('img','') or '';MODE=cj.get('mode','full')
    vault={'principles':[],'quotes':[],'hooks':[],'lit_facts':[]}
    try:vault.update(json.loads(get(VAULT,15)))
    except Exception:pass
    notes=''
    try:notes=get(SITEB+'notes.txt',15)[:3000]
    except Exception:pass
    used=[]
    try:used=json.loads(get(SITEB+'used.json',15))
    except Exception:pass
    facts=' '.join(vault['lit_facts'])+' '+notes
    def related(t):
        ws=[w for w in re.split(r'[\s،,]+',t) if len(w)>2]
        hits=[]
        for src in vault['lit_facts']+vault['quotes']+vault['principles']:
            if any(w in src for w in ws):hits.append(src)
        return ' | '.join(hits[:6])
    pool=[p for p in vault['principles'] if p not in used]
    if not pool:
        fresh=ask(R('ایده‌پرداز فارکسین','موضوع‌ها جدید، کاربردی و متفاوت از پست‌های قبلی باشند.','فقط ۳ موضوع فارسی کوتاه و تازه دربارهٔ فارکس/طلا/پول هوشمند/روانشناسی بازار بنویس؛ هر خط یک موضوع، بدون شماره و علامت.'),'دانش برند: '+facts)
        nl=[x.strip(' -•*') for x in fresh.splitlines() if len(x.strip())>8][:3]
        pool=nl or vault['principles'] or ['مدیریت سرمایه: اول بقا، بعد سود']
    topic=custom_topic or random.choice(pool)
    if not custom_topic:
        used.append(topic);used=used[-30:]
        commit_site('used.json',json.dumps(used,ensure_ascii=False))
    hookT=random.choice(vault['hooks'] or ['قبل از هر ترید این را ببین'])
    quote=random.choice(vault['quotes'] or ['اول بقا، بعد سود.'])
    icon=pick_icon(topic)
    NARR=random.choice(['با یک داستان واقعی کوتاه','با یک آمار شوکه‌کننده','با یک سوال چالشی','با یک هشدار جدی','با مقایسهٔ دو نوع تریدر','با روایت یک اشتباه رایج'])
    REL=related(topic)
    usdt=0;ounce=0.0
    try:usdt=int(json.loads(get(SITEB+'price.json',10)).get('usdt',0))
    except Exception:pass
    try:ounce=float(json.loads(get('https://api.gold-api.com/price/XAU',10)).get('price',0))
    except Exception:pass
    g18=int(usdt*ounce/31.1035*0.75) if usdt and ounce else 0
    TRAIN='دانش برند: '+facts+' | لحن: حرفه‌ای، صمیمی، مطمئن، انسانی و احساسی، بدون وعدهٔ سود.'
    an=ask(R('تحلیلگر ارشد بازار فارکسین',TRAIN,'[تحلیل] ۲خط، [زاویه] داستانی احساسی، [هدف] مخاطب و درد او بنویس. سبک روایت: '+NARR),'موضوع: '+topic+' | انس: '+str(ounce)+(' | مطالب کتابخانه: '+REL if REL else '')+(' | یادداشت: '+custom_text[:300] if custom_text else ''))
    analysis=part(an,'[تحلیل]','[زاویه]') or topic
    angle=part(an,'[زاویه]','[هدف]');target=part(an,'[هدف]','')
    ad=ask(R('کارگردان هنری','تصویر باید مرتبط با موضوع و فارکس باشد.','فقط یک عبارت تصویری انگلیسی ۳-۶ کلمه‌ای بنویس که مفهوم موضوع را نشان دهد. [en]'),'موضوع: '+topic+' | تحلیل: '+analysis)
    en=part(ad,'[en]','').strip() or 'gold candlestick chart'
    imgp='cinematic photorealistic '+en+', glowing forex candlestick chart in background, dark golden light, no text'
    cp=ask(R('کپی‌رایتر ارشد فارکسین',TRAIN,'بخش‌های [اینستا][یوتیوب][لینکدین][تلگرام][آموزش][ریلز] را بنویس. هوک عدددار، سئو، لینک. سبک روایت: '+NARR+'. هوک و ساختار کاملاً متفاوت از پست‌های قبلی.'),'موضوع: '+topic+' | تحلیل: '+analysis+' | زاویه: '+angle+' | هدف: '+target+' | انس: '+str(ounce)+(' | مطالب کتابخانه: '+REL if REL else ''))
    gd=ask(R('نگهبان کیفیت (QC) فارکسین','متن: انسانی/احساسی/بدون تکرار/لحن برند. شروع و هوک باید متفاوت از پست‌های قبل باشد.','پیش‌نویس را بازنویسی کن و همان بخش‌ها [اینستا] تا [ریلز] را برگردان. پایان: این توصیهٔ مالی نیست.'),cp)
    ai=gd if (gd and '[اینستا]' in gd) else cp
    if not ai or '[اینستا]' not in ai:
        ai='[اینستا] 🔥 '+hookT+'\n'+topic+'؛ اصلی که ۹۰٪ نادیده می‌گیرند.\n'+quote+' تجربه‌ات را بنویس 👇'+LINKS+'\n#فارکس #ترید #مدیریت_سرمایه #LIT #فارکسین #پرایس_اکشن #طلا #روانشناسی_معاملات\n\n[یوتیوب] '+topic+' | آموزش کاربردی فارکس'+LINKS+'\n#فارکس #آموزش_فارکس #طلا #ترید #LIT #پرایس_اکشن\n\n[لینکدین] '+topic+'؛ اصلی که حرفه‌ای‌ها فراموش نمی‌کنند. #Forex #SmartMoney\n\n[تلگرام] 🔥 '+topic+'\nشما رعایت می‌کنید؟ بنویسید.\n\n[آموزش] یک معاملهٔ تمرینی با این اصل بزن و یادداشت کن.\n\n[ریلز] صحنه۱ هوک صحنه۲ توضیح صحنه۳ دعوت'
    if custom_text and len(custom_text)>100:
        ai='[اینستا] '+custom_text+'\n\n[یوتیوب] '+part(ai,'[یوتیوب]','[لینکدین]')+'\n\n[لینکدین] '+part(ai,'[لینکدین','[تلگرام]')+'\n\n[تلگرام] '+custom_text+'\n\n[آموزش] '+part(ai,'[آموزش]','[ریلز]')+'\n\n[ریلز] '+part(ai,'[ریلز]','')
    cover=None;mu=None
    if custom_img:
        try:
            d=get(custom_img,30)
            if len(d)>10000:cover=brand(crop_to(Image.open(io.BytesIO(d)).convert('RGBA'),1080,1080),short(topic,7),topic)
        except Exception:pass
    if cover is None:
        mi,mu=media_img(1080,1080,seed)
        if mi is not None:cover=brand(mi,short(topic,7),topic)
    if cover is None:
        g=gen_img(imgp,1080,1080,seed)
        cover=brand(g,short(topic,7),topic) if g else design(1080,1080,short(topic,7),topic,seed,icon)
    if mu:commit_site('img_used.json',json.dumps({'last':mu}))
    o=io.BytesIO();cover.convert('RGB').save(o,'JPEG',quality=88);cover_b=o.getvalue()
    o=io.BytesIO();Image.open(io.BytesIO(cover_b)).convert('RGB').resize((1080,608)).save(o,'JPEG',quality=88);wide_b=o.getvalue()
    head='📝 استودیو هوش فارکسین\n🎯 '+topic+'\n\n'
    if MODE=='cap':
        txt('✍️ کپشن اینستاگرام:\n'+part(ai,'[اینستا]','[یوتیوب]')+LINKS)
        txt('▶️ یوتیوب:\n'+part(ai,'[یوتیوب]','[لینکدین]')+LINKS)
        txt('💼 لینکدین:\n'+part(ai,'[لینکدین','[تلگرام]'))
        txt('📢 تلگرام:\n'+part(ai,'[تلگرام]','[آموزش]')+'\n🦁 '+quote)
        print('OK cap');sys.exit(0)
    if MODE=='img':
        send_file('/sendPhoto','photo','insta.jpg',cover_b,'image/jpeg',head+'🖼 تصویر موضوع')
        send_file('/sendPhoto','photo','cover.jpg',wide_b,'image/jpeg','🖼 کاور عریض')
        print('OK img');sys.exit(0)
    video=None;verr=''
    def clip(imgp2,outp,zoom):
        vf='zoompan=z=min(zoom+0.0015,1.12):d=100:s=720x900:fps=25,fade=t=in:st=0:d=0.4,fade=t=out:st=3.6:d=0.4' if zoom else 'scale=720:900,fps=25,fade=t=in:st=0:d=0.4,fade=t=out:st=3.6:d=0.4'
        p=subprocess.run(['ffmpeg','-y','-loop','1','-i',imgp2,'-t','4','-vf',vf,'-c:v','libx264','-pix_fmt','yuv420p',outp],timeout=120,capture_output=True)
        return p.returncode==0
    m1,_=media_img(720,900,seed+11)
    r1=brand(m1,short(hookT,5),'') if m1 is not None else design(720,900,short(hookT,5),'',seed+11,icon)
    scenes=[r1,design(720,900,short(topic,6),'راه‌حل: متد LIT',seed+7,'chart'),cta(720,900)]
    for i,im in enumerate(scenes):
        o=io.BytesIO();im.convert('RGB').save(o,'JPEG',quality=86);open('s%d.jpg'%i,'wb').write(o.getvalue())
    try:
        ok=all(clip('s%d.jpg'%i,'s%d.mp4'%i,True) for i in range(3))
        if not ok:ok=all(clip('s%d.jpg'%i,'s%d.mp4'%i,False) for i in range(3))
        if ok:
            open('list.txt','w').write("file 's0.mp4'\nfile 's1.mp4'\nfile 's2.mp4'\n")
            p=subprocess.run(['ffmpeg','-y','-f','concat','-safe','0','-i','list.txt','-c','copy','reel.mp4'],timeout=120,capture_output=True)
            if p.returncode==0:video=open('reel.mp4','rb').read()
    except Exception as ex:
        verr=str(ex)[:150]
    if not video:
        try:
            subprocess.run(['ffmpeg','-y','-loop','1','-i','s0.jpg','-t','5','-vf','scale=720:900,fps=25','-c:v','libx264','-pix_fmt','yuv420p','reel.mp4'],timeout=120,check=True,capture_output=True)
            video=open('reel.mp4','rb').read()
        except Exception as ex:verr=str(ex)[:150]
    if MODE=='vid':
        if video:send_file('/sendVideo','video','reel.mp4',video,'video/mp4','🎬 ریلز: '+topic)
        else:txt('🎬 خطای ریلز: '+verr)
        print('OK vid');sys.exit(0)
    cardimg=None
    try:
        W,H=1080,1350
        m2,_=media_img(W,H,seed+5)
        if m2 is not None:
            cim=m2
            dark=Image.new('RGBA',(W,H),(5,5,10,170))
            cim=Image.alpha_composite(cim,dark)
        else:
            cim=designbg(W,H,seed+9,icon)
            dark=Image.new('RGBA',(W,H),(5,5,10,150))
            cim=Image.alpha_composite(cim,dark)
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
    send_file('/sendPhoto','photo','insta.jpg',cover_b,'image/jpeg',head+'📸 اینستاگرام:\n'+part(ai,'[اینستا]','[یوتیوب]')+LINKS)
    if video:send_file('/sendVideo','video','reel.mp4',video,'video/mp4','🎬 ریلز ۳صحنه‌ای:\n'+part(ai,'[ریلز]',''))
    send_file('/sendPhoto','photo','cover.jpg',wide_b,'image/jpeg','▶️ یوتیوب:\n'+part(ai,'[یوتیوب]','[لینکدین]')+LINKS+'\n\n💼 لینکدین:\n'+part(ai,'[لینکدین','[تلگرام]'))
    if cardimg:send_file('/sendPhoto','photo','card.jpg',cardimg,'image/jpeg','💡 کارت آموزشی:\n'+part(ai,'[آموزش]','[ریلز]'))
    txt('📢 تلگرام:\n'+part(ai,'[تلگرام]','[آموزش]')+'\n\n🦁 '+quote+footer)
    print('OK full rel='+str(len(REL)))
except SystemExit:
    raise
except Exception:
    try:txt('🛠 DEBUG:\n'+traceback.format_exc()[-1200:])
    except Exception:print(traceback.format_exc())
