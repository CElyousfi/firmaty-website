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
})();
