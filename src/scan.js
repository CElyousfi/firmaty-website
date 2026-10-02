/* Firmaty · scène 3D « Observer, croiser, décider »
   Exploitation procédurale (agrumes, avocatiers, champs, bassin, brise-vent) balayée par le satellite. */
(function(){
  var root=document.getElementById('scan3d'); if(!root) return;
  var stage=root.querySelector('.s3-stage'), labelsBox=root.querySelector('.s3-labels');
  var reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
  var small=innerWidth<760;
  function webgl(){try{var c=document.createElement('canvas');return !!(window.WebGLRenderingContext&&(c.getContext('webgl2')||c.getContext('webgl')))}catch(e){return false}}
  if(window.S3_LITE){small=true}
  if(!window.THREE||!webgl()){root.classList.add('s3-nogl');setupUI(null);return}
  var T=THREE;

  /* ---------- helpers ---------- */
  var seed=7;function rnd(){seed=(seed*16807)%2147483647;return (seed-1)/2147483646}
  function hash(x,y){var s=Math.sin(x*127.1+y*311.7)*43758.5453;return s-Math.floor(s)}
  function vnoise(x,y){var xi=Math.floor(x),yi=Math.floor(y),xf=x-xi,yf=y-yi;var u=xf*xf*(3-2*xf),v=yf*yf*(3-2*yf);
    var a=hash(xi,yi),b=hash(xi+1,yi),c=hash(xi,yi+1),d=hash(xi+1,yi+1);return a+(b-a)*u+(c-a)*v+(a-b-c+d)*u*v}
  function fbm(x,y){var s=0,a=.5,f=1;for(var i=0;i<5;i++){s+=a*vnoise(x*f,y*f);f*=2;a*=.5}return s}
  function canvasTex(w,h,draw,rep){var c=document.createElement('canvas');c.width=w;c.height=h;draw(c.getContext('2d'),w,h);var t=new T.CanvasTexture(c);
    if(rep){t.wrapS=t.wrapT=T.RepeatWrapping;t.repeat.set(rep[0],rep[1])}t.anisotropy=4;if(T.sRGBEncoding)t.encoding=T.sRGBEncoding;return t}
  function speckle(g,w,h,base,n,cols,sz){g.fillStyle=base;g.fillRect(0,0,w,h);for(var i=0;i<n;i++){g.fillStyle=cols[(rnd()*cols.length)|0];g.globalAlpha=.08+rnd()*.18;var s=1+rnd()*sz;g.fillRect(rnd()*w,rnd()*h,s,s)}g.globalAlpha=1}

  /* ---------- renderer / scene ---------- */
  var renderer=new T.WebGLRenderer({antialias:!small,alpha:true,powerPreference:'high-performance'});
  renderer.setPixelRatio(Math.min(devicePixelRatio||1,small?1.25:1.75));
  if(T.sRGBEncoding)renderer.outputEncoding=T.sRGBEncoding;
  renderer.toneMapping=T.ACESFilmicToneMapping;renderer.toneMappingExposure=1.05;
  renderer.shadowMap.enabled=!small;renderer.shadowMap.type=T.PCFSoftShadowMap;
  stage.appendChild(renderer.domElement);
  var scene=new T.Scene();
  var HAZE=new T.Color('#e6dcc6');scene.fog=new T.Fog(HAZE,420,1500);
  var camera=new T.PerspectiveCamera(34,1,1,4000);

  var hemi=new T.HemisphereLight('#f4ead2','#56603a',.75);scene.add(hemi);
  var sun=new T.DirectionalLight('#ffd9a0',2.1);sun.position.set(-260,170,-340);
  sun.castShadow=!small;sun.shadow.mapSize.set(2048,2048);var sc=sun.shadow.camera;sc.left=-300;sc.right=300;sc.top=260;sc.bottom=-260;sc.near=50;sc.far=1100;sun.shadow.bias=-.0006;sun.shadow.normalBias=.6;
  scene.add(sun);scene.add(sun.target);
  var fill=new T.DirectionalLight('#9fb6d6',.35);fill.position.set(300,120,260);scene.add(fill);

  /* ---------- terrain: flat farm, rolling hills around ---------- */
  var tg=new T.PlaneGeometry(3600,3600,small?90:150,small?90:150);tg.rotateX(-Math.PI/2);
  var pos=tg.attributes.position,cols=[],cA=new T.Color('#8c8f55'),cB=new T.Color('#b9a874'),cC=new T.Color('#6f7a45'),tmp=new T.Color();
  for(var i=0;i<pos.count;i++){var x=pos.getX(i),z=pos.getZ(i),r=Math.sqrt(x*x/1.3+z*z);
    var k=Math.min(1,Math.max(0,(r-330)/520));k=k*k*(3-2*k);var hgt=k*(fbm(x/420+3,z/420)*190+(z<0?fbm(x/200,z/200)*80:20))-k*30;pos.setY(i,hgt);
    var n=fbm(x/90,z/90);tmp.copy(cA).lerp(cB,n).lerp(cC,Math.max(0,fbm(x/40+9,z/40)-.45));cols.push(tmp.r,tmp.g,tmp.b)}
  tg.setAttribute('color',new T.Float32BufferAttribute(cols,3));tg.computeVertexNormals();
  var ground=new T.Mesh(tg,new T.MeshLambertMaterial({vertexColors:true}));ground.receiveShadow=true;scene.add(ground);

  /* ---------- textures ---------- */
  var texSoil=canvasTex(256,256,function(g,w,h){speckle(g,w,h,'#8a6a46',2600,['#5e432a','#a7845a','#6f5335'],3);g.strokeStyle='rgba(60,40,22,.35)';g.lineWidth=2;for(var y=0;y<h;y+=7){g.beginPath();g.moveTo(0,y+rnd()*2);g.lineTo(w,y+rnd()*2);g.stroke()}},[6,6]);
  var texCrop=canvasTex(256,256,function(g,w,h){speckle(g,w,h,'#c9ae6a',3000,['#e2c98a','#a88c4b','#d9bf7c'],2);g.strokeStyle='rgba(120,95,45,.28)';g.lineWidth=1.5;for(var x=0;x<w;x+=5){g.beginPath();g.moveTo(x,0);g.lineTo(x,h);g.stroke()}},[5,5]);
  var texGreen=canvasTex(256,256,function(g,w,h){speckle(g,w,h,'#7d8d43',3000,['#647534','#93a352','#6d7d3b'],2);g.strokeStyle='rgba(60,75,30,.3)';for(var x=0;x<w;x+=6){g.beginPath();g.moveTo(x,0);g.lineTo(x,h);g.stroke()}},[5,5]);
  var texOrch=canvasTex(256,256,function(g,w,h){speckle(g,w,h,'#a98f66',2400,['#8a7350','#bfa77c','#7d6a49'],3);g.strokeStyle='rgba(40,35,25,.35)';g.lineWidth=1.2;for(var y=0;y<h;y+=32){g.beginPath();g.moveTo(0,y);g.lineTo(w,y);g.stroke()}},[4,4]);
  var texRoad=canvasTex(128,128,function(g,w,h){speckle(g,w,h,'#cdbb93',900,['#b8a47b','#ddd0ac'],2)},[40,40]);

  /* ---------- farm layout ---------- */
  var colW=[92,112,100,84],rowD=[78,92,72],ROAD=9;
  var W=colW.reduce(function(a,b){return a+b})+ROAD*(colW.length-1),D=rowD.reduce(function(a,b){return a+b})+ROAD*(rowD.length-1);
  var X0=-W/2,Z0=-D/2;
  var road=new T.Mesh(new T.PlaneGeometry(W+40,D+40),new T.MeshLambertMaterial({map:texRoad}));road.rotation.x=-Math.PI/2;road.position.y=.05;road.receiveShadow=true;scene.add(road);
  var types=[['orch','soil','orch','crop'],['crop','orch','avo','orch'],['young','orch','green','soil']];
  var names={'1,1':'B4','1,2':'C1','0,2':'D2'};
  var parcels=[];
  var treeM=new T.Object3D(),treeData=[];
  var z=Z0;
  for(var r=0;r<rowD.length;r++){var x=X0;
    for(var c=0;c<colW.length;c++){var w=colW[c],d=rowD[r],t=types[r][c],cx=x+w/2,cz=z+d/2;
      var mat=new T.MeshLambertMaterial({map:t==='soil'?texSoil:t==='crop'?texCrop:t==='green'?texGreen:texOrch});
      var m=new T.Mesh(new T.PlaneGeometry(w,d),mat);m.rotation.x=-Math.PI/2;m.position.set(cx,.12,cz);m.receiveShadow=true;scene.add(m);
      var p={x:x,z:z,w:w,d:d,cx:cx,cz:cz,type:t,name:names[r+','+c]||null,h:(t==='orch'||t==='avo'||t==='young')?(t==='young'?2.2:t==='avo'?6.4:4.6):.6};parcels.push(p);
      if(t==='orch'||t==='avo'||t==='young'){var sx=t==='avo'?8:t==='young'?6:(small?7:5.6),sz=t==='avo'?7:(small?6.5:5);
        for(var tz=z+sz/2+1;tz<z+d-1;tz+=sz)for(var tx=x+sx/2+1;tx<x+w-1;tx+=sx){
          if(t==='young'&&rnd()<.15)continue;
          var s=(t==='avo'?2.6:t==='young'?1.05:1.75)*(.85+rnd()*.3);treeData.push([tx+(rnd()-.5)*.6,tz+(rnd()-.5)*.6,s,t])}}
      x+=w+ROAD}
    z+=rowD[r]+ROAD}
  /* windbreak lines (cypress) along the north and west edges */
  for(var wx=X0-14;wx<X0+W+14;wx+=small?7:4.5)treeData.push([wx,Z0-12+(rnd()-.5),2.3+rnd()*.5,'wind']);
  for(var wz=Z0-8;wz<Z0+D;wz+=small?7:4.5)treeData.push([X0-14+(rnd()-.5),wz,2.3+rnd()*.5,'wind']);
  /* scattered trees outside */
  for(var q=0;q<(small?60:160);q++){var a=rnd()*Math.PI*2,rr=W*.62+rnd()*260;treeData.push([Math.cos(a)*rr,Math.sin(a)*rr*.75,1.8+rnd()*1.6,'wild'])}

  var canopyG=new T.IcosahedronGeometry(1,1);canopyG.translate(0,1.25,0);
  var trees=new T.InstancedMesh(canopyG,new T.MeshLambertMaterial({color:'#ffffff'}),treeData.length);
  trees.castShadow=!small;trees.receiveShadow=true;
  var cTree={orch:['#3f5a26','#4c6a2c','#36501f'],avo:['#2f4a22','#3a5626'],young:['#5a7a33','#6a8a3c'],wind:['#2c4120','#33492a'],wild:['#4a5f2c','#56683a']};
  treeData.forEach(function(td,i){var s=td[2],tall=td[3]==='wind';treeM.position.set(td[0],0,td[1]);treeM.scale.set(s,tall?s*3.2:s*.95,s);treeM.rotation.y=rnd()*6.28;treeM.updateMatrix();trees.setMatrixAt(i,treeM.matrix);
    var pal=cTree[td[3]];tmp.set(pal[(rnd()*pal.length)|0]);tmp.offsetHSL(0,0,(rnd()-.5)*.06);trees.setColorAt(i,tmp)});
  scene.add(trees);

  /* buildings, basin, a tractor */
  function box(w,h,d,col,x,y,zz){var b=new T.Mesh(new T.BoxGeometry(w,h,d),new T.MeshLambertMaterial({color:col}));b.position.set(x,y+h/2,zz);b.castShadow=!small;b.receiveShadow=true;scene.add(b);return b}
  function roof(w,d,h,col,x,y,zz){var g=new T.CylinderGeometry(0,1,1,4,1);g.rotateY(Math.PI/4);var m=new T.Mesh(g,new T.MeshLambertMaterial({color:col}));m.scale.set(w*.72,h,d*.72);m.position.set(x,y+h/2,zz);m.castShadow=!small;scene.add(m)}
  var bx=X0+W+38,bz=Z0+40;
  box(46,9,26,'#e8e3d6',bx,0,bz);roof(46,26,6,'#7d98b8',bx,9,bz);
  box(20,6,14,'#efe7d6',bx+6,0,bz+38);roof(20,14,4,'#b5574a',bx+6,6,bz+38);
  box(14,5,10,'#efe7d6',bx-18,0,bz+40);roof(14,10,3.5,'#b5574a',bx-18,5,bz+40);
  for(var si=0;si<3;si++){var sil=new T.Mesh(new T.CylinderGeometry(4,4,18,20),new T.MeshLambertMaterial({color:'#c9ced6'}));sil.position.set(bx+30+si*9.5,9,bz-6);sil.castShadow=!small;scene.add(sil)}
  var basin=new T.Mesh(new T.PlaneGeometry(54,34),new T.MeshPhongMaterial({color:'#4d7f9e',shininess:90,specular:'#fff2d0'}));basin.rotation.x=-Math.PI/2;basin.position.set(bx+4,.3,bz+88);scene.add(basin);
  var rim=new T.Mesh(new T.BoxGeometry(58,1.2,38),new T.MeshLambertMaterial({color:'#d8cdb4'}));rim.position.set(bx+4,.2,bz+88);scene.add(rim);basin.position.y=.85;
  var tractor=new T.Group();var tb=new T.Mesh(new T.BoxGeometry(4.6,2.2,2.6),new T.MeshLambertMaterial({color:'#2f7a4a'}));tb.position.y=1.6;tractor.add(tb);
  var tc=new T.Mesh(new T.BoxGeometry(2,2,2.4),new T.MeshLambertMaterial({color:'#e9efe6'}));tc.position.set(-.8,3.4,0);tractor.add(tc);tractor.children.forEach(function(o){o.castShadow=!small});scene.add(tractor);
  var trackZ=Z0+rowD[0]+ROAD/2;

  /* ---------- scan overlays (one sheet per parcel) ---------- */
  function ndviTex(p){var low=p.name==='C1'?.0:p.name==='D2'?.25:.55;return canvasTex(128,128,function(g,w,h){var img=g.createImageData(w,h);
    for(var yy=0;yy<h;yy++)for(var xx=0;xx<w;xx++){var v=fbm(xx/22+p.cx*.05,yy/22+p.cz*.05);var val=Math.min(1,Math.max(0,low+v*.75-(p.type==='soil'?.45:0)));
      var cR,cG,cB;if(val<.5){var k=val/.5;cR=210-40*k;cG=70+130*k;cB=60}else{var k2=(val-.5)/.5;cR=170-120*k2;cG=200+20*k2;cB=60+40*k2}
      var o=(yy*w+xx)*4;img.data[o]=cR;img.data[o+1]=cG;img.data[o+2]=cB;img.data[o+3]=255}g.putImageData(img,0,0)})}
  var U={uScan:{value:-9999},uAlpha:{value:0},uTime:{value:0}};
  var vs='varying vec2 vUv;varying vec3 vW;void main(){vUv=uv;vec4 w=modelMatrix*vec4(position,1.0);vW=w.xyz;gl_Position=projectionMatrix*viewMatrix*w;}';
  var fs='uniform sampler2D uMap;uniform float uScan,uAlpha,uMix,uPulse,uTime;uniform vec3 uStatus;varying vec2 vUv;varying vec3 vW;'+
    'void main(){float d=uScan-vW.x;float rev=smoothstep(0.0,10.0,d);float edge=exp(-abs(d)/2.8)*step(-40.0,d)*step(d,40.0);'+
    'vec3 n=texture2D(uMap,vUv).rgb;vec3 c=mix(n,uStatus,uMix);vec2 gd=abs(fract(vW.xz/7.0)-0.5);float grid=smoothstep(0.455,0.5,max(gd.x,gd.y));'+
    'vec2 e=min(vUv,1.0-vUv);float border=1.0-smoothstep(0.0,0.012,min(e.x,e.y));float pulse=uPulse*(0.55+0.45*sin(uTime*3.2));'+
    'vec3 col=mix(c,vec3(0.85,1.0,0.96),grid*0.35+border*0.6);col=mix(col,vec3(0.8,1.0,0.95),edge);'+
    'float a=rev*uAlpha*(0.42+grid*0.18+border*0.4+pulse*0.25)+edge*0.85;gl_FragColor=vec4(col,a);}';
  parcels.forEach(function(p){
    var st=p.name==='C1'?'#e0473b':p.name==='D2'?'#f0b43c':p.name==='B4'?'#58c27a':'#5fae8c';
    var u={uMap:{value:ndviTex(p)},uScan:U.uScan,uAlpha:U.uAlpha,uTime:U.uTime,uMix:{value:0},uPulse:{value:0},uStatus:{value:new T.Color(st)}};
    var mat=new T.ShaderMaterial({uniforms:u,vertexShader:vs,fragmentShader:fs,transparent:true,depthWrite:false,blending:T.NormalBlending});
    var sh=new T.Mesh(new T.PlaneGeometry(p.w-1.5,p.d-1.5),mat);sh.rotation.x=-Math.PI/2;sh.position.set(p.cx,p.h+.4,p.cz);sh.renderOrder=2;scene.add(sh);p.u=u;p.sheet=sh});

  /* scanning curtain: vertical light sheet sweeping west → east */
  var curtainMat=new T.ShaderMaterial({uniforms:{uA:{value:0}},transparent:true,depthWrite:false,blending:T.AdditiveBlending,side:T.DoubleSide,
    vertexShader:'varying vec2 vUv;void main(){vUv=uv;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.0);}',
    fragmentShader:'uniform float uA;varying vec2 vUv;void main(){float f=pow(1.0-vUv.y,2.2);float s=1.0-abs(vUv.x-0.5)*2.0;gl_FragColor=vec4(vec3(0.62,1.0,0.88)*f,f*uA*smoothstep(0.0,0.15,s));}'});
  var curtain=new T.Mesh(new T.PlaneGeometry(D+60,140),curtainMat);curtain.rotation.y=Math.PI/2;curtain.position.y=70;curtain.renderOrder=3;scene.add(curtain);
  var sat=new T.Group();var satB=new T.Mesh(new T.BoxGeometry(3,2,2),new T.MeshBasicMaterial({color:'#f2f4f8'}));sat.add(satB);
  var pnl=new T.Mesh(new T.BoxGeometry(.3,.2,12),new T.MeshBasicMaterial({color:'#3d5fa8'}));sat.add(pnl);sat.position.y=210;sat.visible=false;scene.add(sat);

  /* data layers for « Croiser » */
  var layerNames=['Satellite','Climat','Laboratoire'],layers=[];
  layerNames.forEach(function(nm,i){var mat=new T.ShaderMaterial({uniforms:{uA:{value:0},uC:{value:new T.Color(['#7fd6ff','#ffd27a','#9cf0b4'][i])}},transparent:true,depthWrite:false,side:T.DoubleSide,
    vertexShader:'varying vec2 vUv;void main(){vUv=uv;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.0);}',
    fragmentShader:'uniform float uA;uniform vec3 uC;varying vec2 vUv;void main(){vec2 g=abs(fract(vUv*vec2(18.0,13.0))-0.5);float l=smoothstep(0.44,0.5,max(g.x,g.y));vec2 e=min(vUv,1.0-vUv);float b=1.0-smoothstep(0.0,0.01,min(e.x,e.y));gl_FragColor=vec4(uC,uA*(0.1+l*0.28+b*0.95));}'});
    var L=new T.Mesh(new T.PlaneGeometry(W+10,D+10),mat);L.rotation.x=-Math.PI/2;L.position.y=60+i*34;L.renderOrder=4;scene.add(L);layers.push(L)});

  /* ---------- chapters ---------- */
  var CAM={
    idle:{p:[-330,190,330],t:[10,0,0]},
    obs:{p:[-250,230,250],t:[20,0,-5]},
    cro:{p:[-390,250,380],t:[30,40,0]},
    dec:{p:[-150,115,215],t:[60,0,10]}};
  var cur={p:new T.Vector3().fromArray(CAM.idle.p),t:new T.Vector3().fromArray(CAM.idle.t)},goal={p:cur.p.clone(),t:cur.t.clone()};
  var state={ch:0,t0:0};
  var B4=parcels.find(function(p){return p.name==='B4'}),C1=parcels.find(function(p){return p.name==='C1'}),D2=parcels.find(function(p){return p.name==='D2'});
  var labels=[
    {p:B4,el:mk('B4 · Agrumes','Baisse physiologique · aucune action','ok')},
    {p:C1,el:mk('C1 · Avocat','Potassium −25 % · à corriger','crit')},
    {p:D2,el:mk('D2 · Agrumes','Cochenille · à surveiller 48 h','warn')}];
  var layerLabels=layerNames.map(function(nm,i){var e=document.createElement('div');e.className='s3-layer';e.innerHTML='<span>0'+(i+1)+'</span>'+nm;labelsBox.appendChild(e);return e});
  function mk(a,b,k){var e=document.createElement('div');e.className='s3-tag '+k;e.innerHTML='<b>'+a+'</b><span>'+b+'</span>';labelsBox.appendChild(e);return e}

  function go(ch){state.ch=ch;state.t0=clock;var c=['idle','obs','cro','dec'][ch];goal.p.fromArray(CAM[c].p);goal.t.fromArray(CAM[c].t);root.dataset.ch=ch;
    if(reduce){U.uScan.value=9999;}}
  setupUI(go);

  /* ---------- loop ---------- */
  var clock=0,last=performance.now(),running=true,visible=true;
  var io=new IntersectionObserver(function(es){visible=es[0].isIntersecting},{threshold:0});io.observe(root);
  function resize(){var w=stage.clientWidth,h=stage.clientHeight;renderer.setSize(w,h,false);camera.aspect=w/h;var port=w<h*.9;camera.fov=port?50:34;/* frame the farm away from the copy: lift it on portrait screens, nudge it right on wide ones */if(port)camera.setViewOffset(w,h,0,Math.round(h*.2),w,h);else if(w>900)camera.setViewOffset(w,h,-Math.round(w*.08),Math.round(h*.04),w,h);else camera.clearViewOffset();camera.updateProjectionMatrix()}
  addEventListener('resize',resize);resize();
  var v3=new T.Vector3();
  function ease(k){return k<.5?4*k*k*k:1-Math.pow(-2*k+2,3)/2}
  var perf={n:0,sum:0,level:0};
  function adapt(ms){if(perf.level>1)return;perf.n++;perf.sum+=ms;if(perf.n<40)return;var avg=perf.sum/perf.n;perf.n=0;perf.sum=0;
    if(avg>34){perf.level++;if(perf.level===1){renderer.shadowMap.enabled=false;trees.castShadow=false;scene.traverse(function(o){if(o.material)o.material.needsUpdate=true});renderer.setPixelRatio(1)}
      else{renderer.setPixelRatio(.75)}resize()}}
  function frame(now){requestAnimationFrame(frame);var raw=now-last;var dt=Math.min(window.S3_LITE?.5:.05,raw/1000);last=now;if(!visible)return;adapt(raw);clock+=dt;U.uTime.value=clock;
    var ch=state.ch,el=clock-state.t0;
    /* camera: glide toward the chapter shot with a slow breathing orbit */
    var k=reduce?1:1-Math.pow(.0009,dt);cur.p.lerp(goal.p,k*.9);cur.t.lerp(goal.t,k*.9);
    var orb=reduce?0:Math.sin(clock*.07)*.06;var cx=cur.p.x*Math.cos(orb)-cur.p.z*Math.sin(orb),cz=cur.p.x*Math.sin(orb)+cur.p.z*Math.cos(orb);
    camera.position.set(cx,cur.p.y+Math.sin(clock*.19)*2,cz);camera.lookAt(cur.t);
    /* chapter 1: satellite sweep */
    var xmin=X0-40,xmax=X0+W+40;
    if(ch>=1){var sk=reduce?1:Math.min(1,Math.max(0,el-.35)/5.2);if(ch>1)sk=1;U.uScan.value=xmin+(xmax-xmin+80)*(.5-.5*Math.cos(Math.PI*sk));
      U.uAlpha.value+=((ch===2?.45:1)-U.uAlpha.value)*Math.min(1,dt*3);
      var on=ch===1&&sk<1;curtainMat.uniforms.uA.value+=((on?1:0)-curtainMat.uniforms.uA.value)*Math.min(1,dt*4);curtain.position.x=U.uScan.value;
      sat.visible=ch===1;sat.position.x=U.uScan.value;sat.position.z=-40;sat.rotation.x+=dt*.2;
    }else{U.uAlpha.value+=(0-U.uAlpha.value)*Math.min(1,dt*3);curtainMat.uniforms.uA.value*=.9;sat.visible=false}
    /* chapter 2: three data layers descend and merge */
    layers.forEach(function(L,i){var tgtA=ch===2?.95:0,tgtY=ch===2?(Math.max(6,60+i*34-ease(Math.min(1,Math.max(0,(el-.6-i*.35)/2.4)))*(54+i*34))):60+i*34;
      if(ch!==2)tgtY=60+i*34;L.material.uniforms.uA.value+=(tgtA-L.material.uniforms.uA.value)*Math.min(1,dt*3);L.position.y+=(tgtY-L.position.y)*Math.min(1,dt*(reduce?60:4))});
    /* chapter 3: decision colours, C1 pulses */
    parcels.forEach(function(p){var named=!!p.name;var mixT=ch===3?(named?1:.0):0;var aT=ch===3&&!named?.35:1;p.u.uMix.value+=(mixT-p.u.uMix.value)*Math.min(1,dt*3);
      p.u.uPulse.value+=((ch===3&&p.name==='C1'?1:0)-p.u.uPulse.value)*Math.min(1,dt*3);p.sheet.material.opacity=aT});
    /* tractor along the track */
    var tx=X0+((clock*6)%(W+20))-10;tractor.position.set(tx,0,trackZ);
    renderer.render(scene,camera);
    /* labels */
    var w=stage.clientWidth,h=stage.clientHeight;
    labels.forEach(function(L,i){v3.set(L.p.cx,L.p.h+6,L.p.cz).project(camera);var show=ch===3&&v3.z<1;var tx=Math.min(w-(L.el.offsetWidth||160)+4,Math.max(14,(v3.x*.5+.5)*w));L.el.style.transform='translate('+tx+'px,'+((-v3.y*.5+.5)*h)+'px)';L.el.classList.toggle('on',show&&el>.8+i*.25)});
    var prevY=1e9;layerLabels.forEach(function(e,i){var L=layers[i];v3.set(X0+W+4,L.position.y,Z0).project(camera);var lx=Math.min(w-(e.offsetWidth||140)-16,Math.max(16,(v3.x*.5+.5)*w+14));var ly=Math.min((-v3.y*.5+.5)*h,prevY-36);prevY=ly;e.style.transform='translate('+lx+'px,'+ly+'px)';e.classList.toggle('on',ch===2&&L.material.uniforms.uA.value>.4)});
  }
  requestAnimationFrame(frame);

  /* ---------- UI ---------- */
  function setupUI(go){
    var btn=root.querySelector('.s3-go'),steps=root.querySelectorAll('.s3-step'),dots=root.querySelectorAll('.s3-dots button'),ch=0,timer=null;
    function show(n){ch=n;steps.forEach(function(s,i){s.classList.toggle('on',i===n)});dots.forEach(function(d,i){d.classList.toggle('on',i===n);d.setAttribute('aria-current',i===n?'step':'false')});
      btn.querySelector('.s3-go-t').textContent=['Lancer le scan','Croiser les données','Voir la décision','Découvrir notre mission'][n];if(go)go(n);root.dataset.ch=n;
      clearTimeout(timer);if(n>0&&n<3&&!reduce&&!window.S3_HOLD)timer=setTimeout(function(){show(n+1)},n===1?7600:6500)}
    btn.addEventListener('click',function(){if(ch<3)show(ch+1);else{var nx=document.getElementById('notre-conviction');if(nx)nx.scrollIntoView({behavior:reduce?'auto':'smooth'})}});
    dots.forEach(function(d,i){d.addEventListener('click',function(){show(i)})});
    show(0);
  }
})();
