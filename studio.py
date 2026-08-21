import json,os,io,time,urllib.request as ur,random,traceback,subprocess,base64
API='https://api.telegram.org/bot'+os.environ['TOKEN'];CHAT='227491135'
LOGO='https://mbms-1356.github.io/forexin-site-/logo.png'
VAULT='https://mbms-1356.github.io/forexin-site-/vault.json'
FONT='https://cdn.jsdelivr.net/gh/rastikerdar/vazirmatn@v33.003/fonts/ttf/Vazirmatn-Bold.ttf'
PAT=os.environ.get('GH_PAT','');OR=os.environ.get('OPENROUTER_KEY','');GK=os.environ.get('GROQ_KEY','')
CUSTOM=os.environ.get('CUSTOM','')
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
    F=None;F2=None;F3=None;FT=None;FB=None
    try:
        fd=get(FONT,20)
        F=ImageFont.truetype(io.BytesIO(fd),58);F2=ImageFont.truetype(io.BytesIO(fd),38);F3=ImageFont.truetype(io.BytesIO(fd),30)
        FT=ImageFont.truetype(io.BytesIO(fd),74);FB=ImageFont.truetype(io.BytesIO(fd),44)
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
    def poster(tp,hk,sd):
        W,H=1080,1350
        im=Image.new('RGBA',(W,H),(15,12,8,255));dr=ImageDraw.Draw(im)
        for y in range(H):
            t=y/H
            dr.line((0,y,W,y),fill=(int(28+40*(1-t)),int(20+26*(1-t)),int(10+12*(1-t)),255))
        for x in range(0,W,120):dr.line((x,0,x,H),fill=(255,200,60,14),width=1)
        if F3:dr.text((W//2,70),'FOREXIN TURKASLANI | متد LIT',font=F3,fill=(255,205,70),anchor='mm')
        if logo:
            l2=lres(150);im.paste(l2,(W-175,20),l2)
        y=230
        if FT:
            for line in wrap(tp,16):
                dr.text((W//2,y),line,font=FT,fill=(255,215,80),stroke_width=5,stroke_fill=(40,25,5),anchor='mm');y+=100
        y+=10;dr.line((W//2-220,y,W//2+220,y),fill=(212,175,55),width=4);y+=80
        if F2:
            for line in wrap(hk or 'پول هوشمند این‌جا منتظر توست',26):
                dr.text((W//2,y),line,font=F2,fill=(255,255,255),stroke_width=3,stroke_fill=(0,0,0),anchor='mm');y+=58
        py=y+50;ph=330
        dr.rounded_rectangle((60,py,W-60,py+ph),radius=24,fill=(8,10,16,235),outline=(212,175,55),width=3)
        rnd=random.Random(sd);n=24;cw=(W-160)//n;x0=80
