/* Firmaty · animated satellite view of a pilot parcel (« Notre mission »).
   three.js r149 (MIT), loaded only when the section approaches the viewport. */
(function(){
  'use strict';
  var root=document.getElementById('mission');
  if(!root||!root.classList.contains('f3'))return;
  var frameEl=root.querySelector('.f3-frame'),stage=root.querySelector('.f3-stage');
  var reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
  var visible=false,api=null;

  /* ---------- helpers ---------- */
  function hash(x,y){var s=Math.sin(x*127.1+y*311.7)*43758.5453;return s-Math.floor(s)}
  function vnoise(x,y){var xi=Math.floor(x),yi=Math.floor(y),xf=x-xi,yf=y-yi,u=xf*xf*(3-2*xf),v=yf*yf*(3-2*yf);
    var a=hash(xi,yi),b=hash(xi+1,yi),c=hash(xi,yi+1),d=hash(xi+1,yi+1);return a+(b-a)*u+(c-a)*v+(a-b-c+d)*u*v}
  function fbm(x,y){var s=0,a=.5;for(var i=0;i<5;i++){s+=a*vnoise(x,y);x*=2.03;y*=2.03;a*=.5}return s/.97}
  function sst(a,b,x){var t=Math.min(1,Math.max(0,(x-a)/(b-a)));return t*t*(3-2*t)}
  var seed=7;function rnd(){seed=(seed*16807)%2147483647;return (seed-1)/2147483646}
  function rr(a,b){return a+(b-a)*rnd()}
  function H(x,z){return 2.2*Math.sin(x*.0024+1.3)+1.8*Math.cos(z*.0029+.4)}

  /* ---------- UI: layer list + KPI bar (works without WebGL) ---------- */
  var LAYERS=root.querySelectorAll('.f3-src li'),srcBox=root.querySelector('.f3-src'),cur=0,timer=null,DUR=7000;
  function select(i,user){if(i===cur&&!user)return;LAYERS.forEach(function(li,k){li.classList.toggle('on',k===i);li.querySelector('button').setAttribute('aria-pressed',k===i?'true':'false')});
    var prev=cur;cur=i;if(api)api.layer(prev,i);schedule(user?16000:DUR)}
  function schedule(ms){clearTimeout(timer);if(reduce)return;srcBox.style.setProperty('--dur',ms/1000+'s');
    var on=srcBox.querySelector('li.on');if(on){on.classList.remove('on');void on.offsetWidth;on.classList.add('on')}
    timer=setTimeout(function(){if(visible||!api)select((cur+1)%LAYERS.length);else schedule(DUR)},ms)}
  LAYERS.forEach(function(li,i){li.querySelector('button').addEventListener('click',function(){select(i,true)})});
  var bar=root.querySelector('.f3-bar i');
  new IntersectionObserver(function(es){if(es[0].isIntersecting){root.classList.add('f3-in');if(bar)bar.style.width='2%'}},{threshold:.25}).observe(frameEl);
  new IntersectionObserver(function(es){visible=es[0].isIntersecting},{threshold:0}).observe(frameEl);
  if(reduce)srcBox.classList.add('paused');

  function webgl(){try{var c=document.createElement('canvas');return !!(window.WebGLRenderingContext&&(c.getContext('webgl2')||c.getContext('webgl')))}catch(e){return false}}
  if(!webgl()){root.classList.add('f3-nogl');schedule(DUR);return}
  var started=false;
  var io0=new IntersectionObserver(function(es){if(es[0].isIntersecting&&!started){started=true;io0.disconnect();load()}},{rootMargin:'900px 0px'});io0.observe(frameEl);
  function load(){if(window.THREE)return init();var s=document.createElement('script');s.src='vendor/three.min.js';s.onload=init;s.onerror=function(){root.classList.add('f3-nogl')};document.head.appendChild(s)}
  function init(){try{build()}catch(e){root.classList.add('f3-nogl');if(window.console)console.error(e)}schedule(DUR+2600)}

  function build(){
  var T=THREE;T.ColorManagement.legacyMode=false;
  var small=innerWidth<900||!!window.F3_LITE;
  var renderer=new T.WebGLRenderer({antialias:!small,powerPreference:'high-performance'});
  renderer.setPixelRatio(Math.min(devicePixelRatio||1,small?1.5:1.75));
  renderer.outputEncoding=T.sRGBEncoding;renderer.toneMapping=T.ACESFilmicToneMapping;renderer.toneMappingExposure=1.02;
  renderer.shadowMap.enabled=true;renderer.shadowMap.type=T.PCFSoftShadowMap;
  stage.appendChild(renderer.domElement);
  var ANISO=Math.min(8,renderer.capabilities.getMaxAnisotropy());
  var scene=new T.Scene();scene.fog=new T.Fog('#a8a27c',2200,5200);
  var camera=new T.PerspectiveCamera(34,1,10,9000);

  /* environment: warm low sky for soft fill */
  var envScene=new T.Scene();envScene.add(new T.Mesh(new T.SphereGeometry(50,32,16),new T.ShaderMaterial({side:T.BackSide,
    vertexShader:'varying vec3 vP;void main(){vP=normalize(position);gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.0);}',
    fragmentShader:'varying vec3 vP;void main(){float h=vP.y;vec3 c=mix(vec3(.85,.80,.68),vec3(.55,.66,.74),smoothstep(0.0,.6,h));c=mix(c,vec3(.30,.30,.20),smoothstep(0.0,-.3,h));gl_FragColor=vec4(c,1.0);}'})));
  scene.environment=new T.PMREMGenerator(renderer).fromScene(envScene,.04).texture;
  scene.background=new T.Color('#a8a27c');

  /* light: golden hour, very low sun → long shadows */
  scene.add(new T.HemisphereLight('#c9dde0','#4d5a33',.28));
  var SUN=new T.Vector3(-.86,.33,.39).normalize();
  var sun=new T.DirectionalLight('#ffc37e',3.4);sun.position.copy(SUN).multiplyScalar(2400);sun.target.position.set(0,0,0);scene.add(sun,sun.target);
  sun.castShadow=true;var sc=sun.shadow.camera;sc.left=-1500;sc.right=1500;sc.top=1300;sc.bottom=-1300;sc.near=400;sc.far=5200;
  sun.shadow.mapSize.set(small?2048:4096,small?2048:4096);sun.shadow.bias=-.0003;sun.shadow.normalBias=1.4;

  /* ---------- textures ---------- */
  function tex(size,draw,rep){var c=document.createElement('canvas');c.width=c.height=size;var g=c.getContext('2d');draw(g,size);
    var t=new T.CanvasTexture(c);t.wrapS=t.wrapT=T.RepeatWrapping;t.encoding=T.sRGBEncoding;t.anisotropy=ANISO;if(rep)t.repeat.set(rep[0],rep[1]);return t}
  function speck(g,s,n,cols,w,h){for(var i=0;i<n;i++){g.fillStyle=cols[(rnd()*cols.length)|0];g.fillRect(rnd()*s,rnd()*s,w*(.6+rnd()*.8),h*(.6+rnd()*.8))}}
  var TX={
    wheat:tex(512,function(g,s){g.fillStyle='#c39146';g.fillRect(0,0,s,s);for(var y=0;y<s;y+=8){g.fillStyle='rgba(110,74,26,.12)';g.fillRect(0,y,s,3)}
      speck(g,s,17000,['#e9c47c','#d9a857','#ad7c35','#8c6226','#f3d898','#cc9a4a'],1.3,4.2);speck(g,s,2600,['rgba(70,48,18,.5)'],1.4,2.4)}),
    stubble:tex(512,function(g,s){g.fillStyle='#cdb683';g.fillRect(0,0,s,s);for(var y=0;y<s;y+=7){g.fillStyle='rgba(140,108,60,.3)';g.fillRect(0,y,s,1.6)}speck(g,s,9000,['#e2d4a8','#bea268','#ad935c','#e8dcb6'],1.6,1.6)}),
    plough:tex(512,function(g,s){g.fillStyle='#6d4f33';g.fillRect(0,0,s,s);for(var y=0;y<s;y+=6)for(var x=0;x<s;x+=4){var k=hash(x*.13,y*.7);g.fillStyle=k>.5?'rgba(140,104,66,.55)':'rgba(60,40,24,.45)';g.fillRect(x,y+k*1.4,4.4,2.6)}speck(g,s,5000,['#4f3722','#8c6a46','#5e432b'],2,1.6)}),
    green:tex(512,function(g,s){g.fillStyle='#7d6847';g.fillRect(0,0,s,s);for(var y=0;y<s;y+=10){g.fillStyle='#4f6d2b';g.fillRect(0,y+2,s,6)}speck(g,s,9000,['#6a8a37','#3f5c22','#5c7a30','#7e9a46'],2,2.2)}),
    meadow:tex(512,function(g,s){g.fillStyle='#78843f';g.fillRect(0,0,s,s);speck(g,s,15000,['#8b9550','#66713a','#9aa060','#5c6834','#a9a56e'],1.6,2.2)}),
    grass:tex(512,function(g,s){g.fillStyle='#8a8a52';g.fillRect(0,0,s,s);speck(g,s,16000,['#7b7c48','#9d9b63','#6c6f40','#a8a26c','#858a4e'],1.5,1.8)}),
    road:tex(256,function(g,s){g.fillStyle='#cdbb92';g.fillRect(0,0,s,s);speck(g,s,5000,['#bca97f','#dccfae','#b09c73'],1.6,1.6)}),
    roof:tex(256,function(g,s){for(var x=0;x<s;x+=8){g.fillStyle='#9fb3c9';g.fillRect(x,0,4,s);g.fillStyle='#7890ab';g.fillRect(x+4,0,4,s)}},[6,1]),
    silo:tex(256,function(g,s){g.fillStyle='#c3ccd6';g.fillRect(0,0,s,s);for(var y=0;y<s;y+=10){g.fillStyle='#9eabb9';g.fillRect(0,y,s,2)}},[3,4]),
    wall:tex(256,function(g,s){g.fillStyle='#e8e9e7';g.fillRect(0,0,s,s);for(var x=0;x<s;x+=12){g.fillStyle='rgba(120,130,140,.16)';g.fillRect(x,0,2,s)}},[5,1])};

  /* ---------- ground ---------- */
  var tg=new T.PlaneGeometry(9000,9000,120,120);tg.rotateX(-Math.PI/2);
  var tp=tg.attributes.position,tuv=tg.attributes.uv,tcol=new Float32Array(tp.count*3);
  for(var i=0;i<tp.count;i++){var x=tp.getX(i),z=tp.getZ(i);tp.setY(i,H(x,z)-.6);tuv.setXY(i,x/34,z/34);var n=.82+.3*fbm(x*.004+3,z*.004+9);tcol[i*3]=n;tcol[i*3+1]=n;tcol[i*3+2]=n*.95}
  tg.setAttribute('color',new T.BufferAttribute(tcol,3));tg.computeVertexNormals();
  var ground=new T.Mesh(tg,new T.MeshStandardMaterial({map:TX.grass,vertexColors:true,roughness:1,envMapIntensity:.35}));ground.receiveShadow=true;scene.add(ground);

  /* local frame of the pilot parcel (rotated grid of the farm) */
  var ANG=-.52,CA=Math.cos(ANG),SA=Math.sin(ANG);
  function L(u,v){return [u*CA-v*SA,u*SA+v*CA]}
  var PW=640,PD=540;   /* parcel size along u and v */

  /* ---------- fields ---------- */
  var FM={},TILE={wheat:32,stubble:38,plough:28,green:34,meadow:56};
  ['wheat','stubble','plough','green','meadow'].forEach(function(k){FM[k]=new T.MeshStandardMaterial({map:TX[k],bumpMap:TX[k],bumpScale:1,vertexColors:true,roughness:.96,envMapIntensity:.3,
    polygonOffset:true,polygonOffsetFactor:-2,polygonOffsetUnits:-4})});
  function fieldGeo(u0,v0,u1,v1,N,lift,tile){
    var pos=[],uv=[],luv=[],col=[],idx=[],tint=.88+rnd()*.18;
    for(var j=0;j<=N;j++)for(var i=0;i<=N;i++){var u=u0+(u1-u0)*i/N,v=v0+(v1-v0)*j/N,w=L(u,v),x=w[0],z=w[1];
      pos.push(x,H(x,z)+lift,z);uv.push(u/tile,v/tile);luv.push(i/N,j/N);var n=(.84+.28*fbm(x*.011+3,z*.011+5))*tint;col.push(n,n,n)}
    for(j=0;j<N;j++)for(i=0;i<N;i++){var a=j*(N+1)+i,b=a+1,c=a+N+1,d=c+1;idx.push(a,c,b,b,c,d)}
    var g=new T.BufferGeometry();g.setAttribute('position',new T.Float32BufferAttribute(pos,3));g.setAttribute('uv',new T.Float32BufferAttribute(uv,2));
    g.setAttribute('luv',new T.Float32BufferAttribute(luv,2));g.setAttribute('color',new T.Float32BufferAttribute(col,3));g.setIndex(idx);g.computeVertexNormals();
    if(g.attributes.normal.getY(0)<0){g.index.array.reverse();g.computeVertexNormals()}
    return g}
  function field(type,u0,v0,u1,v1,N){var m=new T.Mesh(fieldGeo(u0,v0,u1,v1,N||14,.45,TILE[type]),FM[type]);m.receiveShadow=true;scene.add(m);return m}
  var GAP=34;
  field('wheat',-PW/2,-PD/2,PW/2,PD/2,30);
  var types=['stubble','meadow','plough','green','wheat','meadow','stubble','plough'];
  var cols=[-2600,-1800,-1060,-PW/2-GAP-(PW*.9),-PW/2,PW/2+GAP,PW/2+GAP+520+GAP,1900,2700];
  for(var ci=0;ci<cols.length-1;ci++)for(var vr=-2600;vr<2600;){var dv=rr(380,560);var u0=cols[ci]+GAP/2,u1=cols[ci+1]-GAP/2;
      var isP=(u0<=-PW/2+1&&u1>=PW/2-1&&vr<PD/2&&vr+dv>-PD/2);
      if(!isP&&!(u0<PW/2&&u1>-PW/2&&vr+dv>-PD/2-GAP&&vr<PD/2+GAP))field(types[(rnd()*types.length)|0],u0,vr+GAP/2,u1,vr+dv-GAP/2);
      vr+=dv}
  /* the band above/below the parcel inside its column */
  field('meadow',-PW/2,PD/2+GAP,PW/2,PD/2+GAP+420);
  field('stubble',-PW/2,-PD/2-GAP-380,-40,-PD/2-GAP);

  /* roads */
  var roadMat=new T.MeshStandardMaterial({map:TX.road,roughness:1,envMapIntensity:.4,polygonOffset:true,polygonOffsetFactor:-1,polygonOffsetUnits:-2});
  function road(ua,va,ub,vb,w){var n=60,pos=[],uv=[],idx=[],len=Math.hypot(ub-ua,vb-va),nu=-(vb-va)/len*w/2,nv=(ub-ua)/len*w/2;
    for(var i=0;i<=n;i++){var u=ua+(ub-ua)*i/n,v=va+(vb-va)*i/n;[[u+nu,v+nv],[u-nu,v-nv]].forEach(function(q){var p=L(q[0],q[1]);pos.push(p[0],H(p[0],p[1])+.3,p[1])});uv.push(0,i*len/n/w,1,i*len/n/w);
      if(i){var a=(i-1)*2;idx.push(a,a+2,a+1,a+1,a+2,a+3)}}
    var g=new T.BufferGeometry();g.setAttribute('position',new T.Float32BufferAttribute(pos,3));g.setAttribute('uv',new T.Float32BufferAttribute(uv,2));g.setIndex(idx);g.computeVertexNormals();
    if(g.attributes.normal.getY(0)<0){g.index.array.reverse();g.computeVertexNormals()}var m=new T.Mesh(g,roadMat);m.receiveShadow=true;scene.add(m)}
  road(-3000,PD/2+GAP/2,3000,PD/2+GAP/2,12);
  road(PW/2+GAP/2,-3000,PW/2+GAP/2,3000,10);
  road(-PW/2-GAP/2,-PD/2-GAP/2,-PW/2-GAP/2,-3000,9);

  /* ---------- merged geometry + trees ---------- */
  function merge(parts){var P=[],N=[],C=[];parts.forEach(function(pr){var g=pr.g.index?pr.g.toNonIndexed():pr.g,p=g.attributes.position,n=g.attributes.normal,c=pr.c;
      for(var i=0;i<p.count;i++){P.push(p.getX(i),p.getY(i),p.getZ(i));N.push(n.getX(i),n.getY(i),n.getZ(i));var k=pr.shade?pr.shade(p.getY(i)):1;C.push(c.r*k,c.g*k,c.b*k)}});
    var g=new T.BufferGeometry();g.setAttribute('position',new T.Float32BufferAttribute(P,3));g.setAttribute('normal',new T.Float32BufferAttribute(N,3));g.setAttribute('color',new T.Float32BufferAttribute(C,3));return g}
  function blob(ws,hs,sd){var g=new T.SphereGeometry(1,ws,hs),p=g.attributes.position,v=new T.Vector3();
    for(var i=0;i<p.count;i++){v.fromBufferAttribute(p,i);v.multiplyScalar(1+.16*Math.sin(v.x*3.1+sd)*Math.cos(v.y*2.6+sd*1.3)+.1*Math.sin(v.z*4.7+sd*2.1));p.setXYZ(i,v.x,v.y,v.z)}g.computeVertexNormals();return g}
  function at(g,x,y,z,sx,sy,sz){g.scale(sx,sy,sz);g.translate(x,y,z);return g}
  var W1=new T.Color(1,1,1),BARK=new T.Color('#4a3a2a');function shade(lo,hi){return function(y){return .5+.5*sst(lo,hi,y)}}
  var treeGeo=merge([{g:at(new T.CylinderGeometry(.35,.55,6,6),0,3,0,1,1,1),c:BARK},{g:at(blob(10,8,1),0,9,0,4.6,5,4.6),c:W1,shade:shade(4,13)},
    {g:at(blob(9,7,4),2.6,7.4,1.2,3.1,3.3,3.1),c:W1,shade:shade(4,13)},{g:at(blob(9,7,7),-2.1,10.4,-1.1,2.9,3.4,2.9),c:W1,shade:shade(4,13)}]);
  var leaf=new T.MeshStandardMaterial({vertexColors:true,roughness:.9,envMapIntensity:.6});
  var GREENS=['#3f5a2a','#4b6a31','#334d24','#56743a','#5f7a3c','#455f30'].map(function(c){return new T.Color(c)});
  var trees=[];function tree(x,z,s,narrow){trees.push({x:x,z:z,s:s,n:narrow,c:GREENS[(rnd()*GREENS.length)|0].clone().multiplyScalar(.85+rnd()*.3),r:rnd()*6.28})}
  function hedge(ua,va,ub,vb,step,smin,smax,gap,narrow){var len=Math.hypot(ub-ua,vb-va),n=Math.floor(len/step);
    for(var i=0;i<=n;i++){var u=ua+(ub-ua)*i/n+rr(-2,2),v=va+(vb-va)*i/n+rr(-2,2),p=L(u,v);if(gap&&vnoise(u*.01+ua*.1,v*.01)<gap)continue;tree(p[0],p[1],rr(smin,smax),narrow)}}
  hedge(-3000,PD/2+GAP/2+12,3000,PD/2+GAP/2+12,8,1,1.45,.3);          /* along the main road */
  hedge(PW/2+GAP/2+11,-3000,PW/2+GAP/2+11,3000,9,1,1.4,.35);
  hedge(-PW/2-GAP/2-10,-PD/2-GAP,-PW/2-GAP/2-10,-3000,8,1,1.4,.3);
  hedge(-PW/2-GAP/2,PD/2+GAP,-PW/2-GAP/2,2600,9,.9,1.3,.45);
  for(i=0;i<16;i++){var hu=rr(-2600,2600),hv=rr(-2600,2600);if(Math.abs(hu)<PW&&Math.abs(hv)<PD)continue;var dir=rnd()<.5;hedge(hu,hv,dir?hu+rr(300,800):hu,dir?hv:hv+rr(300,800),9,1,1.4,.35)}
  for(i=0;i<220;i++){var su=rr(-2800,2800),sv=rr(-2800,2800);if(Math.abs(su)<PW/2+60&&Math.abs(sv)<PD/2+60)continue;var p0=L(su,sv);tree(p0[0],p0[1],rr(.9,1.5))}
  for(i=0;i<9;i++){var gp=L(rr(-1600,-700),rr(-1400,-500));for(var k=0;k<40;k++)tree(gp[0]+rr(-90,90),gp[1]+rr(-70,70),rr(1,1.6))}
  var tm=new T.InstancedMesh(treeGeo,leaf,trees.length),o=new T.Object3D();
  trees.forEach(function(t,i){o.position.set(t.x,H(t.x,t.z)-.3,t.z);o.rotation.set(0,t.r,0);if(t.n)o.scale.set(t.s*.42,t.s*1.9,t.s*.42);else o.scale.set(t.s,t.s*(.9+rnd()*.25),t.s);o.updateMatrix();tm.setMatrixAt(i,o.matrix);tm.setColorAt(i,t.c)});
  tm.castShadow=true;tm.receiveShadow=true;scene.add(tm);

  /* ---------- farmstead (above the parcel's far corner) ---------- */
  var MAT={wall:new T.MeshStandardMaterial({color:'#ecedeb',map:TX.wall,roughness:.8}),roof:new T.MeshStandardMaterial({color:'#e3ebf3',map:TX.roof,roughness:.45,metalness:.35,envMapIntensity:.8}),
    roofR:new T.MeshStandardMaterial({color:'#b5684f',roughness:.75}),silo:new T.MeshStandardMaterial({color:'#ffffff',map:TX.silo,roughness:.3,metalness:.65}),
    steel:new T.MeshStandardMaterial({color:'#7e868d',roughness:.55,metalness:.55}),dark:new T.MeshStandardMaterial({color:'#2b3236',roughness:.6}),
    concrete:new T.MeshStandardMaterial({color:'#cfcbbd',roughness:.95})};
  function sh(o){o.traverse(function(c){if(c.isMesh){c.castShadow=true;c.receiveShadow=true}})}
  function place(g,u,v,rot){var p=L(u,v);g.position.set(p[0],H(p[0],p[1]),p[1]);g.rotation.y=-ANG+(rot||0);g.scale.setScalar(1.45);sh(g);scene.add(g);return g}
  function barn(w,d,h,red,pitch){var g=new T.Group();var walls=new T.Mesh(new T.BoxGeometry(w,h,d),MAT.wall);walls.position.y=h/2;g.add(walls);
    var rise=w*(pitch||.24),s=new T.Shape();s.moveTo(-w/2,0);s.lineTo(0,rise);s.lineTo(w/2,0);s.lineTo(-w/2,0);
    var gab=new T.Mesh(new T.ExtrudeGeometry(s,{depth:d,bevelEnabled:false}),MAT.wall);gab.position.set(0,h,-d/2);g.add(gab);
    var sl=Math.hypot(w/2,rise)+1.6,an=Math.atan2(rise,w/2);[-1,1].forEach(function(sg){var r=new T.Mesh(new T.BoxGeometry(sl,.7,d+3),red?MAT.roofR:MAT.roof);r.position.set(sg*w/4,h+rise/2+.3,0);r.rotation.z=-sg*an;g.add(r)});
    var pad=new T.Mesh(new T.BoxGeometry(w+16,.6,d+16),MAT.concrete);pad.position.y=.1;g.add(pad);return g}
  function silo(r,h){var g=new T.Group();var b=new T.Mesh(new T.CylinderGeometry(r,r,h,28,1,true),MAT.silo);b.position.y=h/2+3;g.add(b);
    var t=new T.Mesh(new T.ConeGeometry(r*1.05,r*.75,28),MAT.silo);t.position.y=h+3+r*.37;g.add(t);var hp=new T.Mesh(new T.CylinderGeometry(r,1.2,3,20),MAT.steel);hp.position.y=1.5;g.add(hp);return g}
  var FU=-PW/2+60,FV=-PD/2-GAP-150;
  place(barn(70,36,13),FU+40,FV-30,Math.PI/2);
  place(barn(54,28,11),FU+120,FV-60,Math.PI/2);
  place(barn(30,18,8,true,.4),FU-20,FV-110,0);
  [0,1,2].forEach(function(i){place(silo(8,30),FU+150+i*19,FV+40)});
  place(silo(5.5,22),FU+215,FV+40);
  var yard=new T.Mesh(new T.PlaneGeometry(420,250),MAT.concrete);yard.rotation.x=-Math.PI/2;yard.rotation.z=-ANG;var yp=L(FU+90,FV-20);yard.position.set(yp[0],H(yp[0],yp[1])+.35,yp[1]);yard.receiveShadow=true;scene.add(yard);

  /* irrigation basin (right of the parcel) */
  var bs=new T.Shape(),BW=150,BD=170;bs.moveTo(-BW/2,-BD/2+30);bs.lineTo(-BW/2+30,-BD/2);bs.lineTo(BW/2,-BD/2);bs.lineTo(BW/2,BD/2-40);bs.lineTo(BW/2-50,BD/2);bs.lineTo(-BW/2,BD/2);bs.lineTo(-BW/2,-BD/2+30);
  var bp=L(PW/2+GAP+130,-30);
  var bank=new T.Mesh(new T.ShapeGeometry(bs),new T.MeshStandardMaterial({color:'#b9ad86',roughness:1,polygonOffset:true,polygonOffsetFactor:-2,polygonOffsetUnits:-4}));
  bank.rotation.x=-Math.PI/2;bank.rotation.z=-ANG;bank.scale.set(1.16,1.14,1);bank.position.set(bp[0],H(bp[0],bp[1])+.4,bp[1]);bank.receiveShadow=true;scene.add(bank);
  var water=new T.Mesh(new T.ShapeGeometry(bs),new T.MeshStandardMaterial({color:'#1d3247',roughness:.12,metalness:.3,envMapIntensity:1.2,polygonOffset:true,polygonOffsetFactor:-3,polygonOffsetUnits:-6}));
  water.rotation.x=-Math.PI/2;water.rotation.z=-ANG;water.position.set(bp[0],H(bp[0],bp[1])+.7,bp[1]);water.receiveShadow=true;scene.add(water);
  
  /* power line crossing the scene */
  var pylMat=new T.MeshStandardMaterial({color:'#6b7075',roughness:.6,metalness:.4}),latMat=new T.LineBasicMaterial({color:'#4f5559',transparent:true,opacity:.8});
  function beam(a,b,t){var d=new T.Vector3().subVectors(b,a),m=new T.Mesh(new T.BoxGeometry(t,t,d.length()),pylMat);m.position.copy(a).add(b).multiplyScalar(.5);m.lookAt(b);return m}
  var ATT=[[-12,46],[12,46],[-9,56],[9,56],[0,66]];
  function pylon(x,z,rot){var g=new T.Group(),lv=[],levels=[0,8,16,24,32,40,46,52,58,64];
    levels.forEach(function(y){var w=y<40?6.4-(y/40)*3.8:2.6-(y-40)/64*1.2;lv.push([[-w,-w],[w,-w],[w,w],[-w,w]].map(function(c){return new T.Vector3(c[0],y,c[1])}))});
    for(var k=0;k<4;k++)for(var l=0;l<levels.length-1;l++)g.add(beam(lv[l][k],lv[l+1][k],.7));
    var lp=[];for(l=0;l<levels.length-1;l++)for(k=0;k<4;k++)lp.push(lv[l][k],lv[l+1][(k+1)%4],lv[l][(k+1)%4],lv[l+1][k]);g.add(new T.LineSegments(new T.BufferGeometry().setFromPoints(lp),latMat));
    g.add(beam(new T.Vector3(-12,46,0),new T.Vector3(12,46,0),.8),beam(new T.Vector3(-9,56,0),new T.Vector3(9,56,0),.8));
    g.position.set(x,H(x,z),z);g.rotation.y=rot;g.traverse(function(c){if(c.isMesh)c.castShadow=true});scene.add(g);return g}
  var pyl=[];for(i=-3;i<=3;i++){var q=L(-PW/2-260+i*40,i*560);pyl.push(pylon(q[0],q[1],-ANG+Math.PI/2+.07))}
  var wm=new T.LineBasicMaterial({color:'#2f3437',transparent:true,opacity:.6});
  for(i=0;i<pyl.length-1;i++){pyl[i].updateMatrixWorld();pyl[i+1].updateMatrixWorld();ATT.forEach(function(ap){var a=new T.Vector3(ap[0],ap[1],0).applyMatrix4(pyl[i].matrixWorld),b=new T.Vector3(ap[0],ap[1],0).applyMatrix4(pyl[i+1].matrixWorld),pts=[];
    for(var s=0;s<=30;s++){var t=s/30,p=a.clone().lerp(b,t);p.y-=a.distanceTo(b)*.028*4*t*(1-t);pts.push(p)}scene.add(new T.Line(new T.BufferGeometry().setFromPoints(pts),wm))})}

  /* ---------- the zone map on the parcel ---------- */
  var ZU={uT:{value:0},uA:{value:0},uB:{value:0},uRev:{value:0},uOn:{value:0}};
  var zone=new T.ShaderMaterial({uniforms:ZU,transparent:true,depthWrite:false,polygonOffset:true,polygonOffsetFactor:-5,polygonOffsetUnits:-8,
    vertexShader:'attribute vec2 luv;varying vec2 vL;void main(){vL=luv;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.0);}',
    fragmentShader:[
      'uniform float uT,uA,uB,uRev,uOn;varying vec2 vL;',
      'float h(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}',
      'float n(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.0-2.0*f);return mix(mix(h(i),h(i+vec2(1,0)),f.x),mix(h(i+vec2(0,1)),h(i+vec2(1,1)),f.x),f.y);}',
      'float fb(vec2 p){float s=0.0,a=.55;for(int i=0;i<4;i++){s+=a*n(p);p*=2.07;a*=.5;}return s;}',
      'float val(vec2 c,float L){vec2 o=vec2(L*17.31,L*9.73);float sc=2.2+mod(L,2.0)*.7;float v=.5+(fb(c*sc+o)-.52)*2.6+.16*sin(c.x*3.0+L*2.1)*cos(c.y*2.4-L);return clamp(v,0.0,1.0);}',
      'vec3 pal(float k){if(k<1.0)return vec3(.80,.24,.15);if(k<2.0)return vec3(.91,.53,.18);if(k<3.0)return vec3(.93,.78,.34);if(k<4.0)return vec3(.16,.70,.60);return vec3(.04,.48,.46);}',
      'void main(){vec2 R=vec2(56.0,47.0);vec2 cell=floor(vL*R);vec2 cc=cell/R;vec2 fr=fract(vL*R);',
      ' float va=val(cc,uA),vb=val(cc,uB);',
      ' float d=dot(cc,normalize(vec2(1.0,.42)))*.92;float s=uRev*1.25-.12;',
      ' float useB=step(d,s);float v=mix(va,vb,useB);float k=floor(clamp(v,0.0,.999)*5.0);vec3 c=pal(k);',
      ' float gl=1.0-smoothstep(.0,.06,min(min(fr.x,fr.y),min(1.0-fr.x,1.0-fr.y)));c*=1.0-gl*.18;',
      ' float edge=exp(-abs(d-s)*70.0)*step(.001,uRev)*step(uRev,.999);',
      ' float tr=abs(fract(vL.x*13.0+.035*sin(vL.y*7.0+1.3))-.5);float tram=smoothstep(.485,.5,tr);',
      ' vec2 e=min(vL,1.0-vL);float bd=1.0-smoothstep(0.0,.004,min(e.x,e.y));',
      ' float spark=step(.985,h(cell+floor(uT*3.0)))*.6;',
      ' vec3 col=mix(c,vec3(.85,1.0,.95),edge*.85);col=mix(col,vec3(1.0),tram*.45+bd*.6);',
      ' float a=uOn*(.7+tram*.15+bd*.3)+edge*.6+spark*uOn*.15;gl_FragColor=vec4(col,clamp(a,0.0,1.0));}'].join('\n')});
  var zm=new T.Mesh(fieldGeo(-PW/2,-PD/2,PW/2,PD/2,46,1.1,40),zone);zm.renderOrder=5;scene.add(zm);

  /* legend lying along the near edge, like a printed scale on the map */
  (function(){var c=document.createElement('canvas');c.width=2048;c.height=230;var g=c.getContext('2d');
    var cols=['#cc3d26','#e8872e','#ebc454','#3fae94','#1a8073'],lab=['Très faible','Faible','Moyen','Élevé','Très élevé'];
    for(var i=0;i<5;i++){var x0=i*410+10;g.fillStyle=cols[i];g.fillRect(x0,16,380,22);g.save();g.translate(x0+190,138);g.font='italic 600 70px "Noto Sans",sans-serif';g.textAlign='center';
      g.fillStyle='rgba(0,0,0,.35)';g.fillText(lab[i],2,3);g.fillStyle='rgba(255,252,240,.95)';g.fillText(lab[i],0,0);g.restore()}
    var t=new T.CanvasTexture(c);t.encoding=T.sRGBEncoding;t.anisotropy=ANISO;
    var m=new T.Mesh(new T.PlaneGeometry(PW*.92,PW*.92*230/2048),new T.MeshBasicMaterial({map:t,transparent:true,depthWrite:false,polygonOffset:true,polygonOffsetFactor:-6,polygonOffsetUnits:-10}));
    m.rotation.x=-Math.PI/2;m.rotation.z=-ANG;var p=L(0,PD/2+GAP/2+24);m.position.set(p[0],H(p[0],p[1])+1.4,p[1]);m.renderOrder=6;scene.add(m)})();

  /* ---------- combine working the parcel along the tramlines ---------- */
  function boxm(w,h,d,mat,x,y,z){var m=new T.Mesh(new T.BoxGeometry(w,h,d),mat);m.position.set(x,y,z);return m}
  function wheel(r,w,x,y,z){var m=new T.Mesh(new T.CylinderGeometry(r,r,w,16),new T.MeshStandardMaterial({color:'#1c1e1f',roughness:.85}));m.rotation.z=Math.PI/2;m.position.set(x,y,z);return m}
  var CG=new T.MeshStandardMaterial({color:'#2f8048',roughness:.45,metalness:.25}),GL=new T.MeshStandardMaterial({color:'#1b2a30',roughness:.08,metalness:.6}),WH=new T.MeshStandardMaterial({color:'#eef0ee',roughness:.5});
  var combine=new T.Group();combine.add(boxm(8.4,5.6,12,CG,0,5.2,0),boxm(7.6,3.2,8,CG,0,9.4,-1.6),boxm(5,4.4,4.6,GL,0,10.2,4.2),boxm(5.6,.4,5.2,WH,0,12.6,4.2),
    boxm(26,1.5,4,new T.MeshStandardMaterial({color:'#9aa1a6',roughness:.5,metalness:.4}),0,1.6,10.6),wheel(2.9,2.1,-4.9,2.9,3.2),wheel(2.9,2.1,4.9,2.9,3.2),wheel(1.8,1.4,-4.2,1.8,-4.4),wheel(1.8,1.4,4.2,1.8,-4.4));
  var reel=new T.Mesh(new T.CylinderGeometry(1.4,1.4,25,10),new T.MeshStandardMaterial({color:'#c4472f',roughness:.6}));reel.rotation.z=Math.PI/2;reel.position.set(0,3.6,11.4);combine.add(reel);
  combine.scale.setScalar(1.6);sh(combine);scene.add(combine);
  var trailer=new T.Group();trailer.add(boxm(3,2.6,6,new T.MeshStandardMaterial({color:'#2f6f3c',roughness:.5}),0,3,1.6),boxm(3.2,3.2,3,GL,0,5.4,-1),boxm(4.6,2.8,9,new T.MeshStandardMaterial({color:'#8c6a3e',roughness:.8}),0,3.4,-9.5),
    wheel(2.1,1.3,-2.2,2.1,-1.2),wheel(2.1,1.3,2.2,2.1,-1.2),wheel(1.3,.9,-2.5,1.3,-10),wheel(1.3,.9,2.5,1.3,-10));trailer.scale.setScalar(1.6);sh(trailer);scene.add(trailer);
  var LANE=PW/13,hv={lane:2,u:-PW/2+20,dir:1,turn:-1};
  var dustTex=(function(){var c=document.createElement('canvas');c.width=c.height=64;var g=c.getContext('2d'),gr=g.createRadialGradient(32,32,0,32,32,32);gr.addColorStop(0,'rgba(255,255,255,1)');gr.addColorStop(1,'rgba(255,255,255,0)');g.fillStyle=gr;g.fillRect(0,0,64,64);return new T.CanvasTexture(c)})();
  var dust=[];for(i=0;i<20;i++){var sp=new T.Sprite(new T.SpriteMaterial({map:dustTex,color:'#efdcae',transparent:true,depthWrite:false,opacity:0}));sp.userData={life:1};scene.add(sp);dust.push(sp)}
  var dI=0,dT=0;

  /* drifting cloud shadows */
  var cloudTex=(function(){var c=document.createElement('canvas');c.width=c.height=512;var g=c.getContext('2d');
    for(var i=0;i<26;i++){var x=rnd()*512,y=rnd()*512,r=40+rnd()*90;for(var dx=-1;dx<=1;dx++)for(var dy=-1;dy<=1;dy++){var gr=g.createRadialGradient(x+dx*512,y+dy*512,0,x+dx*512,y+dy*512,r);gr.addColorStop(0,'rgba(0,0,0,.55)');gr.addColorStop(1,'rgba(0,0,0,0)');g.fillStyle=gr;g.fillRect(x+dx*512-r,y+dy*512-r,r*2,r*2)}}
    var t=new T.CanvasTexture(c);t.wrapS=t.wrapT=T.RepeatWrapping;t.repeat.set(2.2,2.2);return t})();
  var clouds=new T.Mesh(new T.PlaneGeometry(7000,7000),new T.MeshBasicMaterial({map:cloudTex,transparent:true,opacity:.32,depthWrite:false,fog:false,color:'#0b1408'}));
  clouds.rotation.x=-Math.PI/2;clouds.position.y=3.2;clouds.renderOrder=8;scene.add(clouds);

  /* ---------- camera ---------- */
  var mouse={x:0,y:0,tx:0,ty:0};
  frameEl.addEventListener('pointermove',function(e){if(e.pointerType!=='mouse')return;var r=frameEl.getBoundingClientRect();mouse.tx=(e.clientX-r.left)/r.width-.5;mouse.ty=(e.clientY-r.top)/r.height-.5});
  frameEl.addEventListener('pointerleave',function(){mouse.tx=0;mouse.ty=0});
  var aspect=1,tgt=new T.Vector3();
  function resize(){var w=stage.clientWidth,h=stage.clientHeight;if(!w||!h)return;renderer.setSize(w,h,false);aspect=w/h;camera.aspect=aspect;camera.fov=aspect<.8?44:(aspect<1.15?38:32);camera.updateProjectionMatrix()}
  addEventListener('resize',resize);resize();

  /* ---------- layer API used by the UI ---------- */
  var rev={t:1,from:0,to:0};
  api={layer:function(a,b){ZU.uA.value=a;ZU.uB.value=b;ZU.uRev.value=0;rev.t=0}};
  ZU.uA.value=0;ZU.uB.value=0;var intro=0;

  /* ---------- loop ---------- */
  var clock=0,last=performance.now(),perf={n:0,sum:0,level:0},fr=0,v3=new T.Vector3();
  function adapt(ms){if(perf.level>1||ms>400)return;perf.n++;perf.sum+=ms;if(perf.n<45)return;var avg=perf.sum/perf.n;perf.n=0;perf.sum=0;
    if(avg>30){perf.level++;if(perf.level===1)renderer.setPixelRatio(Math.min(1.25,devicePixelRatio||1));else{sun.shadow.mapSize.set(1024,1024);sun.shadow.map&&sun.shadow.map.dispose();sun.shadow.map=null;renderer.setPixelRatio(1)}resize()}}
  function frame(now){requestAnimationFrame(frame);var raw=now-last;last=now;if(!visible||document.hidden)return;
    var dt=Math.min(window.F3_LITE?.5:.05,raw/1000);if(fr>3)adapt(raw);clock+=dt;ZU.uT.value=clock;
    /* first satellite pass, then layer transitions */
    if(intro<1){intro=Math.min(1,intro+dt/(reduce?.01:2.6));ZU.uOn.value=sst(0,.25,intro);ZU.uRev.value=intro;if(intro>=1)ZU.uRev.value=1}
    else if(rev.t<1){rev.t=Math.min(1,rev.t+dt/(reduce?.01:2.2));ZU.uRev.value=rev.t}
    /* camera: high oblique, slow breathing drift */
    mouse.x+=(mouse.tx-mouse.x)*Math.min(1,dt*2);mouse.y+=(mouse.ty-mouse.y)*Math.min(1,dt*2);
    var yaw=-.18+(reduce?0:Math.sin(clock*.05)*.05)+mouse.x*.08,pitch=.92+(reduce?0:Math.sin(clock*.037)*.02)-mouse.y*.05,dist=aspect<.8?2350:(aspect<1.15?2050:1900);
    tgt.set(-20,0,aspect<.8?260:230);
    camera.position.set(tgt.x+Math.sin(yaw)*Math.cos(pitch)*dist,Math.sin(pitch)*dist,tgt.z+Math.cos(yaw)*Math.cos(pitch)*dist);camera.lookAt(tgt);
    /* combine on the tramlines */
    if(!reduce){var spd=8*dt;if(hv.turn<0){hv.u+=spd*hv.dir;if(hv.u>PW/2-24||hv.u<-PW/2+24){hv.u=Math.max(-PW/2+24,Math.min(PW/2-24,hv.u));hv.turn=0}}
      else{hv.turn+=dt/5;if(hv.turn>=1){hv.turn=-1;hv.dir*=-1;hv.lane=(hv.lane+1)%12}}}
    var lv=-PD/2+30+hv.lane*((PD-60)/11),cu=hv.u,cv=lv,ry=hv.dir>0?0:Math.PI;
    if(hv.turn>=0){var th=hv.turn*Math.PI,rad=(PD-60)/22;cu=hv.u+hv.dir*Math.sin(th)*rad;cv=lv+rad-Math.cos(th)*rad;ry=(hv.dir>0?0:Math.PI)-hv.dir*th}
    var cp=L(cu,cv),ddx=cp[0]-combine.position.x,ddz=cp[1]-combine.position.z;if(ddx*ddx+ddz*ddz>1e-4)combine.rotation.y=Math.atan2(ddx,ddz);combine.position.set(cp[0],H(cp[0],cp[1])+.4,cp[1]);reel.rotation.x+=dt*2.4;
    dT+=dt;if(dT>.2&&!reduce){dT=0;var p=dust[dI++%dust.length],bk=L(cu-hv.dir*14,cv);p.position.set(bk[0]+rr(-3,3),H(bk[0],bk[1])+5,bk[1]+rr(-3,3));p.userData.life=0;p.userData.vx=rr(-1,1);p.userData.vy=rr(1.5,3)}
    dust.forEach(function(p){var u=p.userData;if(u.life<1){u.life+=dt/3;p.position.x+=(u.vx+2.6)*dt*3;p.position.y+=u.vy*dt*3;var s=7+u.life*20;p.scale.set(s,s,1);p.material.opacity=Math.sin(u.life*Math.PI)*.4}else p.material.opacity=0});
    /* tractor along the main road */
    var tu=-1800+((clock*14)%3600),tp2=L(tu,PD/2+GAP/2);trailer.position.set(tp2[0],H(tp2[0],tp2[1])+.3,tp2[1]);trailer.rotation.y=Math.atan2(CA,SA);
    cloudTex.offset.set(clock*.0016,clock*.0009);
    renderer.render(scene,camera);
    if(++fr===3)root.classList.add('f3-live');
  }
  requestAnimationFrame(frame);
  }
})();
