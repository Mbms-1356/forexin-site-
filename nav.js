(function(){
var el=document.getElementById('nav');if(!el)return;
var st=document.createElement('style');
st.textContent='.nav{'+(document.querySelector('.langbar')?'':'position:sticky;top:0;')+'background:rgba(7,11,9,.95);display:flex;justify-content:center;gap:4px;padding:8px;flex-wrap:wrap;z-index:9;border-bottom:1px solid rgba(245,196,81,.2)}.nav a{color:#f5c451;padding:6px 12px;border-radius:16px;font-size:.8rem;border:1px solid transparent;display:inline-flex;align-items:center;gap:6px}.nav a.on{border-color:rgba(245,196,81,.4);background:#101a15;box-shadow:0 0 12px rgba(245,196,81,.15)}.nic{width:18px;height:18px;stroke:url(#ng);fill:none;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round;filter:drop-shadow(0 1px 2px rgba(0,0,0,.7)) drop-shadow(0 0 4px rgba(245,196,81,.45))}';
document.head.appendChild(st);
var p=(location.pathname.split('/').pop()||'index.html');if(p==='')p='index.html';
var items=[
['index.html','خانه','<path d="M4 10.5L12 3.5l8 7"/><path d="M6 9.5V20h4.5v-5.5h3V20H18V9.5"/>'],
['maghale.html','مقاله','<rect x="3.5" y="4.5" width="17" height="16" rx="2"/><path d="M7.5 9h9M7.5 12.5h9M7.5 16h5.5"/>'],
['vajeh.html','واژه‌نامه','<path d="M12 6.5C10 4.9 7 4.3 4 4.3v13.9c3 0 6 .6 8 2.1 2-1.5 5-2.1 8-2.1V4.3c-3 0-6 .6-8 2.2z"/><path d="M12 6.5v13.8"/>'],
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
