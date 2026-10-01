(function(){
  var reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
  if('IntersectionObserver' in window && !reduce){
    document.documentElement.classList.add('js');
    document.querySelectorAll('.hero .a1').forEach(function(el,i){el.classList.add('pre');setTimeout(function(){el.classList.remove('pre')},150+i*100)});
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.remove('pre');io.unobserve(e.target)}})},{rootMargin:'0px 0px -6% 0px'});
    document.querySelectorAll('.a2,.a3,.fd,.fi,.sl').forEach(function(el){if(el.getBoundingClientRect().top>innerHeight){el.classList.add('pre');io.observe(el)}});
    setTimeout(function(){document.querySelectorAll('.pre').forEach(function(el){el.classList.remove('pre')})},8000);
  }

  /* aerial imagery drawn in code: orchard sectors seen from orbit */
  function rng(a){return function(){a|=0;a=a+0x6D2B79F5|0;var t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}
  function mix(c1,c2,t){return 'rgb('+c1.map(function(v,i){return Math.round(v+(c2[i]-v)*t)}).join(',')+')'}
  function ndviCol(v){var s=[[190,59,51],[226,170,60],[200,205,90],[90,160,70],[28,100,50]];var x=Math.max(0,Math.min(.999,v))*(s.length-1),i=Math.floor(x);return mix(s[i],s[i+1],x-i)}
  function draw(cv){
    var seed=+cv.dataset.field,zoom=+cv.dataset.zoom||1,ndvi=cv.dataset.ndvi,markC=cv.dataset.mark;
    var r=cv.getBoundingClientRect(),dpr=Math.min(window.devicePixelRatio||1,2),W=Math.max(1,r.width),H=Math.max(1,r.height);
    cv.width=W*dpr;cv.height=H*dpr;var g=cv.getContext('2d');g.setTransform(dpr,0,0,dpr,0,0);
    var R=rng(seed);
    g.fillStyle=ndvi?'#3b3a33':'#b8a479';g.fillRect(0,0,W,H);
    if(!ndvi)for(var n=0;n<W*H/900;n++){g.fillStyle='rgba('+(R()<.5?'90,70,40':'232,218,184')+','+(R()*.08)+')';g.fillRect(R()*W,R()*H,2+R()*6,2+R()*6)}
    var cell=230*zoom,road=9*zoom,tilt=-.06,marked=null;
    g.save();g.translate(W/2,H/2);g.rotate(tilt);g.translate(-W/2-cell*.4,-H/2-cell*.4);
    var cols=Math.ceil(W/cell)+2,rows=Math.ceil(H/(cell*.82))+2;
    for(var y=0;y<rows;y++)for(var x=0;x<cols;x++){
      var off=(y%2)*cell*.35,x0=x*cell+off+road+R()*8,y0=y*cell*.82+road+R()*8,w=cell-road*2-R()*14,h=cell*.82-road*2-R()*12;
      var type=R(),v=.45+R()*.55,angle=R()<.5;
      if(markC&&!marked&&x0>W*.25&&y0>H*.15&&x0+w<W*.95)marked={x:x0,y:y0,w:w,h:h};
      g.save();g.beginPath();g.rect(x0,y0,w,h);g.clip();
      if(ndvi){
        for(var a=x0;a<x0+w;a+=6*zoom)for(var b=y0;b<y0+h;b+=6*zoom){var lv=v+(R()-.5)*.35-(type<.15?.4:0);g.fillStyle=ndviCol(lv);g.fillRect(a,b,6*zoom+.5,6*zoom+.5)}
      }else if(type<.16){g.fillStyle='#a88f63';g.fillRect(x0,y0,w,h);g.strokeStyle='rgba(80,60,35,.25)';g.lineWidth=1.5*zoom;for(var s=0;s<w+h;s+=7*zoom){g.beginPath();g.moveTo(x0+s,y0);g.lineTo(x0+s-h*.3,y0+h);g.stroke()}}
      else if(type<.38){g.fillStyle=mix([150,160,70],[70,120,50],v);g.fillRect(x0,y0,w,h);g.strokeStyle='rgba(30,60,20,.18)';g.lineWidth=2*zoom;for(var s2=0;s2<h;s2+=6*zoom){g.beginPath();g.moveTo(x0,y0+s2);g.lineTo(x0+w,y0+s2);g.stroke()}}
      else{
        g.fillStyle='#a8946a';g.fillRect(x0,y0,w,h);
        var sp=(11+R()*3)*zoom,rad=sp*.42;
        for(var a2=x0+sp/2;a2<x0+w;a2+=angle?sp*1.35:sp)for(var b2=y0+sp/2;b2<y0+h;b2+=angle?sp:sp*1.35){
          var lv2=Math.max(0,Math.min(1,v+(R()-.5)*.25)),rr=rad*(.75+lv2*.35);
          g.fillStyle='rgba(40,30,15,.35)';g.beginPath();g.arc(a2+rr*.35,b2+rr*.35,rr,0,6.283);g.fill();
          g.fillStyle=mix([150,150,60],[28,72,36],lv2);g.beginPath();g.arc(a2,b2,rr,0,6.283);g.fill();
          g.fillStyle='rgba(255,255,220,.10)';g.beginPath();g.arc(a2-rr*.3,b2-rr*.3,rr*.45,0,6.283);g.fill();
        }
      }
      g.restore();
    }
    if(marked){g.strokeStyle='#FFFBF3';g.lineWidth=2.5;g.setLineDash([8,6]);g.strokeRect(marked.x,marked.y,marked.w,marked.h);g.setLineDash([]);g.fillStyle='rgba(190,59,51,.22)';g.fillRect(marked.x,marked.y,marked.w,marked.h)}
    g.restore();
  }
  function paint(){document.querySelectorAll('canvas[data-field]').forEach(draw)}
  var t;addEventListener('resize',function(){clearTimeout(t);t=setTimeout(paint,150)});
  paint();if(document.fonts&&document.fonts.ready)document.fonts.ready.then(paint);

  var hdr=document.getElementById('hdr'),up=document.getElementById('up');
  function sc(){var y=scrollY;hdr.classList.toggle('stuck',y>50);up.classList.toggle('on',y>innerHeight*.6)}
  addEventListener('scroll',sc,{passive:true});sc();
  var bg=document.getElementById('burger'),dr=document.getElementById('drop');
  bg.addEventListener('click',function(){var o=dr.classList.toggle('open');bg.setAttribute('aria-expanded',o)});
  dr.querySelectorAll('a').forEach(function(a){a.addEventListener('click',function(){dr.classList.remove('open');bg.setAttribute('aria-expanded','false')})});

  var f=document.getElementById('demoForm'),err=document.getElementById('err');
  f.addEventListener('submit',function(e){
    e.preventDefault();err.textContent='';
    if(!f.nom.value.trim()){err.textContent='Indiquez votre nom pour que nous puissions vous recontacter.';f.nom.focus();return}
    if(!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(f.email.value.trim())){err.textContent='Saisissez un email valide, par exemple vous@exploitation.ma.';f.email.focus();return}
    if(!f.ok.checked){err.textContent='Cochez la case de consentement pour envoyer votre demande.';return}
    f.innerHTML='<div class="done" role="status"><h3>Demande enregistrée</h3><p>Nous revenons vers vous pour convenir d\'un créneau et des secteurs à analyser.</p></div>';
  });
})();