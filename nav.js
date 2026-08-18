(function(){
var el=document.getElementById('nav');
var st=document.createElement('style');
st.textContent='.nav{'+(document.querySelector('.langbar')?'':'position:sticky;top:0;')+'background:rgba(7,11,9,.95);display:flex;justify-content:center;gap:4px;padding:8px;flex-wrap:wrap;z-index:9;border-bottom:1px solid rgba(245,196,81,.2)}.nav a{color:#f5c451;padding:6px 12px;border-radius:16px;font-size:.8rem;border:1px solid transparent;display:inline-flex;align-items:center;gap:6px}.nav a.on{border-color:rgba(245,196,81,.4);background:#101a15;box-shadow:0 0 12px rgba(245,196,81,.15)}.nic{width:18px;height:18px;stroke:url(#ng);fill:none;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round;filter:drop-shadow(0 1px 2px rgba(0,0,0,.7)) drop-shadow(0 0 4px rgba(245,196,81,.45))}.tgfloat{position:fixed;bottom:18px;left:18px;z-index:99;display:flex;align-items:center;gap:8px;padding:12px 20px;border-radius:30px;background:linear-gradient(145deg,#5ecdf5,#2AABEE 60%,#1c8fc7);color:#fff;font-weight:bold;font-size:.85rem;box-shadow:0 8px 25px rgba(42,171,238,.5);animation:fl 2.2s infinite;text-decoration:none}.tgfloat svg{width:22px;height:22px;fill:#fff}@keyframes fl{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}';
document.head.appendChild(st);
document.body.insertAdjacentHTML('beforeend','<a class="tgfloat" href="https://t.me/TurkaslaniSiteBot?start=web" target="_blank"><svg viewBox="0 0 24 24"><path d="M9.78 18.65l.28-4.23 7.68-6.92c.34-.31-.07-.46-.52-.19L7.74 13.3 3.64 12c-.88-.25-.89-.86.2-1.3l15.97-6.16c.73-.33 1.43.18 1.15 1.3l-2.72 12.81c-.19.91-.74 1.13-1.5.71l-4.14-3.05-1.99 1.93c-.23.23-.42.42-.83.41z"/></svg>چت آنلاین</a>');
if(!el)return;
var p=(location.pathname.split('/').pop()||'index.html');if(p==='')p='index.html';
var items=[
['index.html','خانه','<path d="M4 10.5L12 3.5l8 7"/><path d="M6 9.5V20h4.5v-5.5h3V20H18V9.5"/>'],
['learn.html','آموزش','<path d="M12 4L2 9l10 5 10-5-10-5z"/><path d="M6 11.5V16c0 1.5 2.7 3 6 3s6-1.5 6-3v-4.5"/>'],
['quiz.html','آزمون','<rect x="5" y="5" width="14" height="16" rx="2"/><path d="M9 5V3h6v2"/><path d="M9 13l2 2 4-5"/>'],
['maghale.html','مقاله','<rect x="3.5" y="4.5" width="17" height="16" rx="2"/><path d="M7.5 9h9M7.5 12.5h9M7.5 16h5.5"/>'],
['results.html','نتایج','<path d="M7 4h10v4a5 5 0 0 1-10 0V4z"/><path d="M7 5H4v2a4 4 0 0 0 4 4"/><path d="M17 5h3v2a4 4 0 0 1-4 4"/><path d="M12 13v4"/><path d="M8 21h8"/><path d="M10 21c0-2.2.9-4 2-4s2 1.8 2 4"/>'],
['plans.html','پلن‌ها','<path d="M7 3.5h10l4 5.5-9 11.5L3 9l4-5.5z"/><path d="M3 9h18"/><path d="M12 20.5L8.5 9 12 3.5 15.5 9 12 20.5"/>'],
['platforms.html','پلتفرم‌ها','<rect x="3" y="4.5" width="18" height="12" rx="2"/><path d="M12 16.5v4M8 20.5h8"/>'],
['about.html','درباره','<circle cx="9" cy="8" r="3.2"/><path d="M4 19.5c0-3 2.2-5 5-5s5 2 5 5"/><circle cx="17" cy="9" r="2.6"/><path d="M15.8 14.3c2.5.4 4.2 2.2 4.2 4.7"/>'],
['rules.html','قوانین','<path d="M12 4v16"/><path d="M9 20h6"/><path d="M5 7h14"/><path d="M7 7l-3 6a3.4 3.4 0 0 0 6 0L7 7z"/><path d="M17 7l-3 6a3.4 3.4 0 0 0 6 0l-3-6"/>']
];
var h='<div class="nav"><svg style="display:none"><defs><linearGradient id="ng" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffe9a3"/><stop offset=".5" stop-color="#f5c451"/><stop offset="1" stop-color="#b8860b"/></linearGradient></defs></svg>';
for(var i=0;i<items.length;i++){
var on=(p===items[i][0])?' class="on"':'';
h+='<a href="'+items[i][0]+'"'+on+'><svg class="nic" viewBox="0 0 24 24">'+items[i][2]+'</svg>'+items[i][1]+'</a>';
}
h+='</div>';
el.innerHTML=h;
})();
