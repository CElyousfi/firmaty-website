(function(){
  var reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* entrance animations: hero items slide in on load, the rest as it scrolls into view */
  if('IntersectionObserver' in window && !reduce){
    document.documentElement.classList.add('js');
    document.querySelectorAll('.hero .a1,.phero .a1').forEach(function(el,i){el.classList.add('pre');setTimeout(function(){el.classList.remove('pre')},150+i*100)});
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.remove('pre');io.unobserve(e.target)}})},{rootMargin:'0px 0px -6% 0px'});
    document.querySelectorAll('.a2,.a3,.fd,.fi,.sl').forEach(function(el){if(el.getBoundingClientRect().top>innerHeight){el.classList.add('pre');io.observe(el)}});
    setTimeout(function(){document.querySelectorAll('.pre').forEach(function(el){el.classList.remove('pre')})},8000);
  }

  /* header shadow, back-to-top, mobile menu */
  var hdr=document.getElementById('hdr'),up=document.getElementById('up');
  function sc(){var y=scrollY;if(hdr)hdr.classList.toggle('stuck',y>50);if(up)up.classList.toggle('on',y>innerHeight*.6)}
  addEventListener('scroll',sc,{passive:true});sc();
  var bg=document.getElementById('burger'),dr=document.getElementById('drop');
  if(bg&&dr){
    bg.addEventListener('click',function(){var o=dr.classList.toggle('open');bg.setAttribute('aria-expanded',o)});
    dr.querySelectorAll('a').forEach(function(a){a.addEventListener('click',function(){dr.classList.remove('open');bg.setAttribute('aria-expanded','false')})});
  }

  /* demo request forms: validate, then confirm in place */
  document.querySelectorAll('form.demo-form,#demoForm').forEach(function(f){
    var err=f.querySelector('.err');
    f.addEventListener('submit',function(e){
      e.preventDefault();err.textContent='';
      if(!f.nom.value.trim()){err.textContent='Indiquez votre nom pour que nous puissions vous recontacter.';f.nom.focus();return}
      if(!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(f.email.value.trim())){err.textContent='Saisissez un email valide, par exemple vous@exploitation.ma.';f.email.focus();return}
      if(!f.ok.checked){err.textContent='Cochez la case de consentement pour envoyer votre demande.';return}
      f.innerHTML='<div class="done" role="status"><h3>Demande enregistrée</h3><p>Nous revenons vers vous pour convenir d\'un créneau et des secteurs à analyser.</p></div>';
    });
  });

  /* gallery lightbox */
  var lb=document.getElementById('lb');
  if(lb){
    var items=[].slice.call(document.querySelectorAll('.gbtn')),cur=0,last=null;
    var img=document.getElementById('lbImg'),cap=document.getElementById('lbCap');
    function show(i){cur=(i+items.length)%items.length;var b=items[cur];img.src=b.dataset.full;img.alt=b.dataset.cap;cap.textContent=b.dataset.cap}
    function open(i){last=document.activeElement;show(i);lb.hidden=false;document.body.style.overflow='hidden';document.getElementById('lbX').focus()}
    function close(){lb.hidden=true;document.body.style.overflow='';if(last)last.focus()}
    items.forEach(function(b,i){b.addEventListener('click',function(){open(i)})});
    document.getElementById('lbX').addEventListener('click',close);
    document.getElementById('lbP').addEventListener('click',function(){show(cur-1)});
    document.getElementById('lbN').addEventListener('click',function(){show(cur+1)});
    lb.addEventListener('click',function(e){if(e.target===lb)close()});
    addEventListener('keydown',function(e){if(lb.hidden)return;if(e.key==='Escape')close();if(e.key==='ArrowLeft')show(cur-1);if(e.key==='ArrowRight')show(cur+1)});
  }

  /* play-once animations (engine sequence, lead-time chart) */
  var plays=document.querySelectorAll('[data-play]');
  if(plays.length){
    if('IntersectionObserver' in window && !reduce){
      var po=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('play');po.unobserve(e.target)}})},{threshold:.35});
      plays.forEach(function(el){po.observe(el)});
    } else plays.forEach(function(el){el.classList.add('play')});
  }

  /* moving pill under a segmented control */
  function ink(bar,btn,el){if(!bar||!btn||!el)return;el.style.width=btn.offsetWidth+'px';el.style.transform='translateX('+(btn.offsetLeft)+'px)'}

  /* plateforme: pinned screen follows the step in view */
  var scrolly=document.querySelector('.scrolly');
  if(scrolly){
    var steps=[].slice.call(scrolly.querySelectorAll('.st-step')),frames=scrolly.querySelectorAll('.st-frame'),tabs=[].slice.call(scrolly.querySelectorAll('.st-tab'));
    var bar=scrolly.querySelector('.st-tabs'),sink=scrolly.querySelector('.st-ink'),prog=scrolly.querySelector('.st-progress i'),cur=-1;
    function setStep(i){
      if(i===cur)return;cur=i;
      steps.forEach(function(s,k){s.classList.toggle('on',k===i)});
      frames.forEach(function(f,k){f.classList.toggle('on',k===i)});
      tabs.forEach(function(t,k){t.classList.toggle('on',k===i);t.setAttribute('aria-selected',k===i)});
      ink(bar,tabs[i],sink);if(prog)prog.style.width=((i+1)/steps.length*100)+'%';
    }
    function onScroll(){var mid=innerHeight*.5,best=0,bd=1e9;steps.forEach(function(s,k){var r=s.getBoundingClientRect(),d=Math.abs(r.top+r.height/2-mid);if(d<bd){bd=d;best=k}});setStep(best)}
    tabs.forEach(function(t,k){t.addEventListener('click',function(){var r=steps[k].getBoundingClientRect();scrollTo({top:scrollY+r.top+r.height/2-innerHeight/2,behavior:reduce?'auto':'smooth'})})});
    addEventListener('scroll',onScroll,{passive:true});addEventListener('resize',function(){ink(bar,tabs[cur],sink)});
    setStep(0);ink(bar,tabs[0],sink);onScroll();
    if(document.fonts&&document.fonts.ready)document.fonts.ready.then(function(){ink(bar,tabs[cur],sink)});
  }

  /* méthode: satellite-only vs Firmaty reading of the same sectors */
  document.querySelectorAll('.smap').forEach(function(m){
    var btns=[].slice.call(m.querySelectorAll('.smap-toggle button')),bar=m.querySelector('.smap-toggle'),sk=m.querySelector('.smap-ink');
    function set(mode){m.dataset.mode=mode;btns.forEach(function(b){var on=b.dataset.mode===mode;b.classList.toggle('on',on);b.setAttribute('aria-selected',on);if(on)ink(bar,b,sk)})}
    btns.forEach(function(b){b.addEventListener('click',function(){set(b.dataset.mode)})});
    set('sat');addEventListener('resize',function(){ink(bar,m.querySelector('.smap-toggle .on'),sk)});
    if(document.fonts&&document.fonts.ready)document.fonts.ready.then(function(){ink(bar,m.querySelector('.smap-toggle .on'),sk)});
  });

  /* pour qui: audience tabs with arrow-key support */
  document.querySelectorAll('.aud').forEach(function(a){
    var tabs=[].slice.call(a.querySelectorAll('.aud-tab')),imgs=a.querySelectorAll('.aud-img'),panels=a.querySelectorAll('.aud-panel');
    function set(i,focus){tabs.forEach(function(t,k){var on=k===i;t.classList.toggle('on',on);t.setAttribute('aria-selected',on);t.tabIndex=on?0:-1});
      imgs.forEach(function(im,k){im.classList.toggle('on',k===i)});panels.forEach(function(p,k){p.hidden=k!==i;p.classList.toggle('on',k===i)});if(focus)tabs[i].focus()}
    tabs.forEach(function(t,k){t.addEventListener('click',function(){set(k)});t.addEventListener('keydown',function(e){if(e.key==='ArrowRight'){e.preventDefault();set((k+1)%tabs.length,true)}if(e.key==='ArrowLeft'){e.preventDefault();set((k-1+tabs.length)%tabs.length,true)}})});
    set(0);
  });

  /* galerie: filters */
  var chips=[].slice.call(document.querySelectorAll('.chip-btn'));
  chips.forEach(function(c){c.addEventListener('click',function(){
    var f=c.dataset.f;chips.forEach(function(x){var on=x===c;x.classList.toggle('on',on);x.setAttribute('aria-pressed',on)});
    document.querySelectorAll('.gitem').forEach(function(g){var isScr=g.classList.contains('scr'),show=f==='all'||(f==='scr'?isScr:!isScr);g.classList.toggle('out',!show);if(show){g.classList.remove('fadein');void g.offsetWidth;g.classList.add('fadein')}});
  })});

  /* questions: live search */
  var q=document.getElementById('q');
  if(q){
    var items=[].slice.call(document.querySelectorAll('.faqs details')),groups=[].slice.call(document.querySelectorAll('.faq-group')),cnt=document.querySelector('.faq-count'),empty=document.querySelector('.faq-empty');
    items.forEach(function(d){d.dataset.txt=d.textContent.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'');d.dataset.open=d.open?'1':''});
    function esc(x){return x.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')}
    q.addEventListener('input',function(){
      var v=q.value.trim().toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,''),n=0;
      items.forEach(function(d){var hit=!v||d.dataset.txt.indexOf(v)>-1;d.classList.toggle('out',!hit);if(hit)n++;d.open=v?hit:!!d.dataset.open});
      groups.forEach(function(g){g.classList.toggle('out',!g.querySelector('details:not(.out)'))});
      cnt.textContent=v?(n+' réponse'+(n>1?'s':'')):'';empty.hidden=!(v&&n===0);
    });
  }
})();
