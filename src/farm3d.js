/* Firmaty · living 3D farm for the « Notre mission » section.
   three.js r149 (MIT), loaded on demand when the section approaches the viewport. */
(function(){
  'use strict';
  var root=document.getElementById('mission');
  if(!root||!root.classList.contains('f3'))return;
  var reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
  var stage=root.querySelector('.f3-stage'),hotBox=root.querySelector('.f3-hot');
  var MONTHS=['Janvier','Février','Mars','Avril','Mai','Juin','Juillet','Août','Septembre','Octobre','Novembre','Décembre'];
  var season={m:6.15,speed:1/6};          /* months; one month every 6 s */
  var visible=false;

  /* ---------------- small math helpers ---------------- */
  function hash(x,y){var s=Math.sin(x*127.1+y*311.7)*43758.5453;return s-Math.floor(s)}
  function vnoise(x,y){var xi=Math.floor(x),yi=Math.floor(y),xf=x-xi,yf=y-yi,u=xf*xf*(3-2*xf),v=yf*yf*(3-2*yf);
    var a=hash(xi,yi),b=hash(xi+1,yi),c=hash(xi,yi+1),d=hash(xi+1,yi+1);return a+(b-a)*u+(c-a)*v+(a-b-c+d)*u*v}
  function fbm(x,y){var s=0,a=.5;for(var i=0;i<5;i++){s+=a*vnoise(x,y);x*=2.03;y*=2.03;a*=.5}return s/.97}
  function sst(a,b,x){var t=Math.min(1,Math.max(0,(x-a)/(b-a)));return t*t*(3-2*t)}
  var seed=11;function rnd(){seed=(seed*16807)%2147483647;return (seed-1)/2147483646}
  function rr(a,b){return a+(b-a)*rnd()}
  function H(x,z){
    var base=3*Math.sin(x*.0021+1.3)+2.5*Math.cos(z*.0027+.4);
    var r=Math.hypot(x*.72,z+260);
    var hills=sst(1400,3900,r)*(fbm(x*.0007+3,z*.0007+7)*150+8);
    var ridge=sst(2400,5600,-z)*(40+fbm(x*.00045+1,4.2)*170);
    return base+hills+ridge}

  /* ---------------- HUD: card, sparklines, timeline (also without WebGL) ---------------- */
  setupHUD();
  function webgl(){try{var c=document.createElement('canvas');return !!(window.WebGLRenderingContext&&(c.getContext('webgl2')||c.getContext('webgl')))}catch(e){return false}}
  if(!webgl()){root.classList.add('f3-nogl');return}
  var started=false;
  var io0=new IntersectionObserver(function(es){if(es[0].isIntersecting&&!started){started=true;io0.disconnect();load()}},{rootMargin:'900px 0px'});
  io0.observe(root);
  function load(){if(window.THREE)return init();var s=document.createElement('script');s.src='vendor/three.min.js';s.onload=init;s.onerror=function(){root.classList.add('f3-nogl')};document.head.appendChild(s)}

  function init(){
  try{build()}catch(e){root.classList.add('f3-nogl');if(window.console)console.error(e)}
  }

  function build(){
  var T=THREE;T.ColorManagement.legacyMode=false;
  var small=innerWidth<900||!!window.F3_LITE;
  var renderer=new T.WebGLRenderer({antialias:!small,powerPreference:'high-performance'});
  var maxPR=small?1.5:1.75;renderer.setPixelRatio(Math.min(devicePixelRatio||1,maxPR));
  renderer.outputEncoding=T.sRGBEncoding;renderer.toneMapping=T.ACESFilmicToneMapping;renderer.toneMappingExposure=.9;
  renderer.shadowMap.enabled=!small;renderer.shadowMap.type=T.PCFSoftShadowMap;
  stage.appendChild(renderer.domElement);
  var ANISO=Math.min(8,renderer.capabilities.getMaxAnisotropy());

  var scene=new T.Scene();
  var FOGC='#dcd8c9';scene.fog=new T.Fog(FOGC,420,4400);
  var camera=new T.PerspectiveCamera(34,1,3,14000);

  /* ---------- sky ---------- */
  var SUN=new T.Vector3(-.62,.40,-.68).normalize();
  function skyMat(){return new T.ShaderMaterial({uniforms:{uSun:{value:SUN}},side:T.BackSide,depthWrite:false,fog:false,
    vertexShader:'varying vec3 vP;void main(){vP=normalize(position);gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.0);}',
    fragmentShader:'uniform vec3 uSun;varying vec3 vP;void main(){float h=vP.y;vec3 hor=vec3(.863,.847,.788);vec3 zen=vec3(.62,.72,.78);'+
      'vec3 c=mix(hor,zen,pow(smoothstep(0.0,.3,max(h,0.0)),.7));float s=max(dot(vP,uSun),0.0);'+
      'c+=vec3(1.0,.9,.7)*(pow(s,6.0)*.30+pow(s,48.0)*.55)+vec3(1.0,.97,.9)*pow(s,900.0)*1.5;'+
      'c=mix(c,vec3(.42,.38,.28),smoothstep(0.0,-.2,h));gl_FragColor=vec4(c,1.0);}'})}
  var sky=new T.Mesh(new T.SphereGeometry(11000,48,24),skyMat());scene.add(sky);
  var pmrem=new T.PMREMGenerator(renderer);var envScene=new T.Scene();envScene.add(new T.Mesh(new T.SphereGeometry(50,32,16),skyMat()));
  scene.environment=pmrem.fromScene(envScene,.04).texture;

  /* ---------- light ---------- */
  scene.add(new T.HemisphereLight('#eef3f5','#6e5f40',.22));
  var sun=new T.DirectionalLight('#ffd49a',3.1);sun.position.copy(SUN).multiplyScalar(1600).add(new T.Vector3(0,0,-120));
  sun.target.position.set(0,0,-120);scene.add(sun,sun.target);
  if(!small){sun.castShadow=true;var sc=sun.shadow.camera;sc.left=-1150;sc.right=1150;sc.top=950;sc.bottom=-950;sc.near=200;sc.far=3400;
    sun.shadow.mapSize.set(2048,2048);sun.shadow.bias=-.0004;sun.shadow.normalBias=1.2;}

  /* ---------- procedural textures ---------- */
  function tex(size,draw,rep){var c=document.createElement('canvas');c.width=c.height=size;var g=c.getContext('2d');draw(g,size);
    var t=new T.CanvasTexture(c);t.wrapS=t.wrapT=T.RepeatWrapping;t.encoding=T.sRGBEncoding;t.anisotropy=ANISO;if(rep)t.repeat.set(rep[0],rep[1]);return t}
  function speck(g,s,n,cols,w,h){for(var i=0;i<n;i++){g.fillStyle=cols[(rnd()*cols.length)|0];g.fillRect(rnd()*s,rnd()*s,w*(.6+rnd()*.8),h*(.6+rnd()*.8))}}
  var TX={
    wheat:tex(512,function(g,s){g.fillStyle='#c4953f';g.fillRect(0,0,s,s);
      for(var y=0;y<s;y+=8){g.fillStyle='rgba(120,84,32,.10)';g.fillRect(0,y,s,3)}
      speck(g,s,17000,['#ecc77c','#dcac56','#b07f36','#8f6427','#f6dc9c','#cf9d4b'],1.3,4.4);
      speck(g,s,2600,['rgba(80,56,22,.55)'],1.4,2.4);}),
    stubble:tex(512,function(g,s){g.fillStyle='#d4c08e';g.fillRect(0,0,s,s);
      for(var y=0;y<s;y+=7){g.fillStyle='rgba(150,118,66,.28)';g.fillRect(0,y,s,1.6)}
      speck(g,s,9000,['#e8dcb4','#c4aa72','#b39a63','#efe4c2'],1.6,1.6);}),
    plough:tex(512,function(g,s){g.fillStyle='#7a593a';g.fillRect(0,0,s,s);
      for(var y=0;y<s;y+=6){for(var x=0;x<s;x+=4){var k=hash(x*.13,y*.7);g.fillStyle=k>.5?'rgba(150,112,72,.55)':'rgba(70,48,28,.45)';g.fillRect(x,y+(k*1.4),4.4,2.6)}}
      speck(g,s,5000,['#5a3f26','#9a7650','#6b4c30'],2,1.6);}),
    green:tex(512,function(g,s){g.fillStyle='#8c744d';g.fillRect(0,0,s,s);
      for(var y=0;y<s;y+=10){g.fillStyle='#5f7d31';g.fillRect(0,y+2,s,6)}
      speck(g,s,9000,['#7b9b40','#4c6a26','#6c8b37','#91ab52'],2,2.2);}),
    meadow:tex(512,function(g,s){g.fillStyle='#98a05e';g.fillRect(0,0,s,s);speck(g,s,14000,['#a9b06b','#848c4c','#b6b77a','#7a8446','#c2bd86'],1.6,2.2);}),
    grass:tex(512,function(g,s){g.fillStyle='#bcb084';g.fillRect(0,0,s,s);speck(g,s,16000,['#a99f6d','#cfc49b','#999266','#b9b27f','#d8cfaa'],1.5,1.8);}),
    road:tex(256,function(g,s){g.fillStyle='#d5c6a0';g.fillRect(0,0,s,s);speck(g,s,5000,['#c4b28a','#e2d6b6','#b8a47c'],1.6,1.6);
      g.fillStyle='rgba(140,116,80,.35)';g.fillRect(s*.28,0,s*.08,s);g.fillRect(s*.64,0,s*.08,s);}),
    roof:tex(256,function(g,s){for(var x=0;x<s;x+=8){g.fillStyle='#93a9c1';g.fillRect(x,0,4,s);g.fillStyle='#6f87a2';g.fillRect(x+4,0,4,s)}},[6,1]),
    silo:tex(256,function(g,s){g.fillStyle='#c3ccd6';g.fillRect(0,0,s,s);for(var y=0;y<s;y+=10){g.fillStyle='#9eabb9';g.fillRect(0,y,s,2)}for(var x=0;x<s;x+=4){g.fillStyle='rgba(255,255,255,.12)';g.fillRect(x,0,1,s)}},[3,4]),
    wall:tex(256,function(g,s){g.fillStyle='#e6e8e8';g.fillRect(0,0,s,s);for(var x=0;x<s;x+=12){g.fillStyle='rgba(120,130,140,.18)';g.fillRect(x,0,2,s)}},[5,1])
  };

  /* ---------- terrain ---------- */
  var TW=10000,TD=9200,TZ=-2100,seg=small?160:230;
  var tg=new T.PlaneGeometry(TW,TD,seg,seg);tg.rotateX(-Math.PI/2);tg.translate(0,0,TZ);
  var tp=tg.attributes.position,tuv=tg.attributes.uv,tcol=new Float32Array(tp.count*3);
  var cNear=new T.Color('#d2c79f'),cFar=new T.Color('#97a06e'),cWood=new T.Color('#7d8a5a'),ct=new T.Color();
  for(var i=0;i<tp.count;i++){var x=tp.getX(i),z=tp.getZ(i);tp.setY(i,H(x,z)-.6);tuv.setXY(i,x/38,z/38);
    var far=sst(900,2600,Math.hypot(x*.72,z+260)),n=fbm(x*.002+9,z*.002+2);
    ct.copy(cNear).lerp(cFar,far*.9).lerp(cWood,far*sst(.55,.75,n)*.8);ct.multiplyScalar(.9+.18*fbm(x*.01,z*.01));
    tcol[i*3]=ct.r;tcol[i*3+1]=ct.g;tcol[i*3+2]=ct.b}
  tg.setAttribute('color',new T.BufferAttribute(tcol,3));tg.computeVertexNormals();
  var terrain=new T.Mesh(tg,new T.MeshStandardMaterial({map:TX.grass,vertexColors:true,roughness:1,envMapIntensity:.35}));
  terrain.receiveShadow=true;scene.add(terrain);

  /* ---------- fields ---------- */
  var FM={};
  function fmat(k,extra){var m=new T.MeshStandardMaterial(Object.assign({map:TX[k],bumpMap:TX[k],bumpScale:1.1,vertexColors:true,roughness:.96,envMapIntensity:.32,
    polygonOffset:true,polygonOffsetFactor:-2,polygonOffsetUnits:-4},extra||{}));return m}
  ['wheat','stubble','plough','green','meadow'].forEach(function(k){FM[k]=fmat(k)});
  var TILE={wheat:34,stubble:40,plough:30,green:36,meadow:60};
  var fields=[];
  function quadPt(P,u,v){var ax=P[0][0]+(P[1][0]-P[0][0])*u,az=P[0][1]+(P[1][1]-P[0][1])*u,bx=P[3][0]+(P[2][0]-P[3][0])*u,bz=P[3][1]+(P[2][1]-P[3][1])*u;return [ax+(bx-ax)*v,az+(bz-az)*v]}
  function fieldGeo(P,N,lift,tile){
    var ang=Math.atan2(P[1][1]-P[0][1],P[1][0]-P[0][0]),ca=Math.cos(-ang),sa=Math.sin(-ang);
    var pos=[],uv=[],luv=[],col=[],idx=[];var tint=.86+rnd()*.2;
    for(var j=0;j<=N;j++)for(var i=0;i<=N;i++){var u=i/N,v=j/N,q=quadPt(P,u,v),x=q[0],z=q[1];
      pos.push(x,H(x,z)+lift,z);uv.push((x*ca-z*sa)/tile,(x*sa+z*ca)/tile);luv.push(u,v);
      var n=(.82+.3*fbm(x*.012+3,z*.012+5))*tint;col.push(n,n,n)}
    for(j=0;j<N;j++)for(i=0;i<N;i++){var a=j*(N+1)+i,b=a+1,c=a+N+1,d=c+1;idx.push(a,c,b,b,c,d)}
    var g=new T.BufferGeometry();g.setAttribute('position',new T.Float32BufferAttribute(pos,3));g.setAttribute('uv',new T.Float32BufferAttribute(uv,2));
    g.setAttribute('luv',new T.Float32BufferAttribute(luv,2));g.setAttribute('color',new T.Float32BufferAttribute(col,3));g.setIndex(idx);g.computeVertexNormals();
    /* make sure faces point up */
    var nr=g.attributes.normal;if(nr.getY(0)<0){for(var k=0;k<idx.length;k+=3){var t=idx[k+1];idx[k+1]=idx[k+2];idx[k+2]=t}g.setIndex(idx);g.computeVertexNormals()}
    return g}
  function field(id,type,P,N){var g=fieldGeo(P,N||18,.45,TILE[type]);var m=new T.Mesh(g,FM[type]);m.receiveShadow=true;scene.add(m);var f={id:id,type:type,P:P,mesh:m};fields.push(f);return f}
  /* the hero fields, close to the camera */
  var A=field('A','plough',[[-780,470],[-95,480],[-60,95],[-735,118]],22);
  var B=field('B','wheat',[[-45,485],[770,470],[724,92],[-22,100]],26);
  var C=field('C','wheat',[[18,62],[650,48],[575,-205],[52,-188]],22);
  var D=field('D','stubble',[[-715,86],[-40,68],[-18,-168],[-672,-150]],20);
  field('E','green',[[-1520,452],[-805,468],[-760,120],[-1470,98]]);
  field('F','wheat',[[795,462],[1520,432],[1450,62],[752,82]]);
  field('G','meadow',[[-1430,86],[-735,104],[-690,-160],[-1370,-170]]);
  field('H','plough',[[690,36],[1420,26],[1350,-236],[610,-216]]);
  field('I','stubble',[[-2300,440],[-1560,455],[-1500,100],[-2240,90]]);
  field('J','wheat',[[1560,430],[2320,405],[2240,40],[1490,58]]);
  field('K','wheat',[[-2230,80],[-1470,92],[-1410,-180],[-2160,-190]]);
  field('L','green',[[1390,22],[2160,10],[2090,-250],[1330,-240]]);
  /* patchwork beyond the farmstead */
  var types=['wheat','stubble','plough','green','meadow','wheat','stubble'];
  for(var zr=-500,row=0;zr>-1500;row++){var dz=rr(200,280),x0=-2700+rr(-80,80);
    while(x0<2700){var w=rr(260,470);if(!(zr>-560&&x0>-420&&x0<380)){var sk=rr(-30,30),sk2=rr(-30,30);
      field('far',types[(rnd()*types.length)|0],[[x0+sk,zr],[x0+w+sk,zr+rr(-12,12)],[x0+w+sk2,zr-dz+rr(-12,12)],[x0+sk2,zr-dz]],12)}
      x0+=w+rr(10,18)}
    zr-=dz+rr(10,16)}

  /* tracks */
  var roadMat=new T.MeshStandardMaterial({map:TX.road,roughness:1,envMapIntensity:.5,polygonOffset:true,polygonOffsetFactor:-1,polygonOffsetUnits:-2});
  function road(pts,w){var pos=[],uv=[],idx=[],L=0;for(var i=0;i<pts.length;i++){var p=pts[i],q=pts[Math.min(i+1,pts.length-1)],o=pts[Math.max(i-1,0)];
      var dx=q[0]-o[0],dz=q[1]-o[1],l=Math.hypot(dx,dz)||1,nx=-dz/l*w/2,nz=dx/l*w/2;if(i>0)L+=Math.hypot(p[0]-pts[i-1][0],p[1]-pts[i-1][1]);
      pos.push(p[0]+nx,H(p[0]+nx,p[1]+nz)+.25,p[1]+nz,p[0]-nx,H(p[0]-nx,p[1]-nz)+.25,p[1]-nz);uv.push(0,L/w,1,L/w);
      if(i>0){var a=(i-1)*2;idx.push(a,a+2,a+1,a+1,a+2,a+3)}}
    var g=new T.BufferGeometry();g.setAttribute('position',new T.Float32BufferAttribute(pos,3));g.setAttribute('uv',new T.Float32BufferAttribute(uv,2));g.setIndex(idx);g.computeVertexNormals();
    if(g.attributes.normal.getY(0)<0){g.index.array.reverse();g.computeVertexNormals()}
    var m=new T.Mesh(g,roadMat);m.receiveShadow=true;scene.add(m)}
  function line(a,b,n){var r=[];for(var i=0;i<=n;i++)r.push([a[0]+(b[0]-a[0])*i/n,a[1]+(b[1]-a[1])*i/n]);return r}
  road(line([-2600,94],[2600,70],120),13);
  road(line([-30,84],[-14,-250],30),11);
  road(line([-14,-250],[-60,-470],12),9);

  /* ---------- merged geometry helper ---------- */
  function merge(parts){var P=[],N=[],C=[];parts.forEach(function(pr){var g=pr.g.index?pr.g.toNonIndexed():pr.g;var p=g.attributes.position,n=g.attributes.normal,c=pr.c;
      for(var i=0;i<p.count;i++){P.push(p.getX(i),p.getY(i),p.getZ(i));N.push(n.getX(i),n.getY(i),n.getZ(i));
        var k=pr.shade?pr.shade(p.getY(i)):1;C.push(c.r*k,c.g*k,c.b*k)}});
    var g=new T.BufferGeometry();g.setAttribute('position',new T.Float32BufferAttribute(P,3));g.setAttribute('normal',new T.Float32BufferAttribute(N,3));g.setAttribute('color',new T.Float32BufferAttribute(C,3));return g}
  function blob(ws,hs,sd){var g=new T.SphereGeometry(1,ws,hs),p=g.attributes.position,v=new T.Vector3();
    for(var i=0;i<p.count;i++){v.fromBufferAttribute(p,i);var n=1+.16*Math.sin(v.x*3.1+sd)*Math.cos(v.y*2.6+sd*1.3)+.1*Math.sin(v.z*4.7+sd*2.1);v.multiplyScalar(n);p.setXYZ(i,v.x,v.y,v.z)}
    g.computeVertexNormals();return g}
  function at(g,x,y,z,sx,sy,sz){g.scale(sx,sy,sz);g.translate(x,y,z);return g}
  var WHITE=new T.Color(1,1,1),BARK=new T.Color('#4a3a2a');
  function crownShade(lo,hi){return function(y){return .55+.45*sst(lo,hi,y)}}
  var treeGeo=merge([
    {g:at(new T.CylinderGeometry(.32,.5,5,6),0,2.5,0,1,1,1),c:BARK},
    {g:at(blob(12,9,1),0,7.6,0,4.1,4.5,4.1),c:WHITE,shade:crownShade(3.5,11)},
    {g:at(blob(10,8,4),2.3,6.2,1.1,2.8,3,2.8),c:WHITE,shade:crownShade(3.5,11)},
    {g:at(blob(10,8,7),-1.9,8.9,-1,2.6,3.1,2.6),c:WHITE,shade:crownShade(3.5,11)}]);
  var farGeo=merge([{g:at(blob(7,5,2),0,5,0,3.6,4.4,3.6),c:WHITE,shade:crownShade(1,9)}]);
  var leafMat=new T.MeshStandardMaterial({vertexColors:true,roughness:.92,envMapIntensity:.7});
  var GREENS=['#4b6631','#58743a','#3e5629','#64803f','#6f8744','#52693a'].map(function(c){return new T.Color(c)});
  var near=[],farT=[];
  function addTree(list,x,z,s,narrow){list.push({x:x,z:z,s:s,n:narrow,c:GREENS[(rnd()*GREENS.length)|0].clone().multiplyScalar(.85+rnd()*.3),r:rnd()*6.28})}
  function hedge(a,b,step,smin,smax,gap,narrow,list){var L=Math.hypot(b[0]-a[0],b[1]-a[1]),n=Math.floor(L/step);
    for(var i=0;i<=n;i++){var t=i/n,x=a[0]+(b[0]-a[0])*t+rr(-2.5,2.5),z=a[1]+(b[1]-a[1])*t+rr(-2.5,2.5);
      if(gap&&vnoise(x*.012+a[0],z*.012)<gap)continue;addTree(list||near,x,z,rr(smin,smax),narrow)}}
  hedge([-1700,-438],[1700,-470],8.5,.85,1.35,.28);
  hedge([-1700,-452],[1700,-484],11,.8,1.2,.4);
  hedge([-792,485],[-748,108],9,.8,1.25,.22);
  hedge([782,480],[736,96],9,.8,1.2,.25);
  hedge([700,40],[618,-226],10,.8,1.2,.3);
  hedge([-1460,470],[-1400,100],12,.8,1.1,.35);
  hedge([1520,450],[1460,70],12,.8,1.1,.35);
  hedge([-330,-212],[-345,-420],7,1,1.25,0,true);       /* poplar windbreak by the farmstead */
  hedge([250,-230],[258,-420],8,.95,1.2,.15,true);
  for(i=0;i<70;i++)addTree(near,rr(-420,330),rr(-470,-395),rr(.8,1.4));
  for(i=0;i<16;i++)addTree(near,rr(-260,-120),rr(-200,-120),rr(.9,1.3));
  [[-560,40],[310,62],[-260,94],[540,470],[-420,480]].forEach(function(p){for(var k=0;k<3;k++)addTree(near,p[0]+rr(-14,14),p[1]+rr(-10,10),rr(1.1,1.6))});
  /* distant woods on the hills */
  var FAR=small?3200:7200;
  for(var tries=0;farT.length<FAR&&tries<90000;tries++){var x=rr(-4800,4800),z=rr(-6000,-520);
    var wood=fbm(x*.0016+5,z*.0016+1),edge=Math.abs(vnoise(x*.004,z*.004)-.5);
    if(wood>.57)addTree(farT,x,z,rr(1.5,2.3)*(1+Math.min(1.2,-z/3500)))}
  for(i=0;i<30;i++){var zz=rr(-1500,-640),xa=rr(-2800,1800);hedge([xa,zz],[xa+rr(500,1400),zz+rr(-50,50)],5,1.4,2.1,.22,false,farT)}
  for(i=0;i<14;i++){var xx=rr(-2400,2400),za=rr(-1500,-600);hedge([xx,za],[xx+rr(-80,80),za-rr(250,600)],5.5,1.4,2,.22,false,farT)}
  function instTrees(geo,list,shadow){var m=new T.InstancedMesh(geo,leafMat,list.length),o=new T.Object3D();
    list.forEach(function(t,i){o.position.set(t.x,H(t.x,t.z)-.3,t.z);o.rotation.set(0,t.r,0);if(t.n)o.scale.set(t.s*.42,t.s*1.85,t.s*.42);else o.scale.set(t.s,t.s*(.9+rnd()*.25),t.s);
      o.updateMatrix();m.setMatrixAt(i,o.matrix);m.setColorAt(i,t.c)});
    m.castShadow=shadow;m.frustumCulled=false;scene.add(m);return m}
  instTrees(treeGeo,near,true);instTrees(farGeo,farT,false);

  /* ---------- farmstead ---------- */
  var MAT={wall:new T.MeshStandardMaterial({color:'#e9ebeb',map:TX.wall,roughness:.82}),
    roof:new T.MeshStandardMaterial({color:'#dfe6ef',map:TX.roof,roughness:.5,metalness:.3,envMapIntensity:.7}),
    roofR:new T.MeshStandardMaterial({color:'#b9705a',roughness:.75}),
    silo:new T.MeshStandardMaterial({color:'#ffffff',map:TX.silo,roughness:.32,metalness:.7}),
    steel:new T.MeshStandardMaterial({color:'#7e868d',roughness:.55,metalness:.6}),
    dark:new T.MeshStandardMaterial({color:'#2b3236',roughness:.6}),
    glow:new T.MeshBasicMaterial({color:'#ffe3b5',fog:true}),
    concrete:new T.MeshStandardMaterial({color:'#cfcbc0',roughness:.95})};
  function shadowAll(o){o.traverse(function(c){if(c.isMesh){c.castShadow=true;c.receiveShadow=true}})}
  function barn(x,z,w,d,h,rot,opts){opts=opts||{};var g=new T.Group();var y0=H(x,z);
    var walls=new T.Mesh(new T.BoxGeometry(w,h,d),MAT.wall);walls.position.y=h/2;g.add(walls);
    var rise=w*(opts.pitch||.24),sh=new T.Shape();sh.moveTo(-w/2,0);sh.lineTo(0,rise);sh.lineTo(w/2,0);sh.lineTo(-w/2,0);
    var gable=new T.Mesh(new T.ExtrudeGeometry(sh,{depth:d,bevelEnabled:false}),MAT.wall);gable.position.set(0,h,-d/2);g.add(gable);
    var sl=Math.hypot(w/2,rise)+1.6,an=Math.atan2(rise,w/2);
    [-1,1].forEach(function(sg){var r=new T.Mesh(new T.BoxGeometry(sl,.7,d+3),opts.red?MAT.roofR:MAT.roof);r.position.set(sg*(w/4),h+rise/2+.3,0);r.rotation.z=-sg*an;g.add(r)});
    if(opts.door){var dr=new T.Mesh(new T.PlaneGeometry(w*.34,h*.72),MAT.glow);dr.position.set(opts.doorX||0,h*.36,d/2+.06);g.add(dr)}
    if(opts.door2){var d2=new T.Mesh(new T.PlaneGeometry(w*.22,h*.6),MAT.dark);d2.position.set(-w*.28,h*.3,d/2+.06);g.add(d2)}
    var pad=new T.Mesh(new T.BoxGeometry(w+14,.6,d+14),MAT.concrete);pad.position.y=.1;g.add(pad);
    g.position.set(x,y0,z);g.rotation.y=rot;shadowAll(g);scene.add(g);return g}
  function shed(x,z,w,d,h,rot){var g=new T.Group(),y0=H(x,z);
    for(var i=0;i<=4;i++)[-1,1].forEach(function(s){var p=new T.Mesh(new T.BoxGeometry(.7,h,.7),MAT.steel);p.position.set(-w/2+w*i/4,h/2,s*d/2);g.add(p)});
    var r=new T.Mesh(new T.BoxGeometry(w+3,.6,d+4),MAT.roof);r.position.y=h+1.2;r.rotation.x=.08;g.add(r);
    var back=new T.Mesh(new T.BoxGeometry(w,h*.55,.5),MAT.wall);back.position.set(0,h*.27,-d/2);g.add(back);
    for(i=0;i<9;i++){var b=new T.Mesh(new T.CylinderGeometry(1.5,1.5,1.8,14),new T.MeshStandardMaterial({color:'#d8bd7c',map:TX.stubble,roughness:.95}));b.rotation.z=Math.PI/2;b.position.set(-w/2+5+i*3.4,1.5,rr(-2,3));g.add(b)}
    g.position.set(x,y0,z);g.rotation.y=rot;shadowAll(g);scene.add(g)}
  function silo(x,z,r,h){var g=new T.Group(),y0=H(x,z);
    var b=new T.Mesh(new T.CylinderGeometry(r,r,h,32,1,true),MAT.silo);b.position.y=h/2+3;g.add(b);
    var top=new T.Mesh(new T.ConeGeometry(r*1.04,r*.75,32),MAT.silo);top.position.y=h+3+r*.37;g.add(top);
    var hop=new T.Mesh(new T.CylinderGeometry(r,1.2,3,24),MAT.steel);hop.position.y=1.5;g.add(hop);
    for(var i=0;i<4;i++){var l=new T.Mesh(new T.BoxGeometry(.5,3,.5),MAT.steel);l.position.set(Math.cos(i*1.57+.78)*r*.8,1.5,Math.sin(i*1.57+.78)*r*.8);g.add(l)}
    var lad=new T.Mesh(new T.BoxGeometry(.5,h,.3),MAT.steel);lad.position.set(r+.3,h/2+3,0);g.add(lad);
    g.position.set(x,y0,z);shadowAll(g);scene.add(g);return g}
  var R=-.06;
  barn(-120,-318,74,34,13,R,{door:true,doorX:8,door2:true});
  barn(-196,-262,44,24,9,R+.03,{red:true,door2:true,pitch:.3});
  barn(-38,-372,58,26,11,R,{door2:true});
  shed(150,-300,64,22,10,R+.04);
  [0,1,2,3].forEach(function(i){silo(30+i*17.5,-318-i*1.2,7.2,32)});
  silo(108,-336,5,22);silo(120,-336,5,22);
  /* elevator leg + conveyor between silos */
  var leg=new T.Mesh(new T.BoxGeometry(2.4,52,2.4),MAT.steel);leg.position.set(16,H(16,-306)+26,-306);leg.castShadow=true;scene.add(leg);
  var conv=new T.Mesh(new T.BoxGeometry(70,1.4,1.4),MAT.steel);conv.position.set(52,H(52,-312)+46,-312);conv.castShadow=true;scene.add(conv);
  /* house with red roof */
  barn(-262,-338,26,16,7,R+.1,{red:true,pitch:.42,door2:true});
  /* weather station */
  var ws=new T.Group(),wy=H(-12,-214);
  var mast=new T.Mesh(new T.CylinderGeometry(.18,.22,11,8),MAT.steel);mast.position.y=5.5;ws.add(mast);
  var pan=new T.Mesh(new T.BoxGeometry(2.6,.12,1.8),new T.MeshStandardMaterial({color:'#1d2c4a',roughness:.3,metalness:.4}));pan.position.set(0,6,1.1);pan.rotation.x=-.7;ws.add(pan);
  var box=new T.Mesh(new T.BoxGeometry(1.1,1.4,.6),MAT.wall);box.position.set(0,3.5,.5);ws.add(box);
  var arm=new T.Mesh(new T.BoxGeometry(3.4,.14,.14),MAT.steel);arm.position.y=10.6;ws.add(arm);
  var cups=new T.Group();cups.position.set(1.6,11.2,0);for(i=0;i<3;i++){var cp=new T.Mesh(new T.SphereGeometry(.28,8,6),MAT.wall);cp.position.set(Math.cos(i*2.09)*.7,0,Math.sin(i*2.09)*.7);cups.add(cp)}ws.add(cups);
  ws.position.set(-12,wy,-214);shadowAll(ws);scene.add(ws);

  /* irrigation basin */
  var bsh=new T.Shape();for(i=0;i<=48;i++){var a=i/48*Math.PI*2,rw=150*(1+.08*Math.sin(a*3)),rd=62*(1+.1*Math.cos(a*2));if(i===0)bsh.moveTo(Math.cos(a)*rw,Math.sin(a)*rd);else bsh.lineTo(Math.cos(a)*rw,Math.sin(a)*rd)}
  var bx=800,bz=-330,by=H(bx,bz)+.7;
  var bank=new T.Mesh(new T.ShapeGeometry(bsh,1),new T.MeshStandardMaterial({color:'#b6a77b',roughness:1,polygonOffset:true,polygonOffsetFactor:-2,polygonOffsetUnits:-4}));
  bank.rotation.x=-Math.PI/2;bank.scale.set(1.08,1.14,1);bank.position.set(bx,by-.2,bz);bank.receiveShadow=true;scene.add(bank);
  var water=new T.Mesh(new T.ShapeGeometry(bsh,1),new T.MeshStandardMaterial({color:'#7e9ea6',roughness:.08,metalness:.25,envMapIntensity:1.4,polygonOffset:true,polygonOffsetFactor:-3,polygonOffsetUnits:-6}));
  water.rotation.x=-Math.PI/2;water.position.set(bx,by,bz);water.receiveShadow=true;scene.add(water);
  for(i=0;i<26;i++){var a2=rnd()*6.28;addTree(near,bx+Math.cos(a2)*175,bz+Math.sin(a2)*80,rr(.6,1))}

  /* ---------- power line ---------- */
  var pylMat=new T.MeshStandardMaterial({color:'#666c71',roughness:.6,metalness:.4});
  var latMat=new T.LineBasicMaterial({color:'#5c6267',transparent:true,opacity:.85});
  function beam(a,b,t){var d=new T.Vector3().subVectors(b,a),m=new T.Mesh(new T.BoxGeometry(t,t,d.length()),pylMat);m.position.copy(a).add(b).multiplyScalar(.5);m.lookAt(b);return m}
  var attach=[[-12,46],[12,46],[-9,56],[9,56],[0,66]];
  function pylon(x,z,rot){var g=new T.Group(),y0=H(x,z),HT=64,lv=[];
    function corner(y){var w=y<40?6.2-(y/40)*3.6:2.6-(y-40)/HT*1.2;return [[-w,-w],[w,-w],[w,w],[-w,w]].map(function(c){return new T.Vector3(c[0],y,c[1])})}
    var levels=[0,7,14,21,28,34,40,46,52,58,HT];levels.forEach(function(y){lv.push(corner(y))});
    for(var k=0;k<4;k++){for(var l=0;l<levels.length-1;l++)g.add(beam(lv[l][k],lv[l+1][k],.55))}
    var lp=[];for(l=0;l<levels.length-1;l++)for(k=0;k<4;k++){var a=lv[l][k],b=lv[l][(k+1)%4],c=lv[l+1][k],d=lv[l+1][(k+1)%4];lp.push(a,d,b,c,c,d)}
    g.add(new T.LineSegments(new T.BufferGeometry().setFromPoints(lp),latMat));
    [[46,12],[56,9]].forEach(function(r){g.add(beam(new T.Vector3(-r[1],r[0],0),new T.Vector3(r[1],r[0],0),.6));
      var ap=[];[-1,1].forEach(function(s){ap.push(new T.Vector3(s*r[1],r[0],0),new T.Vector3(s*2.4,r[0]-5,0))});g.add(new T.LineSegments(new T.BufferGeometry().setFromPoints(ap),latMat))});
    var ins=[];attach.slice(0,4).forEach(function(p){ins.push(new T.Vector3(p[0],p[1],0),new T.Vector3(p[0],p[1]-3.2,0))});
    g.add(new T.LineSegments(new T.BufferGeometry().setFromPoints(ins),new T.LineBasicMaterial({color:'#3d4246'})));
    g.position.set(x,y0,z);g.rotation.y=rot;g.traverse(function(c){if(c.isMesh)c.castShadow=true});scene.add(g);return g}
  var PY=[[-1500,-210],[-760,-372],[-30,-545],[700,-712],[1430,-880],[2160,-1050]],pyl=[];
  PY.forEach(function(p,i){var nx=PY[Math.min(i+1,PY.length-1)],pv=PY[Math.max(i-1,0)];var ang=Math.atan2(nx[1]-pv[1],nx[0]-pv[0]);pyl.push(pylon(p[0],p[1],-ang))});
  var wireMat=new T.LineBasicMaterial({color:'#4b5054',transparent:true,opacity:.7});
  for(var pi=0;pi<pyl.length-1;pi++){pyl[pi].updateMatrixWorld();pyl[pi+1].updateMatrixWorld();
    attach.forEach(function(ap,k){var a=new T.Vector3(ap[0],ap[1]-(k<4?3.2:0),0).applyMatrix4(pyl[pi].matrixWorld),b=new T.Vector3(ap[0],ap[1]-(k<4?3.2:0),0).applyMatrix4(pyl[pi+1].matrixWorld);
      var pts=[];for(var s=0;s<=40;s++){var t=s/40,p=a.clone().lerp(b,t);p.y-=a.distanceTo(b)*.03*4*t*(1-t);pts.push(p)}
      scene.add(new T.Line(new T.BufferGeometry().setFromPoints(pts),wireMat))})}

  /* ---------- round bales on the stubble ---------- */
  var baleGeo=new T.CylinderGeometry(1.6,1.6,1.9,16);baleGeo.rotateZ(Math.PI/2);
  var bales=new T.InstancedMesh(baleGeo,new T.MeshStandardMaterial({color:'#e2c98a',map:TX.stubble,roughness:.95}),84),bo=new T.Object3D(),bc=0;
  for(var br=0;br<7;br++)for(var bi=0;bi<12;bi++){if(rnd()<.18)continue;var q=quadPt(D.P,.07+bi*.078+rr(-.02,.02),.12+br*.12+rr(-.02,.02));
    bo.position.set(q[0],H(q[0],q[1])+1.95,q[1]);bo.rotation.set(0,rr(0,3.14),0);bo.scale.setScalar(1.6);bo.updateMatrix();bales.setMatrixAt(bc++,bo.matrix)}
  bales.count=bc;bales.castShadow=true;bales.receiveShadow=true;scene.add(bales);

  /* ---------- vehicles ---------- */
  function boxm(w,h,d,mat,x,y,z){var m=new T.Mesh(new T.BoxGeometry(w,h,d),mat);m.position.set(x,y,z);return m}
  function wheel(r,w,x,y,z){var m=new T.Mesh(new T.CylinderGeometry(r,r,w,18),new T.MeshStandardMaterial({color:'#1c1e1f',roughness:.85}));m.rotation.z=Math.PI/2;m.position.set(x,y,z);return m}
  var CG=new T.MeshStandardMaterial({color:'#2f7f45',roughness:.45,metalness:.25}),GLASS=new T.MeshStandardMaterial({color:'#1b2a30',roughness:.08,metalness:.6}),WH=new T.MeshStandardMaterial({color:'#eef0ee',roughness:.5});
  /* combine harvester: local +z is forward */
  var combine=new T.Group();
  combine.add(boxm(8.4,5.6,12,CG,0,5.2,0),boxm(7.6,3.2,8,CG,0,9.4,-1.6),boxm(5,4.4,4.6,GLASS,0,10.2,4.2),boxm(5.6,.4,5.2,WH,0,12.6,4.2),
    boxm(3.4,3.2,6,CG,0,3.4,7.2),boxm(26,1.5,4,new T.MeshStandardMaterial({color:'#8f979c',roughness:.5,metalness:.4}),0,1.6,10.6),
    boxm(26.4,.5,1.2,CG,0,3.2,9),wheel(2.9,2.1,-4.9,2.9,3.2),wheel(2.9,2.1,4.9,2.9,3.2),wheel(1.8,1.4,-4.2,1.8,-4.4),wheel(1.8,1.4,4.2,1.8,-4.4));
  var reel=new T.Mesh(new T.CylinderGeometry(1.4,1.4,25,10,1,false),new T.MeshStandardMaterial({color:'#c4472f',roughness:.6}));reel.rotation.z=Math.PI/2;reel.position.set(0,3.6,11.4);combine.add(reel);
  var auger=boxm(.9,.9,13,CG,-5.4,10.2,-1);auger.rotation.y=-1.2;auger.position.set(-9,10.4,-.5);combine.add(auger);
  combine.scale.setScalar(1.35);shadowAll(combine);scene.add(combine);
  /* harvested swaths that grow behind the combine */
  var LANE=42,NL=6,swaths=[],SEG=90,swMat=new T.MeshStandardMaterial({map:TX.stubble,bumpMap:TX.stubble,bumpScale:.6,roughness:.96,envMapIntensity:.55,polygonOffset:true,polygonOffsetFactor:-3,polygonOffsetUnits:-6});
  var LX0=60,LX1=600;
  function laneZ(k){return -172+k*LANE}
  for(var k=0;k<NL;k++){var zc=laneZ(k),pos=[],uv=[],idx=[];for(var s=0;s<=SEG;s++){var x=LX0+(LX1-LX0)*s/SEG;[zc-LANE/2-.5,zc+LANE/2+.5].forEach(function(z){pos.push(x,H(x,z)+.62,z);uv.push(x/40,z/40)})}
    for(s=0;s<SEG;s++){var a=s*2;idx.push(a,a+1,a+2,a+2,a+1,a+3)}
    var g=new T.BufferGeometry();g.setAttribute('position',new T.Float32BufferAttribute(pos,3));g.setAttribute('uv',new T.Float32BufferAttribute(uv,2));g.setIndex(idx);g.computeVertexNormals();
    if(g.attributes.normal.getY(0)<0){g.index.array.reverse();g.computeVertexNormals()}
    var m=new T.Mesh(g,swMat);m.receiveShadow=true;m.visible=false;scene.add(m);swaths.push(m)}
  var harvest={lane:0,x:LX0,dir:1,turn:-1};
  /* dust behind the combine */
  var dustTex=(function(){var c=document.createElement('canvas');c.width=c.height=64;var g=c.getContext('2d'),gr=g.createRadialGradient(32,32,0,32,32,32);gr.addColorStop(0,'rgba(255,255,255,1)');gr.addColorStop(1,'rgba(255,255,255,0)');g.fillStyle=gr;g.fillRect(0,0,64,64);return new T.CanvasTexture(c)})();
  var dust=[];for(i=0;i<22;i++){var sp=new T.Sprite(new T.SpriteMaterial({map:dustTex,color:'#e9dcb6',transparent:true,depthWrite:false,opacity:0}));sp.userData={life:1,vx:0,vy:0,vz:0};scene.add(sp);dust.push(sp)}
  var dustI=0,dustT=0;
  /* tractor + trailer on the main track */
  var tractor=new T.Group(),TR=new T.MeshStandardMaterial({color:'#2f6f3c',roughness:.5,metalness:.2});
  tractor.add(boxm(3,2.6,6,TR,0,3,1.6),boxm(3.2,3.4,3.2,GLASS,0,5.6,-1),boxm(3.6,.3,3.6,WH,0,7.4,-1),wheel(2.1,1.3,-2.2,2.1,-1.2),wheel(2.1,1.3,2.2,2.1,-1.2),wheel(1.2,.9,-1.9,1.2,3.4),wheel(1.2,.9,1.9,1.2,3.4),
    boxm(4.6,2.8,9,new T.MeshStandardMaterial({color:'#8c6a3e',roughness:.8}),0,3.4,-9.5),wheel(1.3,.9,-2.5,1.3,-9),wheel(1.3,.9,2.5,1.3,-11));
  tractor.scale.setScalar(1.25);shadowAll(tractor);scene.add(tractor);
  /* tanker parked by the silos */
  var truck=new T.Group();truck.add(boxm(3.4,3.4,3.6,WH,0,3,5.4),boxm(3.6,.5,13,MAT.dark,0,1.4,-1),wheel(1.1,.8,-1.6,1.1,5),wheel(1.1,.8,1.6,1.1,5),wheel(1.1,.8,-1.6,1.1,-4),wheel(1.1,.8,1.6,1.1,-4));
  var tank=new T.Mesh(new T.CylinderGeometry(1.9,1.9,10,18),new T.MeshStandardMaterial({color:'#9fb4c9',roughness:.25,metalness:.7}));tank.rotation.x=Math.PI/2;tank.position.set(0,3.6,-1.4);truck.add(tank);
  truck.position.set(68,H(68,-286),-286);truck.rotation.y=1.45;truck.scale.setScalar(1.25);shadowAll(truck);scene.add(truck);

  /* ---------- satellite scan of parcel C ---------- */
  var scanU={uT:{value:0},uA:{value:1}};
  var scanMat=new T.ShaderMaterial({uniforms:scanU,transparent:true,depthWrite:false,polygonOffset:true,polygonOffsetFactor:-5,polygonOffsetUnits:-8,
    vertexShader:'attribute vec2 luv;varying vec2 vL;varying vec3 vW;void main(){vL=luv;vec4 w=modelMatrix*vec4(position,1.0);vW=w.xyz;gl_Position=projectionMatrix*viewMatrix*w;}',
    fragmentShader:'uniform float uT,uA;varying vec2 vL;varying vec3 vW;'+
      'float h(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}'+
      'float n(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.0-2.0*f);return mix(mix(h(i),h(i+vec2(1,0)),f.x),mix(h(i+vec2(0,1)),h(i+vec2(1,1)),f.x),f.y);}'+
      'void main(){vec2 e=min(vL,1.0-vL);float ed=min(e.x,e.y);float edge=1.0-smoothstep(0.0,.006,ed);float inner=1.0-smoothstep(.006,.03,ed);'+
      'vec2 g=abs(fract(vL*vec2(28.0,14.0))-.5);float grid=smoothstep(.44,.5,max(g.x,g.y));'+
      'float sw=fract(uT*.075);float d=vL.x-sw;float band=exp(-abs(d)*55.0);float trail=smoothstep(-.35,0.0,d)*step(d,0.0);'+
      'float nd=n(vW.xz*.022)*.6+n(vW.xz*.06)*.4;'+
      'vec3 c=mix(vec3(.02,.58,.56),vec3(.22,.86,.74),nd);c=mix(c,vec3(.8,1.0,.95),band*.8+edge*.7);'+
      'float a=uA*(.40+.16*smoothstep(.25,.85,nd)+grid*.10*(.3+trail)+inner*.18+edge*.6+band*.3);gl_FragColor=vec4(c,a);}'});
  var scanMesh=new T.Mesh(fieldGeo(C.P,40,1.2,30),scanMat);scanMesh.renderOrder=5;scene.add(scanMesh);
  /* light wall rising from the parcel outline */
  (function(){var pos=[],uv=[],P=C.P;for(var k=0;k<4;k++){var a=P[k],b=P[(k+1)%4];for(var s=0;s<=20;s++){var t=s/20,x=a[0]+(b[0]-a[0])*t,z=a[1]+(b[1]-a[1])*t,y=H(x,z)+1;pos.push(x,y,z,x,y+6,z);uv.push(t,0,t,1)}}
    var idx=[];for(k=0;k<4;k++)for(var s2=0;s2<20;s2++){var o=k*42+s2*2;idx.push(o,o+1,o+2,o+2,o+1,o+3)}
    var g=new T.BufferGeometry();g.setAttribute('position',new T.Float32BufferAttribute(pos,3));g.setAttribute('uv',new T.Float32BufferAttribute(uv,2));g.setIndex(idx);
    var m=new T.Mesh(g,new T.ShaderMaterial({uniforms:scanU,transparent:true,depthWrite:false,side:T.DoubleSide,blending:T.AdditiveBlending,
      vertexShader:'varying vec2 vU;void main(){vU=uv;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.0);}',
      fragmentShader:'uniform float uT,uA;varying vec2 vU;void main(){float f=pow(1.0-vU.y,2.4);gl_FragColor=vec4(vec3(.3,.95,.82)*f*.28*uA,1.0);}'}));
    m.renderOrder=6;scene.add(m)})();
  /* sweep line crossing the parcel */
  var sweep=new T.Mesh(new T.PlaneGeometry(1,22),new T.ShaderMaterial({transparent:true,depthWrite:false,side:T.DoubleSide,blending:T.AdditiveBlending,uniforms:{uA:{value:1}},
    vertexShader:'varying vec2 vU;void main(){vU=uv;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.0);}',
    fragmentShader:'uniform float uA;varying vec2 vU;void main(){float f=pow(1.0-vU.y,2.2)*(1.0-pow(abs(vU.x-.5)*2.0,6.0));gl_FragColor=vec4(vec3(.55,1.0,.9)*f*.45*uA,1.0);}'}));
  sweep.renderOrder=7;scene.add(sweep);

  /* ---------- hotspots ---------- */
  var HS=[
    {k:'01',t:'Détecter 15 jours avant',d:"Chaque passage Sentinel-2 est analysé. Un stress hydrique ou une carence apparaît sur la carte avant d'être visible au champ.",p:function(v){var q=quadPt(C.P,.52,.5);v.set(q[0],H(q[0],q[1])+14,q[1])}},
    {k:'02',t:'Réduire les coûts',d:"L'irrigation et la fertilisation suivent le besoin réel de chaque secteur, pas la moyenne de la parcelle.",p:function(v){v.set(bx-30,by+12,bz)}},
    {k:'03',t:'Produire en préservant',d:"Plus de rendement avec moins d'intrants : l'eau et l'azote vont là où la culture en a vraiment besoin.",p:function(v){var q=quadPt(A.P,.45,.42);v.set(q[0],H(q[0],q[1])+12,q[1])}},
    {k:'04',t:'Décider sur des faits',d:"Analyses de sol, foliaires et d'eau, croisées avec l'image et le climat : chaque décision repose sur des données objectives.",p:function(v){v.set(56,H(56,-318)+50,-318)}},
    {k:'',t:'Climat en temps réel',d:"Température, pluie, humidité et évapotranspiration, mesurées et prévues pour chaque exploitation.",p:function(v){v.set(-12,wy+17,-214)}},
    {k:'',t:'Toute la saison',d:"De la levée à la récolte, Firmaty suit vos parcelles à chaque nouvelle image, mois après mois.",p:function(v){v.copy(combine.position);v.y+=22}}
  ];
  var openHs=null;
  HS.forEach(function(h,i){var b=document.createElement('div');b.className='f3-hs';
    b.innerHTML='<button type="button" aria-expanded="false" aria-label="'+h.t+'"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M12 5v14M5 12h14"/></svg></button><i aria-hidden="true"></i>'+
      '<div class="f3-pop" role="dialog" aria-label="'+h.t+'">'+(h.k?'<span>'+h.k+'</span>':'')+'<b>'+h.t+'</b><p>'+h.d+'</p></div>';
    var btn=b.querySelector('button');btn.addEventListener('click',function(e){e.stopPropagation();var o=!b.classList.contains('open');closeHs();if(o){b.classList.add('open');btn.setAttribute('aria-expanded','true');openHs=b}});
    hotBox.appendChild(b);h.el=b;h.v=new T.Vector3()});
  function closeHs(){if(openHs){openHs.classList.remove('open');openHs.querySelector('button').setAttribute('aria-expanded','false');openHs=null}}
  document.addEventListener('click',function(e){if(openHs&&!openHs.contains(e.target))closeHs()});
  document.addEventListener('keydown',function(e){if(e.key==='Escape')closeHs()});

  /* ---------- camera ---------- */
  var mouse={x:0,y:0,tx:0,ty:0};
  root.addEventListener('pointermove',function(e){if(e.pointerType!=='mouse')return;var r=root.getBoundingClientRect();mouse.tx=(e.clientX-r.left)/r.width-.5;mouse.ty=(e.clientY-r.top)/r.height-.5});
  root.addEventListener('pointerleave',function(){mouse.tx=0;mouse.ty=0});
  var portrait=false,tgt=new T.Vector3();
  function resize(){var w=stage.clientWidth,h=stage.clientHeight;if(!w||!h)return;renderer.setSize(w,h,false);camera.aspect=w/h;portrait=w<h;
    camera.fov=portrait?48:(w/h<1.45?42:36);camera.updateProjectionMatrix()}
  addEventListener('resize',resize);resize();

  /* ---------- loop ---------- */
  var io=new IntersectionObserver(function(es){visible=es[0].isIntersecting},{threshold:0});io.observe(root);
  var clock=0,last=performance.now(),perf={n:0,sum:0,level:0},firstFrames=0;
  var wheatGreen=new T.Color('#a9c06a'),wheatGold=new T.Color('#ffffff'),tmpC=new T.Color();
  var v3=new T.Vector3();
  function adapt(ms){if(perf.level>1||ms>400)return;perf.n++;perf.sum+=ms;if(perf.n<45)return;var avg=perf.sum/perf.n;perf.n=0;perf.sum=0;
    if(avg>30){perf.level++;if(perf.level===1){renderer.setPixelRatio(Math.min(1.25,devicePixelRatio||1))}else{renderer.shadowMap.enabled=false;scene.traverse(function(o){if(o.material)o.material.needsUpdate=true});renderer.setPixelRatio(1)}resize()}}
  function frame(now){requestAnimationFrame(frame);var raw=now-last;last=now;if(!visible||document.hidden)return;
    var dt=Math.min(window.F3_LITE?.5:.05,raw/1000);if(firstFrames>3)adapt(raw);clock+=dt;
    /* season */
    if(!reduce)season.m=(season.m+dt*season.speed)%12;var m=season.m;
    var ripe=sst(3,6.4,m)*(1-sst(9.6,11.6,m));tmpC.copy(wheatGreen).lerp(wheatGold,ripe);FM.wheat.color.copy(tmpC);
    FM.green.color.setScalar(.75+.25*sst(2,5,m)*(1-sst(9,11.5,m)));
    var harvesting=m>6.2&&m<9.6;
    /* camera */
    mouse.x+=(mouse.tx-mouse.x)*Math.min(1,dt*2.2);mouse.y+=(mouse.ty-mouse.y)*Math.min(1,dt*2.2);
    var drift=reduce?0:Math.sin(clock*.045);
    if(portrait){camera.position.set(120+drift*20,128,320);tgt.set(80,14,-250)}
    else{camera.position.set(150+drift*36+mouse.x*50,135+Math.sin(clock*.07)*3-mouse.y*14,400);tgt.set(40+mouse.x*22,27,-250)}
    camera.lookAt(tgt);sky.position.copy(camera.position);
    /* combine harvests lane after lane, then the field is reset in autumn */
    if(harvesting&&!reduce){combine.visible=true;var sp=7.5*dt*(window.F3_LITE?1:1);
      if(harvest.turn<0){harvest.x+=sp*harvest.dir;if(harvest.x>LX1||harvest.x<LX0){harvest.x=Math.max(LX0,Math.min(LX1,harvest.x));harvest.turn=0}}
      else{harvest.turn+=dt/4.5;if(harvest.turn>=1){harvest.turn=-1;harvest.dir*=-1;harvest.lane=(harvest.lane+1)%NL}}
      var lz=laneZ(harvest.lane),cx2=harvest.x,cz2=lz,ry=harvest.dir>0?Math.PI/2:-Math.PI/2;
      if(harvest.turn>=0){var th=harvest.turn*Math.PI,rad=LANE/2;cx2=harvest.x+harvest.dir*Math.sin(th)*rad;cz2=lz-rad+Math.cos(th)*rad;ry=(harvest.dir>0?Math.PI/2:-Math.PI/2)+harvest.dir*th}
      combine.position.set(cx2,H(cx2,cz2)+.4,cz2);combine.rotation.y=ry;reel.rotation.x+=dt*2.4;
      var sw2=swaths[harvest.lane];sw2.visible=true;var prog=harvest.dir>0?(harvest.x-LX0)/(LX1-LX0):1-(harvest.x-LX0)/(LX1-LX0);
      if(harvest.dir>0){sw2.geometry.setDrawRange(0,Math.floor(prog*SEG)*6)}else{var st=Math.floor((1-prog)*SEG);sw2.geometry.setDrawRange(st*6,(SEG-st)*6)}
      dustT+=dt;if(dustT>.18){dustT=0;var p=dust[dustI++%dust.length];p.position.set(cx2-harvest.dir*8*(harvest.turn<0?1:0)+rr(-3,3),H(cx2,cz2)+4,cz2+rr(-6,6));p.userData.life=0;p.userData.vx=rr(-1,1);p.userData.vy=rr(1.5,3);p.userData.vz=rr(-1,1)}
    }else{combine.visible=harvesting;if(m>=10&&m<10.5){swaths.forEach(function(s){s.visible=false});harvest.lane=0;harvest.x=LX0;harvest.dir=1;harvest.turn=-1}}
    if(!harvesting&&!reduce)combine.position.set(-30,H(-30,170),170),combine.rotation.y=Math.PI/2;
    dust.forEach(function(p){var u=p.userData;if(u.life<1){u.life+=dt/3.2;p.position.x+=u.vx*dt*3;p.position.y+=u.vy*dt*3;p.position.z+=u.vz*dt*3;var s=6+u.life*18;p.scale.set(s,s,1);p.material.opacity=Math.sin(u.life*Math.PI)*.38}else p.material.opacity=0});
    /* tractor on the track */
    var tx=-1500+((clock*9)%3000);tractor.position.set(tx,H(tx,84)+.3,84-tx*.0046);tractor.rotation.y=Math.PI/2;
    cups.rotation.y+=dt*4;
    /* scan */
    scanU.uT.value=clock;var sw=(clock*.075)%1;var q1=quadPt(C.P,sw,0),q2=quadPt(C.P,sw,1);
    sweep.position.set((q1[0]+q2[0])/2,H(q1[0],q1[1])+11,(q1[1]+q2[1])/2);sweep.scale.x=Math.hypot(q2[0]-q1[0],q2[1]-q1[1]);sweep.rotation.y=-Math.atan2(q2[1]-q1[1],q2[0]-q1[0]);
    renderer.render(scene,camera);
    if(++firstFrames===3)root.classList.add('f3-live');
    /* hotspots */
    var w=stage.clientWidth,h=stage.clientHeight;
    HS.forEach(function(s,i){if(i===5&&(!combine.visible||portrait)){s.el.style.opacity=0;s.el.style.pointerEvents='none';return}s.p(s.v);v3.copy(s.v).project(camera);
      var x=(v3.x*.5+.5)*w,y=(-v3.y*.5+.5)*h,on=v3.z<1&&x>10&&x<w-10&&y>10&&y<h-10;
      s.el.style.transform='translate3d('+x.toFixed(1)+'px,'+y.toFixed(1)+'px,0)';s.el.style.opacity=on?'':'0';s.el.style.pointerEvents=on?'':'none';
      s.el.classList.toggle('left',x>w*.62);s.el.classList.toggle('up',y>h*.55)});
  }
  requestAnimationFrame(frame);
  }

  /* ---------------- HUD ---------------- */
  function setupHUD(){
    var card=root.querySelector('.f3-card'),plus=root.querySelector('.f3-plus');
    if(plus)plus.addEventListener('click',function(){var o=card.classList.toggle('open');plus.setAttribute('aria-expanded',o?'true':'false');plus.setAttribute('aria-label',o?'Fermer':'Lire notre mission')});
    var months=root.querySelector('.f3-months'),head=root.querySelector('.f3-head'),ticks=root.querySelector('.f3-ticks');
    MONTHS.forEach(function(n,i){var b=document.createElement('button');b.type='button';b.tabIndex=-1;b.innerHTML='<span class="l">'+n+'</span><span class="s">'+n.slice(0,3)+'</span>';
      b.addEventListener('click',function(){season.m=i+.02});months.appendChild(b)});
    var mb=months.children,sparks=root.querySelectorAll('.f3-spark path'),ndvi=root.querySelector('.f3-ndvi'),eau=root.querySelector('.f3-eau');
    var bar=root.querySelector('.f3-bar i');
    var io=new IntersectionObserver(function(es){if(es[0].isIntersecting){root.classList.add('f3-in');if(bar)bar.style.width='2%'}},{threshold:.25});io.observe(root);
    var t=0,lastM=-1;
    function wave(k,tt){var d='';for(var i=0;i<=40;i++){var x=i*3,y;
        if(k===0)y=13+5*Math.sin(i*.42+tt*1.3)+2.2*Math.sin(i*1.3+tt*2.1)+1.2*Math.sin(i*2.9-tt);
        else if(k===1)y=14+3.2*Math.sin(i*.3-tt*1.1)+2.6*Math.sin(i*.9+tt*.7)+1*Math.sin(i*3.1+tt*3);
        else y=16-7*Math.exp(-Math.pow((i-(tt*4)%60+10)/5,2))+1.4*Math.sin(i*.8+tt);
        d+=(i?'L':'M')+x+' '+y.toFixed(2)}return d}
    function tick(){t+=.12;if(visible||!window.THREE){if(!reduce)sparks.forEach(function(p,k){p.setAttribute('d',wave(k,t))});
        var m=season.m;head.style.left=(m/12*100).toFixed(3)+'%';var mi=Math.floor(m);
        if(mi!==lastM){for(var i=0;i<mb.length;i++)mb[i].classList.toggle('on',i===mi);lastM=mi}
        var ripe=Math.max(0,Math.sin((m-1.5)/9*Math.PI));if(ndvi)ndvi.textContent=(.22+.52*ripe).toFixed(2).replace('.',',');
        if(eau)eau.textContent=Math.round(24+9*Math.sin(t*.25+1)+3*Math.sin(t*.9))+' %'}
      if(!window.THREE&&!reduce&&root.classList.contains('f3-nogl'))season.m=(season.m+.12*season.speed)%12}
    if(reduce)sparks.forEach(function(p,k){p.setAttribute('d',wave(k,1))});
    tick();setInterval(tick,120);
  }
})();
