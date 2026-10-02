from parts import phero, cta, dots
from screens import CLIMAT, SATELLITE, LABO, PILOTAGE, screen

ICON = {
 "sat": '<rect x="19" y="17" width="10" height="10" rx="1.5" transform="rotate(-45 24 22)"/><g transform="rotate(-45 24 22)"><rect x="2" y="18" width="13" height="8" rx="1"/><rect x="33" y="18" width="13" height="8" rx="1"/><path d="M15 22h4M29 22h4M24 27v4M19.5 33.5a4.5 4.5 0 0 0 9 0z"/></g><path d="M7 37a8 8 0 0 0 5 5M3 36a13 13 0 0 0 9 9"/>',
 "cli": '<path d="M10 9a4 4 0 0 1 8 0v18.5a7.5 7.5 0 1 1-8 0z"/><path d="M14 16v15"/><path d="M27 27h13a5 5 0 0 0 0-10 7.5 7.5 0 0 0-14 2.5 4 4 0 0 0 1 7.5z"/><path d="M29 33l-2 4M35 33l-2 4M41 33l-2 4"/>',
 "lab": '<path d="M18 5h12M20.5 5v13L9.5 37.5A3.2 3.2 0 0 0 12.3 42h23.4a3.2 3.2 0 0 0 2.8-4.5L27.5 18V5"/><path d="M14 29h20"/><path d="M19 38c0-5 3.5-7.5 8-7.5 0 4.5-3.5 7.5-8 7.5zM19 38l4.5-4"/>',
 "coop": '<circle cx="24" cy="14" r="5"/><circle cx="10" cy="19" r="4"/><circle cx="38" cy="19" r="4"/><path d="M14 40c0-6 4.5-10 10-10s10 4 10 10M3 37c0-5 3-8 7-8M45 37c0-5-3-8-7-8"/>',
 "truck": '<rect x="3" y="14" width="25" height="18" rx="2"/><path d="M28 20h8l6 7v5H28"/><circle cx="12" cy="36" r="4"/><circle cx="35" cy="36" r="4"/>',
 "flow": '<circle cx="10" cy="12" r="5"/><circle cx="10" cy="36" r="5"/><circle cx="38" cy="24" r="6"/><path d="M15 13c9 1 13 5 17 9M15 35c9-1 13-5 17-9"/>',
 "ask": '<path d="M8 10a4 4 0 0 1 4-4h24a4 4 0 0 1 4 4v18a4 4 0 0 1-4 4H20l-8 8v-8h0a4 4 0 0 1-4-4z"/><path d="M20 15a4 4 0 1 1 5.5 3.7c-1 .5-1.5 1.3-1.5 2.3M24 25.5v.5"/>',
 "doc": '<path d="M12 4h18l8 8v32H12z"/><path d="M30 4v8h8M18 22h14M18 29h14M18 36h8"/>',
}
def ico(k, size=56):
    return f'<span class="ico"><svg viewBox="0 0 48 48" width="{size}" height="{size}" fill="none" stroke="#274B9C" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICON[k]}</svg></span>'

def tags(items):
    return '<ul class="tags">' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'

def bullets(items):
    return '<ul class="ticks">' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'

# ---------------------------------------------------------------- LA MÉTHODE
METHODE = phero("vue-aerienne", "La méthode",
  "Un indice qui baisse ne veut rien dire tout seul",
  "Même exploitation, même semaine, même mesure satellite. Selon ce que vous croisez avec, vous envoyez votre technicien au mauvais endroit, ou vous corrigez le problème qui compte vraiment.") + f'''
<main>
<section class="split">
  <div class="txt">
    <p class="eyebrow sl">Notre approche</p>
    <h2 class="h2 sl" style="transition-delay:.1s">Nous ne lisons pas une source de données. Nous les croisons toutes.</h2>
    <p class="sl" style="transition-delay:.2s">La plupart des outils de suivi satellite surveillent un indice et déclenchent une alerte dès qu'il sort de sa moyenne. Sans connaître le stade de la culture ni les conditions de la période, ils ne peuvent pas faire la différence entre un stress réel et une évolution normale de la plante.</p>
    <p class="sl" style="transition-delay:.2s">Firmaty réunit sur chaque secteur trois flux qui ne se parlent jamais d'habitude : l'imagerie satellite, les conditions climatiques rapportées au stade phénologique, et vos analyses de laboratoire. Notre moteur d'analyse recoupe les trois, écarte les fausses alertes, et vous dit quoi corriger et où.</p>
    <a class="btn btn-blue sl" style="transition-delay:.2s;margin-top:30px" href="services.html">Voir nos services</a>
  </div>
  <div class="media fi"><img src="img/prelevement-sol.jpg" alt="Agronome prélevant un échantillon de sol dans un verger d'agrumes" loading="lazy"></div>
</section>

<section class="wrap20 sec-gap">
  <div class="box">
    <p class="eyebrow a2">Pourquoi le croisement change tout</p>
    <h2 class="h2 a2" style="transition-delay:.1s">Le même secteur, deux lectures</h2>
    <p class="lede a2" style="transition-delay:.15s">Exemple tiré de notre exploitation de démonstration : agrumes et avocat en plein champ, 340 hectares, 12 secteurs.</p>
    <div class="smap a2" data-mode="sat">
      <div class="smap-toggle" role="tablist" aria-label="Lecture du secteur">
        <button type="button" role="tab" class="on" aria-selected="true" data-mode="sat">Plateforme satellite seule</button>
        <button type="button" role="tab" aria-selected="false" data-mode="fir">Firmaty · satellite + climat + laboratoire</button>
        <span class="smap-ink" aria-hidden="true"></span>
      </div>
      <div class="smap-body">
        <div class="smap-photo">
          <img src="img/vue-aerienne.jpg" alt="Vue aérienne de trois blocs de vergers, celui du centre moins vigoureux" width="1100" height="733" loading="lazy">
          <div class="zone z-b4"><span class="zl">B4 · Agrumes</span><span class="zs s-sat">Alerte · vigueur −11 %</span><span class="zs s-fir">Physiologique · aucune action</span></div>
          <div class="zone z-c1"><span class="zl">C1 · Avocat</span><span class="zs s-sat">Aucun signal</span><span class="zs s-fir">À corriger · K −25 %</span></div>
          <div class="zone z-d2"><span class="zl">D2 · Agrumes</span><span class="zs s-sat">Aucun signal</span><span class="zs s-fir">À surveiller · 48 h</span></div>
          <p class="smap-cap">Exploitation de démonstration · 340 ha · 12 secteurs</p>
        </div>
        <div class="smap-panels">
          <div class="smap-panel p-sat">
            <p class="stat">−11 % <small>/ 15 jours</small></p>
            <h3>Vigueur du secteur B4 : alerte envoyée</h3>
            <p>L'indice sort de sa moyenne, le système déclenche. Sans le stade de la culture ni les conditions de la période, il ne peut faire que ça. L'équipe se déplace sur B4 et ne trouve rien.</p>
            <p class="note">Pendant ce temps, la vraie carence sur C1 n'est pas détectée. Elle n'est visible que dans les analyses de laboratoire.</p>
            <ul class="smap-list"><li><span>B4</span>Déplacement inutile<b class="chip crit">Fausse alerte</b></li><li><span>C1</span>Carence non vue<b class="chip n">Aucun signal</b></li><li><span>D2</span>Risque non anticipé<b class="chip n">Aucun signal</b></li></ul>
          </div>
          <div class="smap-panel p-fir">
            <p class="stat">3 sources</p>
            <h3>Fausse alerte écartée, vrai problème trouvé</h3>
            <p>Sur B4, les deux indices baissent ensemble en phase de développement des fruits et les conditions climatiques sont conformes : c'est physiologique, personne ne se déplace. Sur C1, l'analyse foliaire montre un potassium en retrait de 25 % sur la cible du stade.</p>
            <p class="note"><b>Recommandation générée :</b> corriger le potassium sur C1 par fertigation avant la fin du stade. Le calibre du fruit est le premier poste affecté.</p>
            <ul class="smap-list"><li><span>B4</span>Baisse physiologique<b class="chip ok">Aucune action</b></li><li><span>C1</span>Potassium −25 %<b class="chip crit">À corriger</b></li><li><span>D2</span>Pression cochenille<b class="chip warn">À surveiller</b></li></ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="sec-head">
    <p class="eyebrow a2">Ce que contient chaque source</p>
    <h2 class="h2 a2" style="transition-delay:.1s">Trois flux de données, mis à jour en continu</h2>
  </div>
  <div class="grid3">
    <article class="card line a2">{ico("sat")}<div class="txt"><span class="k">SOURCE 01 · SATELLITE</span><h3>Imagerie multispectrale</h3><p>Suivi par secteur, historique sur douze semaines glissantes, couverture nuageuse filtrée. Imagerie du programme européen Copernicus en résolution 10 mètres.</p>{bullets(["Vigueur végétative","Teneur en eau","Statut azoté","Cartographie par secteur"])}</div></article>
    <article class="card line a2" style="transition-delay:.1s">{ico("cli")}<div class="txt"><span class="k">SOURCE 02 · CLIMAT</span><h3>Conditions et prévisions</h3><p>Historique, temps réel et prévisions, rapportés au stade phénologique de chaque culture. Aucune station à installer.</p>{bullets(["Température et humidité","Évapotranspiration","Déficit de pression de vapeur","Pression maladies et ravageurs"])}</div></article>
    <article class="card line a2" style="transition-delay:.2s">{ico("lab")}<div class="txt"><span class="k">SOURCE 03 · LABORATOIRE</span><h3>Mesures physico-chimiques</h3><p>Vos rapports existants, confrontés aux cibles de la culture, du stade et du secteur. Les sondes peuvent être intégrées si vous en avez.</p>{bullets(["Sol et composition","Analyses foliaires","Eau d'irrigation et sondes","Équilibre cationique"])}</div></article>
  </div>
</section>

<section class="sec">
  <div class="sec-head">
    <p class="eyebrow a2">Le moteur d'analyse</p>
    <h2 class="h2 a2" style="transition-delay:.1s">Comment un écart devient une décision</h2>
    <p class="lede a2" style="transition-delay:.15s">Chaque variation suit le même chemin avant d'arriver dans votre synthèse du jour.</p>
  </div>
  <ol class="engine" data-play>
    <li class="eng-step"><span class="eng-n">1</span><h3>Détecter</h3><p>Un indice satellite sort de sa tendance sur un secteur : vigueur, teneur en eau ou statut azoté.</p><span class="eng-tag">Satellite</span></li>
    <li class="eng-step"><span class="eng-n">2</span><h3>Replacer dans le contexte</h3><p>L'écart est comparé au stade phénologique de la culture et aux conditions climatiques de la période.</p><span class="eng-tag">Climat · stade</span></li>
    <li class="eng-step"><span class="eng-n">3</span><h3>Confronter aux mesures</h3><p>Les analyses de sol, foliaires et d'eau sont confrontées aux cibles du stade pour confirmer ou écarter une cause.</p><span class="eng-tag">Laboratoire</span></li>
    <li class="eng-step"><span class="eng-n">4</span><h3>Qualifier et recommander</h3><p>Chaque secteur reçoit un statut et, si besoin, la correction à apporter.</p><span class="eng-out"><b class="chip ok">Aucune action</b><b class="chip warn">À surveiller</b><b class="chip crit">À corriger</b></span></li>
  </ol>
</section>

<section class="cta-wrap">
  <div class="band big a3">
    <div class="band-txt">
      <p class="eyebrow sl">L'avance</p>
      <p class="bignum sl" style="transition-delay:.1s"><small class="pre-n">jusqu'à</small>15 <small>jours</small></p>
    </div>
    <div class="band-side sl" style="transition-delay:.2s">
      <h3>C'est l'avance que vous prenez sur un stress hydrique.</h3>
      <p>L'indice de teneur en eau détecte un déficit avant que la plante ne l'exprime visuellement. Quand vos équipes le voient au champ, il est déjà installé. Sur une culture d'export, cette semaine et demie se lit directement dans le calibre du fruit et dans le tonnage que vous pourrez engager.</p>
    </div>
    <figure class="lead-chart" data-play>
      <svg viewBox="0 0 1000 250" role="img" aria-label="Illustration : l'indice de teneur en eau franchit le seuil de stress environ quinze jours avant que le symptôme soit visible au champ">
        <rect class="lc-win" x="181" y="24" width="705" height="176"/>
        <line class="lc-grid" x1="40" y1="200" x2="980" y2="200"/>
        <line class="lc-thr" x1="40" y1="112" x2="980" y2="112"/>
        <text class="lc-t" x="976" y="104" text-anchor="end">Seuil de stress</text>
        <path class="lc-curve" d="M40 58 C 100 60, 150 84, 181 112 S 400 166, 640 178 S 880 188, 980 191"/>
        <circle class="lc-dot d1" cx="181" cy="112" r="7"/>
        <line class="lc-mark" x1="886" y1="24" x2="886" y2="200"/>
        <circle class="lc-dot d2" cx="886" cy="187" r="7"/>
        <text class="lc-t b" x="181" y="12" text-anchor="middle">Détection Firmaty</text>
        <text class="lc-t b" x="980" y="12" text-anchor="end">Symptôme visible au champ</text>
        <text class="lc-big" x="533" y="92" text-anchor="middle">Jusqu'à 15 jours d'avance</text>
        <g class="lc-ax"><text x="40" y="228">J0</text><text x="181" y="228" text-anchor="middle">J+3</text><text x="886" y="228" text-anchor="middle">J+18</text><text x="980" y="228" text-anchor="end">J+20</text></g>
        <text class="lc-t" x="40" y="40">Indice de teneur en eau</text>
      </svg>
      <figcaption>Illustration du principe, pas une mesure d'exploitation.</figcaption>
    </figure>
  </div>
</section>

<section class="sec" id="lexique">
  <div class="sec-head">
    <p class="eyebrow a2">Lexique</p>
    <h2 class="h2 a2" style="transition-delay:.1s">Les mots de la plateforme</h2>
    <p class="lede a2" style="transition-delay:.15s">Les indicateurs que vous retrouverez dans vos écrans et vos synthèses, expliqués simplement.</p>
  </div>
  <dl class="gloss">
    <div class="a2"><dt>Vigueur végétative</dt><dd>Indice calculé à partir de la réflectance de la végétation dans le rouge et le proche infrarouge. Il traduit la densité et l'activité du couvert : plus il est élevé, plus la canopée est dense et active.</dd></div>
    <div class="a2"><dt>Teneur en eau du couvert</dt><dd>Indice qui combine le proche infrarouge et l'infrarouge à ondes courtes, sensible à l'eau contenue dans les feuilles. Il réagit à un déficit hydrique avant que la plante ne flétrisse.</dd></div>
    <div class="a2"><dt>Évapotranspiration de référence (ET0)</dt><dd>Quantité d'eau, en millimètres, qu'évaporerait un couvert de référence dans les conditions du jour. Rapportée à la culture et à son stade, elle sert de base au calcul des besoins d'irrigation.</dd></div>
    <div class="a2"><dt>Déficit de pression de vapeur (VPD)</dt><dd>Écart, en kilopascals, entre l'humidité que l'air pourrait contenir et celle qu'il contient. Un VPD élevé pousse la plante à transpirer davantage ; trop bas, il favorise certaines maladies.</dd></div>
    <div class="a2"><dt>Stade phénologique</dt><dd>Étape du cycle de la culture : repos, floraison, nouaison, grossissement du fruit, maturation. Les mêmes valeurs n'ont pas la même signification selon le stade.</dd></div>
    <div class="a2"><dt>Antagonisme nutritionnel</dt><dd>Blocage où un élément présent en quantité suffisante devient inaccessible à la plante à cause d'un autre, par exemple un excès de calcium ou de magnésium qui freine l'absorption du potassium.</dd></div>
    <div class="a2"><dt>Équilibre cationique</dt><dd>Rapport entre les principaux cations du sol, potassium, calcium, magnésium et sodium. Un déséquilibre peut provoquer des carences même quand chaque élément paraît correct isolément.</dd></div>
    <div class="a2"><dt>Fertigation</dt><dd>Apport d'engrais dissous dans l'eau d'irrigation, généralement par le goutte-à-goutte. Elle permet de corriger une carence rapidement et au plus près des racines.</dd></div>
  </dl>
</section>
</main>
''' + cta()

# ---------------------------------------------------------------- LA PLATEFORME

SERVICES = [
  ("Météo", "Climat et pression sanitaire",
   "Conditions en temps réel, prévisions et recommandation d'irrigation calculée à partir de l'évapotranspiration et du déficit de pression de vapeur. La pression maladies et ravageurs est calculée en continu pour la culture et son stade en cours.",
   "Sur le secteur B4, l'évapotranspiration cumulée atteint 32,1 mm sur cinq jours sans pluie annoncée. La plateforme conseille un apport modéré sur les créneaux de nuit et signale une pression cochenille en hausse.",
   ["Historique","Prévisions 24h et 5j","Irrigation pilotée","Risques par stade"], "CLIMAT"),
  ("Satellite", "Analyse satellite",
   "Chaque secteur est suivi image après image, avec des seuils agronomiques qui distinguent l'optimal, l'acceptable et le critique. La tendance sur douze semaines révèle ce qu'une image isolée ne montrera jamais.",
   "La vigueur de B4 recule de 12 % en douze semaines mais reste en zone optimale. La baisse conjointe des deux indices correspond à la réallocation des ressources vers le fruit. C1, lui, remonte en tête des priorités.",
   ["Tendances","Stress hydrique","Santé végétale","Nutrition","Cartographie"], "SATELLITE"),
  ("Analyses labo", "Analyses de laboratoire",
   "Vos rapports sont importés et confrontés aux cibles de la culture. La plateforme détecte les antagonismes nutritionnels, ces blocages où un élément présent en quantité suffisante devient inaccessible à la plante à cause d'un autre.",
   "Score de fertilité de 68/100 : six paramètres conformes, trois à surveiller et une action requise. Le potassium est à 25,3 % sous la cible du stade.",
   ["Sol","Foliaire","Eau et sondes","Équilibre cationique","Conformité"], "LABO"),
  ("Pilotage", "Pilotage de l'exploitation",
   "La vue d'ensemble : secteurs configurés, services actifs, actions à traiter. Vous voyez d'un coup d'œil où en est chaque partie de l'exploitation et ce qui demande votre attention cette semaine.",
   "340 hectares, 12 secteurs configurés, 11 services sur 12 actifs et 4 actions à traiter cette semaine.",
   ["Connaissance du terrain","Surveillance","Nutrition et irrigation","Production"], "PILOTAGE"),
]
def scrolly():
    scr = {"CLIMAT": CLIMAT, "SATELLITE": SATELLITE, "LABO": LABO, "PILOTAGE": PILOTAGE}
    tabs = ''.join(f'<button type="button" role="tab" class="st-tab{" on" if i==0 else ""}" data-i="{i}" aria-selected="{"true" if i==0 else "false"}">{t[0]}</button>' for i, t in enumerate(SERVICES))
    frames = ''.join(f'<div class="st-frame{" on" if i==0 else ""}" data-i="{i}">{screen(scr[t[5]], "Écran " + t[1] + ", données de démonstration")}</div>' for i, t in enumerate(SERVICES))
    steps = ''
    for i, (tab, title, text, ex, tg, key) in enumerate(SERVICES):
        steps += f'''<article class="st-step{" on" if i==0 else ""}" data-i="{i}" id="service-{i+1}">
      <span class="k">SERVICE 0{i+1} · {tab.upper()}</span>
      <h2 class="h2">{title}</h2>
      <p>{text}</p>
      <div class="st-ex"><b>Exemple</b>{ex}</div>
      {tags(tg)}
      <div class="st-mobile">{screen(scr[key], "Écran " + title + ", données de démonstration")}</div>
    </article>'''
    return f'''<section class="scrolly" aria-label="Les quatre écrans de la plateforme">
  <div class="st-sticky">
    <div class="st-stage">
      <div class="st-tabs" role="tablist" aria-label="Écrans">{tabs}<span class="st-ink" aria-hidden="true"></span></div>
      <div class="st-frames">{frames}</div>
      <div class="st-progress" aria-hidden="true"><i></i></div>
    </div>
  </div>
  <div class="st-steps">{steps}</div>
</section>
'''
def service_row(n, title, text, tag_list, scr, label, rev=False, extra=""):
    return f'''<section class="split{' rev' if rev else ''}">
  <div class="txt">
    <span class="k sl">SERVICE 0{n}</span>
    <h2 class="h2 sl" style="transition-delay:.1s">{title}</h2>
    <p class="sl" style="transition-delay:.2s">{text}</p>
    {extra}
    <div class="sl" style="transition-delay:.2s">{tags(tag_list)}</div>
  </div>
  <div class="media shot fi">{screen(scr, label)}</div>
</section>
'''

PLATEFORME = phero("laboratoire", "La plateforme",
  "La plateforme, en quatre écrans",
  "Douze services agronomiques, un seul tableau de bord. Chaque secteur est configuré une fois, puis tout s'enchaîne.", "60% center") + '<main>' + \
  scrolly() + f'''
<p class="demo-note">Interfaces reconstituées avec des données de démonstration. Aucune donnée d'exploitation réelle n'est affichée.</p>

<section class="sec situ">
  <div class="sec-head">
    <p class="eyebrow a2">En situation</p>
    <h2 class="h2 a2" style="transition-delay:.1s">Au bureau comme au champ</h2>
    <p class="lede a2" style="transition-delay:.15s">La même plateforme sur ordinateur, tablette et téléphone, là où les décisions se prennent.</p>
  </div>
  <div class="situ-grid">
    <figure class="situ-item wide a2"><img src="img/situ-pilotage.jpg" alt="Le tableau de bord Pilotage de Firmaty sur un ordinateur, au bureau d'une station de conditionnement" loading="lazy"><figcaption><b>Pilotage</b>Au bureau de la station, la vue d'ensemble des secteurs et des actions de la semaine.</figcaption></figure>
    <figure class="situ-item a2" style="transition-delay:.1s"><img src="img/situ-satellite.jpg" alt="L'écran Satellite de Firmaty sur une tablette tenue entre deux rangs d'orangers" loading="lazy" style="object-position:62% center"><figcaption><b>Satellite</b>Entre les rangs, la tendance de vigueur du secteur sous les yeux.</figcaption></figure>
    <figure class="situ-item a2" style="transition-delay:.2s"><img src="img/situ-climat.jpg" alt="L'écran Climat de Firmaty sur un téléphone, au pied d'un jeune agrume" loading="lazy" style="object-position:34% center"><figcaption><b>Climat</b>Au pied de l'arbre, la recommandation d'irrigation des prochaines 24 heures.</figcaption></figure>
    <figure class="situ-item wide a2"><img src="img/situ-labo.jpg" alt="L'écran Laboratoire de Firmaty sur un ordinateur, au milieu d'échantillons de sol et de feuilles" loading="lazy"><figcaption><b>Laboratoire</b>Au labo, les analyses confrontées aux cibles du stade dès leur import.</figcaption></figure>
  </div>
</section>


<section class="wrap20 sec-gap">
  <div class="box">
    <p class="eyebrow a2">Les services</p>
    <h2 class="h2 a2" style="transition-delay:.1s">Douze services, organisés en quatre familles</h2>
    <p class="lede a2" style="transition-delay:.15s">Chaque service s'active secteur par secteur. Vous démarrez avec ce dont vous avez besoin et vous complétez ensuite.</p>
    <div class="grid4">
      <article class="card a2">{dots(1,"Famille 1 sur 4")}<div class="txt"><h3>Connaissance du terrain</h3>{bullets(["Géolocalisation des parcelles","Cultures en place","Découpage en secteurs"])}</div></article>
      <article class="card a2" style="transition-delay:.1s">{dots(2,"Famille 2 sur 4")}<div class="txt"><h3>Surveillance et protection</h3>{bullets(["Météorologie","Imagerie satellite","Phytosanitaire"])}</div></article>
      <article class="card a2" style="transition-delay:.2s">{dots(3,"Famille 3 sur 4")}<div class="txt"><h3>Nutrition et irrigation</h3>{bullets(["Fertilisation","Analyses de laboratoire","Programmes"])}</div></article>
      <article class="card a2" style="transition-delay:.3s">{dots(4,"Famille 4 sur 4")}<div class="txt"><h3>Production</h3><p>Le suivi de la production complète la vue d'ensemble de l'exploitation. Nous détaillons ce module lors de la démonstration, selon vos cultures.</p></div></article>
    </div>
  </div>
</section>

<section class="sec">
  <div class="sec-head">
    <p class="eyebrow a2">Au quotidien</p>
    <h2 class="h2 a2" style="transition-delay:.1s">La synthèse du jour</h2>
    <p class="lede a2" style="transition-delay:.15s">Chaque matin, la plateforme résume l'état de l'exploitation : secteurs suivis, score de conformité, actions à traiter, et ce qui a été écarté.</p>
  </div>
  <div class="digest a2">
    <div class="digest-head"><b>Synthèse du jour</b><span>Mise à jour 06:00</span></div>
    <div class="kpis k3"><div class="kpi"><small>Secteurs</small><b>12/12</b></div><div class="kpi"><small>Conformité</small><b>68/100</b></div><div class="kpi"><small>Actions</small><b>2</b></div></div>
    <div class="drow"><span class="sec-b">B4</span><div><b>Agrumes</b><p>Baisse de vigueur confirmée physiologique par les conditions de la période.</p></div><span class="chip ok">Aucune action</span></div>
    <div class="drow"><span class="sec-b">C1</span><div><b>Avocat</b><p>Potassium à 25 % sous la cible du stade. Correction par fertigation.</p></div><span class="chip crit">À corriger</span></div>
    <div class="drow"><span class="sec-b">D2</span><div><b>Agrumes</b><p>Pression cochenille en hausse sur les prochaines 48 heures.</p></div><span class="chip warn">À surveiller</span></div>
    <p class="digest-src">Sources croisées : satellite · climat · laboratoire</p>
  </div>
</section>
</main>
''' + cta()

# ---------------------------------------------------------------- POUR QUI

AUD = [
  ("agriculteurs","Agriculteurs individuels","situ-climat","Agriculteur consultant l'écran Climat de Firmaty sur son téléphone, au pied d'un jeune agrume","34% center",
   "Votre exploitation, suivie comme celle des grands","Vous cultivez seul ou en famille, sur quelques hectares ou quelques dizaines. Firmaty vous donne la même lecture de vos parcelles que les grandes structures, sans capteur à installer et sans équipe technique.",
   "Vous parcourez vos parcelles quand vous le pouvez. Un stress ou une carence se voit quand il est déjà installé.",
   "Une alerte sur votre téléphone vous dit quel secteur regarder et quoi faire, jusqu'à 15 jours avant que la plante ne l'exprime.",
   ["Aucun capteur ni matériel à acheter","Des recommandations claires pour l'irrigation et la fertilisation","Moins d'eau et d'engrais gaspillés, des rendements préservés"]),
  ("cooperatives","Coopératives","prelevement-sol","Agronome prélevant un échantillon de sol entre deux rangs d'agrumes","35% center",
   "Un compte, tous les adhérents","Vous voyez quelles exploitations décrochent et vous envoyez votre technicien là où il sert.",
   "Le technicien apprend le problème quand l'adhérent appelle. Souvent trop tard.",
   "Les secteurs qui décrochent remontent d'eux-mêmes, avant l'appel de l'adhérent.",
   ["Vue d'ensemble de toutes les exploitations adhérentes","Priorisation des visites du technicien","Historique daté pour chaque adhérent"]),
  ("domaines","Domaines et exportateurs","station","Caisses d'oranges dans une station de conditionnement","center",
   "Vos volumes se jouent des mois avant la récolte","Une anomalie détectée au printemps est corrigeable. Constatée en réception, c'est une perte.",
   "La mauvaise nouvelle arrive au quai de réception, contrat déjà signé.",
   "Les écarts de vigueur, d'eau ou de nutrition sont repérés pendant la saison, quand ils se corrigent encore.",
   ["Suivi du calibre et du tonnage à engager","Jusqu'à 15 jours d'avance sur un stress hydrique","Corrections ciblées secteur par secteur"]),
  ("agregateurs","Agrégateurs et assureurs","vue-aerienne","Vue aérienne de parcelles de vergers","center",
   "Des preuves, pas du déclaratif","Historique daté, mesures horodatées, analyses rattachées au secteur. De quoi objectiver un conseil, un financement ou un sinistre.",
   "La preuve repose sur du déclaratif et des visites ponctuelles.",
   "Chaque constat s'appuie sur des images datées et des mesures rattachées au secteur.",
   ["Historique satellite rétroactif sur les mois écoulés","Mesures horodatées et traçables","Analyses rattachées au secteur concerné"]),
]
def audience_tabs():
    tabs = ''.join(f'<button type="button" role="tab" id="t-{k}" aria-controls="p-{k}" aria-selected="{"true" if i==0 else "false"}" class="aud-tab{" on" if i==0 else ""}" data-i="{i}"><span class="aud-n">0{i+1}</span>{lab}</button>' for i,(k,lab,*_) in enumerate(AUD))
    imgs = ''.join(f'<img class="aud-img{" on" if i==0 else ""}" data-i="{i}" src="img/{img}.jpg" alt="{alt}" loading="lazy" style="object-position:{pos}">' for i,(k,lab,img,alt,pos,*_) in enumerate(AUD))
    panels = ''
    for i,(k,lab,img,alt,pos,title,intro,today,withf,gets) in enumerate(AUD):
        panels += f'''<div class="aud-panel{" on" if i==0 else ""}" role="tabpanel" id="p-{k}" aria-labelledby="t-{k}" data-i="{i}"{"" if i==0 else " hidden"}>
        <p class="eyebrow">{lab}</p>
        <h2 class="h2">{title}</h2>
        <p class="aud-intro">{intro}</p>
        <div class="cmp"><div class="today"><b>Aujourd'hui</b>{today}</div><div class="with"><b>Avec Firmaty</b>{withf}</div></div>
        {bullets(gets)}
      </div>'''
    anchors = ''.join(f'<span id="{k}" class="aud-anchor"></span>' for k,*_ in AUD)
    return f'''<section class="aud a2">{anchors}
  <div class="aud-tabs" role="tablist" aria-label="Profils">{tabs}</div>
  <div class="aud-body">
    <div class="aud-media">{imgs}</div>
    <div class="aud-panels">{panels}</div>
  </div>
</section>
'''
def audience(img, alt, eyebrow, title, intro, today, withf, gets, rev=False, pos="center"):
    return f'''<section class="split{' rev' if rev else ''}">
  <div class="txt">
    <p class="eyebrow sl">{eyebrow}</p>
    <h2 class="h2 sl" style="transition-delay:.1s">{title}</h2>
    <p class="sl" style="transition-delay:.2s">{intro}</p>
    <div class="cmp sl" style="transition-delay:.2s">
      <div class="today"><b>Aujourd'hui</b>{today}</div>
      <div class="with"><b>Avec Firmaty</b>{withf}</div>
    </div>
    <div class="sl" style="transition-delay:.2s">{bullets(gets)}</div>
  </div>
  <div class="media fi"><img src="img/{img}.jpg" alt="{alt}" loading="lazy" style="object-position:{pos}"></div>
</section>
'''

POURQUI = phero("station", "Pour qui",
  "Conçu pour ceux qui ne peuvent plus tout parcourir",
  "Agriculteur individuel, coopérative de deux cents adhérents ou domaine d'un seul tenant, la question est la même : à partir d'une certaine surface, vous ne pouvez plus tout voir. C'est là que la détection à distance change l'économie de votre exploitation.") + '<main>' + \
  audience_tabs() + f'''
<section class="wrap20 sec-gap">
  <div class="box">
    <p class="eyebrow a2">Comment ça se passe</p>
    <h2 class="h2 a2" style="transition-delay:.1s">Trois étapes, aucune installation au champ</h2>
    <div class="grid3">
      <article class="card a2">{dots(1,"Étape 1 sur 3")}<div class="txt"><span class="k">ÉTAPE 01</span><h3>On délimite vos secteurs</h3><p>Vous nous indiquez les contours de vos parcelles et les cultures en place. Aucun capteur, aucun matériel à installer, la mise en route se fait à distance.</p></div></article>
      <article class="card a2" style="transition-delay:.1s">{dots(2,"Étape 2 sur 3")}<div class="txt"><span class="k">ÉTAPE 02</span><h3>On croise les données</h3><p>L'historique satellite est remonté, confronté aux conditions climatiques de la période et à vos analyses de laboratoire si vous en avez déjà.</p></div></article>
      <article class="card a2" style="transition-delay:.2s">{dots(3,"Étape 3 sur 3")}<div class="txt"><span class="k">ÉTAPE 03</span><h3>On vous restitue</h3><p>On passe ensemble sur ce que l'analyse a trouvé, ce qui relève du normal et ce qui mérite votre attention. Vous décidez de la suite.</p></div></article>
    </div>
  </div>
</section>

<section class="split">
  <div class="txt">
    <p class="eyebrow sl">Et votre agronome ?</p>
    <h2 class="h2 sl" style="transition-delay:.1s">Firmaty lui dit où aller</h2>
    <p class="sl" style="transition-delay:.2s">Votre agronome ne peut pas passer sur tous les secteurs chaque semaine, et l'œil ne détecte pas un déficit hydrique avant que la plante ne l'exprime. Firmaty priorise ses déplacements et documente ses décisions.</p>
    <p class="sl" style="transition-delay:.2s">Il garde la main sur le diagnostic final.</p>
    <a class="btn btn-blue sl" style="transition-delay:.2s;margin-top:30px" href="questions.html">Lire les questions fréquentes</a>
  </div>
  <div class="media fi"><img src="img/avocat.jpg" alt="Main d'agronome examinant une feuille d'avocatier" loading="lazy" style="object-position:70% center"></div>
</section>
</main>
''' + cta()

# ---------------------------------------------------------------- GALERIE
def fig(src, cap, w, h, pos="center"):
    full = f"img/{src}-hd.jpg" if src.startswith("situ-") else f"img/{src}.jpg"
    return f'<figure class="gitem fd"><button type="button" class="gbtn" data-full="{full}" data-cap="{cap}" aria-label="Agrandir : {cap}"><img src="img/{src}.jpg" alt="{cap}" width="{w}" height="{h}" loading="lazy" style="object-position:{pos}"></button><figcaption>{cap}</figcaption></figure>'
def figscr(scr, cap):
    return f'<figure class="gitem scr fd">{screen(scr, cap)}<figcaption>{cap}</figcaption></figure>'

GALERIE = phero("goutte-a-goutte", "Galerie",
  "Firmaty en images",
  "Du goutteur au laboratoire, de la vue satellite à la station de conditionnement : les lieux et les gestes que la plateforme accompagne.", "60% center") + f'''
<main>
<section class="sec">
  <div class="sec-head">
    <p class="eyebrow a2">Au champ et à l'écran</p>
    <h2 class="h2 a2" style="transition-delay:.1s">Ce que nous observons, ce que vous voyez</h2>
    <p class="lede a2" style="transition-delay:.15s">Cliquez sur une photo pour l'agrandir.</p>
    <div class="chips a2" role="group" aria-label="Filtrer la galerie"><button type="button" class="chip-btn on" data-f="all" aria-pressed="true">Tout</button><button type="button" class="chip-btn" data-f="photo" aria-pressed="false">Au champ</button><button type="button" class="chip-btn" data-f="scr" aria-pressed="false">Écrans</button></div>
  </div>
  <div class="masonry">
    {fig("hero","Verger d'agrumes au coucher du soleil",1536,1024,"70% center")}
    {fig("situ-pilotage","Pilotage : le tableau de bord au bureau de la station",1400,764)}
    {fig("situ-satellite","Satellite : la tendance de vigueur sur tablette, au verger",1400,764,"62% center")}
    {figscr(SATELLITE,"Écran Satellite : tendance de vigueur sur douze semaines")}
    {fig("goutte-a-goutte","Goutteur d'irrigation au pied d'un jeune agrume",1100,733)}
    {fig("avocat","Contrôle d'une feuille d'avocatier",1300,867)}
    {fig("vue-aerienne","Vue aérienne : un bloc moins vigoureux entre deux parcelles saines",1100,733)}
    {figscr(LABO,"Écran Laboratoire : écarts aux cibles du stade")}
    {fig("prelevement-sol","Prélèvement de sol à la tarière entre deux rangs",1100,733)}
    {fig("laboratoire","Échantillons de feuilles et de sol au laboratoire",1100,733)}
    {figscr(CLIMAT,"Écran Climat : irrigation et pression sanitaire")}
    {fig("station","Arrivée des oranges à la station de conditionnement",1100,733)}
    {fig("situ-climat","Climat : la recommandation d'irrigation sur téléphone",1400,764,"34% center")}
    {fig("situ-labo","Laboratoire : les écarts aux cibles du stade, au labo",1400,764)}
    {figscr(PILOTAGE,"Écran Pilotage : vue d'ensemble de l'exploitation")}
  </div>
  <p class="demo-note">Écrans reconstitués avec des données de démonstration.</p>
</section>
</main>
<div class="lb" id="lb" hidden role="dialog" aria-modal="true" aria-label="Photo agrandie">
  <button type="button" class="lb-x" id="lbX" aria-label="Fermer">✕</button>
  <button type="button" class="lb-nav prev" id="lbP" aria-label="Photo précédente">‹</button>
  <figure><img id="lbImg" alt=""><figcaption id="lbCap"></figcaption></figure>
  <button type="button" class="lb-nav next" id="lbN" aria-label="Photo suivante">›</button>
</div>
''' + cta()

# ---------------------------------------------------------------- QUESTIONS
PM = '<span class="pm" aria-hidden="true"><svg viewBox="0 0 14 14" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M7 1v12M1 7h12"/></svg></span>'
def qa(q, a, open_=False):
    return f'<details class="a2"{" open" if open_ else ""}><summary>{q}{PM}</summary><p>{a}</p></details>'

QUESTIONS = phero("prelevement-sol", "Questions",
  "Ce qu'on nous demande le plus souvent",
  "Tarification, matériel, imagerie, cultures, données : les réponses aux questions qui reviennent avant chaque démonstration.", "35% center") + f'''
<main>
<section class="sec faqs">
  <div class="faq-search a2">
    <label for="q" class="vh">Rechercher dans les questions</label>
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>
    <input id="q" type="search" placeholder="Rechercher : tarif, capteurs, Copernicus, données…" autocomplete="off">
    <span class="faq-count" aria-live="polite"></span>
  </div>
  <p class="faq-empty" hidden>Aucune réponse ne correspond. Posez votre question dans votre <a href="contact.html">demande de démonstration</a>.</p>
  <div class="faq-group">
    <div class="faq-side"><p class="eyebrow a2">Démarrer</p><h2 class="h3 a2">Tarifs et mise en route</h2></div>
    <div class="qa">
      {qa("Comment se situe votre tarification ?","Elle dépend de la surface suivie, du nombre de secteurs et des modules activés. Nous la construisons avec vous après la démonstration, une fois que le périmètre est clair. Nous ne nous comparons pas aux abonnements satellite à quelques euros l'hectare : ceux-ci vendent un accès à la donnée brute, pas un diagnostic.",True)}
      {qa("Faut-il installer des capteurs ou du matériel au champ ?","Non. L'imagerie et les données climatiques proviennent de sources externes. Les analyses de laboratoire sont celles que vous faites déjà, il suffit de nous transmettre les rapports. La plateforme sait aussi intégrer des sondes si vous en avez, mais rien n'est obligatoire pour démarrer.")}
      {qa("Faut-il attendre une saison pour voir des résultats ?","Non. L'historique satellite est rétroactif : nous pouvons analyser vos secteurs sur les mois écoulés sans rien installer et sans attendre. La première restitution porte déjà sur cet historique.")}
      {qa("Comment se passe la mise en route ?","Vous nous indiquez les contours de vos parcelles et les cultures en place. Nous remontons l'historique satellite, le croisons avec les conditions climatiques de la période et avec vos analyses si vous en avez, puis nous passons ensemble sur les résultats. Tout se fait à distance.")}
    </div>
  </div>
  <div class="faq-group">
    <div class="faq-side"><p class="eyebrow a2">La technologie</p><h2 class="h3 a2">Imagerie, cultures et sources</h2></div>
    <div class="qa">
      {qa("Quelle est la source et la résolution de l'imagerie satellite ?","Nous exploitons l'imagerie multispectrale du programme européen Copernicus, en résolution 10 mètres, avec une revisite régulière et un filtrage automatique de la couverture nuageuse. C'est la résolution qui permet de descendre au niveau du secteur plutôt que de la parcelle entière.")}
      {qa("Sur quelles cultures êtes-vous opérationnels ?","Le suivi satellite et climatique fonctionne sur toute culture en plein champ. Les référentiels agronomiques par stade sont plus avancés sur certaines cultures que sur d'autres. Nous vous le disons franchement lors de la démonstration, en fonction de ce que vous cultivez.")}
      {qa("Quelles analyses de laboratoire pouvez-vous intégrer ?","Les analyses de sol, les analyses foliaires et les analyses d'eau d'irrigation, ainsi que les relevés de sondes si vous en avez. Elles sont confrontées aux cibles de la culture, du stade et du secteur, et l'équilibre cationique est vérifié.")}
      {qa("Pourquoi croiser trois sources plutôt qu'une ?","Parce qu'un indice qui baisse ne veut rien dire tout seul. Une baisse de vigueur peut être normale en phase de développement des fruits, ou signaler une carence. Seul le croisement avec le stade, le climat et les analyses permet de faire la différence et d'éviter les déplacements inutiles.")}
    </div>
  </div>
  <div class="faq-group" id="donnees">
    <div class="faq-side"><p class="eyebrow a2">Organisation</p><h2 class="h3 a2">Vos équipes et vos données</h2></div>
    <div class="qa">
      {qa("On a déjà un ingénieur agronome. À quoi servez-vous ?","À lui dire où aller. Votre agronome ne peut pas passer sur tous les secteurs chaque semaine, et l'œil ne détecte pas un déficit hydrique avant que la plante ne l'exprime. Firmaty priorise ses déplacements et documente ses décisions. Il garde la main sur le diagnostic final.")}
      {qa("Que deviennent nos analyses et nos contours de parcelles ?","Ils restent votre propriété et sont cloisonnés par compte. Les modalités précises sont définies dans le contrat, et nous en parlons ouvertement avant tout engagement.")}
      {qa("Une coopérative peut-elle suivre tous ses adhérents ?","Oui. Un compte suffit pour tous les adhérents : vous voyez quelles exploitations décrochent et vous envoyez votre technicien là où il sert.")}
    </div>
  </div>
</section>
</main>
''' + cta(h2="Une autre question ?", p="Posez-la dans votre demande de démonstration. Nous y répondons pendant l'échange, avec vos parcelles sous les yeux.", btn="Poser ma question")

# ---------------------------------------------------------------- CONTACT
CONTACT = phero("avocat", "Démonstration",
  "Voyons ce que vos parcelles disent déjà",
  "L'historique satellite est rétroactif : nous pouvons analyser vos secteurs sur les mois écoulés sans rien installer et sans attendre.", "75% center") + '''
<main>
<section class="contact-wrap first" id="demo">
  <div class="contact a3">
    <div class="ct-copy">
      <p class="eyebrow sl">Demande de démonstration</p>
      <h2 class="h2 sl" style="transition-delay:.1s">Dites-nous ce que vous pilotez</h2>
      <p class="p1 sl" style="transition-delay:.2s">On vous montre ce que la plateforme en tire, sur vos propres secteurs.</p>
      <p class="sl" style="transition-delay:.2s">Vos informations servent uniquement à préparer cet échange.</p>
      <ul class="facts sl" style="transition-delay:.2s">
        <li>Aucun capteur à installer</li>
        <li>Analyse rétroactive de vos secteurs</li>
        <li>Imagerie Copernicus, résolution 10 m</li>
        <li>Vos données restent votre propriété</li>
      </ul>
    </div>
    <div class="ct-form fi" style="transition-delay:.15s">
      <form class="demo-form" novalidate aria-label="Demande de démonstration">
        <div class="f"><label for="nom">Nom et prénom</label><input id="nom" name="nom" placeholder="Votre nom complet" autocomplete="name"></div>
        <div class="f"><label for="fonction">Fonction</label><input id="fonction" name="fonction" placeholder="Directeur technique, agronome…"></div>
        <div class="f"><label for="structure">Structure</label><input id="structure" name="structure" placeholder="Exploitation ou organisme" autocomplete="organization"></div>
        <div class="f"><label for="type">Type de structure</label><select id="type" name="type"><option value="">Sélectionner</option><option>Agriculteur individuel</option><option>Coopérative ou groupement</option><option>Station de conditionnement ou exportateur</option><option>Domaine agricole</option><option>Agrégateur ou bureau d'études</option><option>Assurance ou financement</option><option>Autre</option></select></div>
        <div class="f"><label for="surface">Surface pilotée</label><select id="surface" name="surface"><option value="">Sélectionner</option><option>Moins de 50 ha</option><option>50 à 200 ha</option><option>200 à 1 000 ha</option><option>Plus de 1 000 ha</option></select></div>
        <div class="f"><label for="cultures">Cultures principales</label><input id="cultures" name="cultures" placeholder="Agrumes, avocat, olivier…"></div>
        <div class="f"><label for="region">Région</label><input id="region" name="region" placeholder="Souss-Massa, Gharb…"></div>
        <div class="f"><label for="tel">Téléphone</label><input id="tel" name="tel" type="tel" placeholder="+212 …" autocomplete="tel"></div>
        <div class="f full"><label for="email">Email professionnel</label><input id="email" name="email" type="email" placeholder="vous@exploitation.ma" autocomplete="email"></div>
        <div class="f full"><label for="msg">Ce que vous cherchez à mieux piloter</label><textarea id="msg" name="msg" rows="3" placeholder="Irrigation, nutrition, suivi des adhérents…"></textarea></div>
        <label class="consent" for="ok"><input type="checkbox" id="ok" name="ok">J'accepte que mes informations servent uniquement à préparer cet échange.</label>
        <div class="send"><button class="btn btn-cream" type="submit">Envoyer ma demande</button><span class="err" role="alert"></span></div>
      </form>
    </div>
  </div>
</section>

<section class="wrap20 sec-gap after-contact">
  <div class="box">
    <p class="eyebrow a2">Après votre demande</p>
    <h2 class="h2 a2" style="transition-delay:.1s">Ce qui se passe ensuite</h2>
    <div class="grid3">
      <article class="card a2">''' + dots(1,"Étape 1 sur 3") + '''<div class="txt"><span class="k">ÉTAPE 01</span><h3>Nous convenons d'un créneau</h3><p>Nous revenons vers vous pour fixer un échange et choisir les secteurs à analyser.</p></div></article>
      <article class="card a2" style="transition-delay:.1s">''' + dots(2,"Étape 2 sur 3") + '''<div class="txt"><span class="k">ÉTAPE 02</span><h3>Nous analysons vos secteurs</h3><p>À partir des contours de vos parcelles, nous remontons l'historique satellite et le croisons avec le climat et vos analyses.</p></div></article>
      <article class="card a2" style="transition-delay:.2s">''' + dots(3,"Étape 3 sur 3") + '''<div class="txt"><span class="k">ÉTAPE 03</span><h3>Nous restituons ensemble</h3><p>Ce qui relève du normal, ce qui mérite votre attention, et la suite si vous souhaitez continuer.</p></div></article>
    </div>
  </div>
</section>
</main>
'''


# ---------------------------------------------------------------- LEGAL PAGES
def legal(crumb, h1, lead, blocks):
    body = ''.join(f'<section class="legal-block a2"><h2 class="h3">{t}</h2>{c}</section>' for t, c in blocks)
    return f'''<header class="phero small" id="top">
  <img class="bg" src="img/vue-aerienne.jpg" alt="">
  <p class="crumb a1"><a href="index.html">Accueil</a><span aria-hidden="true">/</span><span>{crumb}</span></p>
  <h1 class="a1">{h1}</h1>
  <p class="lead a1">{lead}</p>
</header>
<main>
<section class="sec legal-page">{body}</section>
</main>
''' + cta(h2="Une question sur vos données ?", p="Écrivez-nous depuis la page démonstration. Nous répondons à toute demande concernant vos informations.", btn="Nous contacter")

TODO = '<span class="todo">à compléter</span>'

MENTIONS = legal("Mentions légales", "Mentions légales", "Les informations sur l'éditeur et l'hébergeur du site firmaty.com.", [
  ("Éditeur du site", f"<p>Firmaty · Agriculture de précision<br>Raison sociale : {TODO}<br>Forme juridique et capital : {TODO}<br>Siège social : {TODO}, Maroc<br>Registre du commerce et identifiant (ICE) : {TODO}<br>Directeur de la publication : {TODO}<br>Contact : via la page <a href=\"contact.html\">Démonstration</a></p>"),
  ("Hébergement", "<p>Le site est hébergé par Vercel Inc., États-Unis (vercel.com). Les fichiers du site sont distribués par son réseau de diffusion.</p>"),
  ("Propriété intellectuelle", "<p>Les textes, photographies, interfaces reconstituées et le logo Firmaty présentés sur ce site sont la propriété de Firmaty. Toute reproduction sans autorisation préalable est interdite.</p><p>Les écrans de la plateforme affichés sur le site sont reconstitués avec des données de démonstration. Ils ne contiennent aucune donnée d'exploitation réelle.</p>"),
  ("Imagerie satellite", "<p>L'imagerie satellite exploitée par la plateforme provient du programme européen Copernicus.</p>"),
])

CONFID = legal("Politique de confidentialité", "Politique de confidentialité", "Quelles informations nous recevons, pourquoi, et comment vous gardez la main dessus.", [
  ("Les informations que vous nous transmettez", "<p>Le formulaire de demande de démonstration recueille : nom et prénom, fonction, structure, type de structure, surface pilotée, cultures principales, région, téléphone, email professionnel et votre message.</p><p>Ces informations servent uniquement à préparer l'échange de démonstration et à vous recontacter. Elles ne sont ni revendues ni utilisées à des fins publicitaires.</p>"),
  ("Vos données d'exploitation", "<p>Les analyses de laboratoire et les contours de parcelles que vous nous confiez restent votre propriété et sont cloisonnés par compte. Les modalités précises sont définies dans le contrat, et nous en parlons ouvertement avant tout engagement.</p>"),
  ("Durée de conservation", f"<p>Les informations d'une demande de démonstration sont conservées pendant {TODO} après le dernier échange, puis supprimées.</p>"),
  ("Vos droits", f"<p>Conformément à la loi marocaine n° 09-08 relative à la protection des personnes physiques à l'égard du traitement des données à caractère personnel, vous disposez d'un droit d'accès, de rectification et d'opposition. Pour l'exercer, contactez-nous à {TODO}. Vous pouvez également saisir la CNDP (Commission nationale de contrôle de la protection des données à caractère personnel).</p>"),
  ("Services tiers", "<p>Le site charge ses polices de caractères depuis Google Fonts, ce qui transmet l'adresse IP de votre navigateur aux serveurs de Google. Le site est hébergé par Vercel Inc.</p>"),
])

COOKIES = legal("Cookies", "Cookies", "Ce que le site dépose, ou plutôt ne dépose pas, dans votre navigateur.", [
  ("Aucun cookie de suivi", "<p>Le site firmaty.com ne dépose aucun cookie publicitaire ni de mesure d'audience, et n'utilise aucun outil de suivi. Aucun bandeau de consentement n'est donc nécessaire.</p>"),
  ("Ce qui peut être échangé", "<p>Pour afficher les pages, votre navigateur contacte notre hébergeur (Vercel) et le service de polices Google Fonts. Ces échanges techniques ne servent pas à vous suivre d'un site à l'autre.</p>"),
  ("Si cela change", "<p>Si nous ajoutons un jour un outil de mesure d'audience, cette page sera mise à jour et votre accord sera demandé lorsque la loi l'exige.</p>"),
])


# ---------------------------------------------------------------- TARIFS
def offer(name, who, price, unit, items, cta, featured=False, note=""):
    li = ''.join(f'<li>{i}</li>' for i in items)
    return f'''<article class="offer a2{' feat' if featured else ''}">
      {'<span class="offer-badge">Le plus choisi</span>' if featured else ''}
      <h3>{name}</h3><p class="offer-who">{who}</p>
      <p class="offer-price">{price}<small>{unit}</small></p>
      <ul class="ticks">{li}</ul>
      {f'<p class="offer-note">{note}</p>' if note else ''}
      <a class="btn {'btn-cream' if featured else 'btn-blue'}" href="contact.html">{cta}</a>
    </article>'''

Y='<td class="y" aria-label="Inclus">●</td>'; N='<td class="n" aria-label="Non inclus">–</td>'
def row(label, a, b, c): return f'<tr><th scope="row">{label}</th>{a}{b}{c}</tr>'

TARIFS = phero("station", "Tarifs",
  "Un tarif construit sur votre exploitation",
  "Le prix dépend de la surface suivie, du nombre de secteurs et des modules activés. Commencez par un diagnostic de vos parcelles, puis choisissez le suivi qui vous convient.") + f'''
<main>
<section class="sec">
  <div class="sec-head">
    <p class="eyebrow a2">Nos offres</p>
    <h2 class="h2 a2" style="transition-delay:.1s">Trois façons de travailler avec Firmaty</h2>
    <p class="lede a2" style="transition-delay:.15s">Aucun capteur à installer, aucun matériel à acheter. Vous payez un diagnostic, pas un accès à de la donnée brute.</p>
  </div>
  <div class="offers">
    {offer("Diagnostic", "Pour découvrir ce que vos parcelles disent déjà", "Sur devis", "analyse ponctuelle",
      ["Délimitation de vos secteurs à distance","Historique satellite rétroactif sur les mois écoulés","Croisement avec le climat de la période","Intégration de vos analyses existantes","Restitution commentée avec un agronome"],
      "Demander un diagnostic", note="Déduit de votre abonnement si vous continuez.")}
    {offer("Exploitation", "Pour les agriculteurs, domaines, stations et exportateurs", "Sur devis", "par hectare et par an",
      ["Les quatre écrans : Climat, Satellite, Laboratoire, Pilotage","Synthèse du jour et actions secteur par secteur","Recommandations d'irrigation et de fertilisation","Alertes maladies et ravageurs par stade","Accompagnement à la mise en route"],
      "Demander une démo", featured=True)}
    {offer("Coopérative", "Pour les coopératives, agrégateurs et assureurs", "Sur devis", "selon le nombre d'adhérents",
      ["Tout le suivi Exploitation","Un compte pour tous les adhérents","Priorisation des visites du technicien","Historique daté et traçable par secteur","Interlocuteur dédié"],
      "Parler à notre équipe")}
  </div>
</section>

<section class="wrap20 sec-gap">
  <div class="box">
    <p class="eyebrow a2">Ce qui fait le prix</p>
    <h2 class="h2 a2" style="transition-delay:.1s">Trois critères, rien de caché</h2>
    <div class="grid3">
      <article class="card a2">{dots(1,"Critère 1 sur 3")}<div class="txt"><h3>La surface suivie</h3><p>Le nombre d'hectares que la plateforme analyse. C'est la base du tarif, et il baisse par hectare quand la surface augmente.</p></div></article>
      <article class="card a2" style="transition-delay:.1s">{dots(2,"Critère 2 sur 3")}<div class="txt"><h3>Le nombre de secteurs</h3><p>Chaque secteur est suivi et qualifié séparément. Plus le découpage est fin, plus le diagnostic est précis.</p></div></article>
      <article class="card a2" style="transition-delay:.2s">{dots(3,"Critère 3 sur 3")}<div class="txt"><h3>Les modules activés</h3><p>Climat, satellite, laboratoire, pilotage : vous activez ce dont vous avez besoin et vous complétez ensuite.</p></div></article>
    </div>
  </div>
</section>

<section class="sec">
  <div class="sec-head">
    <p class="eyebrow a2">Comparer</p>
    <h2 class="h2 a2" style="transition-delay:.1s">Ce que comprend chaque offre</h2>
  </div>
  <div class="cmp-wrap a2">
    <table class="cmp-table">
      <thead><tr><th scope="col"><span class="vh">Fonction</span></th><th scope="col">Diagnostic</th><th scope="col" class="feat">Exploitation</th><th scope="col">Coopérative</th></tr></thead>
      <tbody>
        {row("Historique satellite rétroactif",Y,Y,Y)}
        {row("Croisement climat et stade de la culture",Y,Y,Y)}
        {row("Intégration des analyses de laboratoire",Y,Y,Y)}
        {row("Suivi continu, image après image",N,Y,Y)}
        {row("Synthèse du jour et actions par secteur",N,Y,Y)}
        {row("Recommandation d'irrigation",N,Y,Y)}
        {row("Pression maladies et ravageurs",N,Y,Y)}
        {row("Plusieurs exploitations sur un compte",N,N,Y)}
        {row("Priorisation des visites du technicien",N,N,Y)}
      </tbody>
    </table>
  </div>
</section>

<section class="sec faqs">
  <div class="faq-group">
    <div class="faq-side"><p class="eyebrow a2">Tarifs</p><h2 class="h3 a2">Questions fréquentes</h2></div>
    <div class="qa">
      {qa("Pourquoi pas un prix affiché à l'hectare ?","Parce que le diagnostic dépend de votre découpage en secteurs et des modules utiles à vos cultures. Nous construisons le tarif avec vous après la démonstration, une fois le périmètre clair. Nous ne vendons pas un accès à de la donnée satellite brute, mais une lecture agronomique.",True)}
      {qa("Faut-il acheter du matériel ?","Non. L'imagerie et le climat proviennent de sources externes, et les analyses de laboratoire sont celles que vous faites déjà. Les sondes peuvent être intégrées si vous en avez, sans être obligatoires.")}
      {qa("Peut-on commencer petit ?","Oui. Le diagnostic porte sur les secteurs de votre choix, et chaque module s'active secteur par secteur. Vous élargissez quand les résultats vous ont convaincu.")}
      {qa("Que deviennent nos données si nous arrêtons ?","Vos analyses et vos contours de parcelles restent votre propriété. Les modalités de restitution sont précisées dans le contrat.")}
    </div>
  </div>
</section>
</main>
''' + cta(h2="Recevez une proposition pour vos parcelles", p="Indiquez votre surface, vos cultures et vos secteurs. Nous revenons vers vous avec un diagnostic et un tarif adapté.", btn="Demander un devis")


# ---------------------------------------------------------------- SERVICES
def svc_row(n, key, eyebrow, title, text, gets, media, rev=False, extra=""):
    return f'''<section class="srv{' rev' if rev else ''}" id="{key}">
  <div class="srv-txt">
    <p class="srv-n sl"><span>0{n}</span>{eyebrow}</p>
    <h2 class="h2 sl" style="transition-delay:.1s">{title}</h2>
    <p class="sl" style="transition-delay:.2s">{text}</p>
    {extra}
    <div class="sl" style="transition-delay:.25s">{bullets(gets)}</div>
  </div>
  <div class="srv-media fi">{media}</div>
</section>
'''

def photo(src, alt, pos="center"):
    return f'<img src="img/{src}.jpg" alt="{alt}" loading="lazy" style="object-position:{pos}">'

ALERTS = '''<div class="feed" data-play>
  <div class="feed-head"><b>Alertes automatiques</b><span class="live"><i></i>En temps réel</span></div>
  <ol class="feed-list">
    <li class="al crit"><span class="al-ic" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3c3 4 6 7.2 6 10.5A6 6 0 0 1 6 13.5C6 10.2 9 7 12 3z"/></svg></span><div><b>Stress hydrique détecté</b><p>Secteur Nord-Est : NDWI en baisse de 18 % en 5 jours</p><time>Il y a 2 heures</time></div></li>
    <li class="al warn"><span class="al-ic" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 19c0-8 6-13 14-14 0 8-5 14-14 14z"/><path d="M5 19l8-8"/></svg></span><div><b>Carence azotée probable</b><p>Secteur Sud : NDRE en dessous du seuil critique</p><time>Il y a 6 heures</time></div></li>
    <li class="al inf"><span class="al-ic" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="6" height="6" rx="1" transform="rotate(45 12 12)"/><path d="M7 7L4 4M17 17l3 3M4 7l3-3M20 17l-3 3"/></svg></span><div><b>Nouvelle image disponible</b><p>Sentinel-2 : couverture nuageuse 5 %, qualité optimale</p><time>Il y a 1 jour</time></div></li>
  </ol>
  <p class="feed-note">Exemples d'alertes, données de démonstration.</p>
</div>'''

INDICES = '''<dl class="indices sl" style="transition-delay:.2s">
  <div><dt>NDVI</dt><dd>Vigueur de la végétation</dd></div>
  <div><dt>NDWI</dt><dd>Teneur en eau du couvert</dd></div>
  <div><dt>NDRE</dt><dd>Statut azoté des feuilles</dd></div>
</dl>'''

SERVICES = phero("situ-satellite", "Services",
  "Des services agronomiques, pas un simple logiciel",
  "Nous lisons vos parcelles, nous vous alertons et nous vous disons quoi faire. La technologie travaille en coulisses ; vous recevez des décisions.", "60% center") + f'''
<main>
<section class="sec srv-index-wrap">
  <div class="sec-head">
    <p class="eyebrow a2">Ce que nous faisons pour vous</p>
    <h2 class="h2 a2" style="transition-delay:.1s">Cinq services, de la parcelle à la décision</h2>
    <p class="lede a2" style="transition-delay:.15s">Ils s'enchaînent naturellement : on commence par un diagnostic, puis on surveille, on pilote l'eau et la nutrition, et on vous accompagne dans la durée.</p>
  </div>
  <ol class="srv-index a2">
    <li><a href="#diagnostic"><span>01</span>Diagnostic</a></li>
    <li><a href="#surveillance"><span>02</span>Surveillance et alertes</a></li>
    <li><a href="#irrigation"><span>03</span>Irrigation</a></li>
    <li><a href="#nutrition"><span>04</span>Nutrition</a></li>
    <li><a href="#accompagnement"><span>05</span>Accompagnement</a></li>
  </ol>
</section>
''' + svc_row(1, "diagnostic", "Diagnostic de vos parcelles", "Voyons ce que vos parcelles disent déjà",
  "Vous nous indiquez les contours de vos parcelles et les cultures en place. Nous remontons l'historique satellite sur les mois écoulés, le croisons avec le climat de la période et avec vos analyses existantes, puis nous passons ensemble sur les résultats.",
  ["Aucun capteur, aucun matériel à installer","Historique rétroactif : des résultats sans attendre une saison","Ce qui relève du normal, ce qui mérite votre attention","Restitution commentée avec un agronome"],
  photo("prelevement-sol","Agronome prélevant un échantillon de sol entre deux rangs d'agrumes","35% center")) + \
svc_row(2, "surveillance", "Surveillance continue et alertes automatiques", "Ne ratez plus jamais un moment critique de vos cultures",
  "Surveillance satellite en continu avec alertes automatiques par intelligence artificielle. Chaque nouvelle image Sentinel-2 est analysée : vous détectez les problèmes jusqu'à 15 jours avant qu'ils ne deviennent visibles et recevez des recommandations actionnables.",
  ["Stress hydrique, carence azotée, pression sanitaire","Alertes qualifiées : les fausses alertes sont écartées","Une synthèse chaque matin, secteur par secteur","Couverture nuageuse filtrée automatiquement"],
  ALERTS, rev=True, extra=INDICES) + \
svc_row(3, "irrigation", "Pilotage de l'irrigation", "La bonne quantité d'eau, au bon moment",
  "Conditions en temps réel, prévisions à 24 heures et à 5 jours, évapotranspiration et déficit de pression de vapeur : la recommandation d'apport est calculée pour chaque secteur, selon la culture et son stade.",
  ["Recommandation d'apport sur les prochaines 24 heures","Créneaux conseillés pour limiter l'évaporation","Historique des apports et des conditions","Pression maladies et ravageurs selon le stade"],
  photo("situ-climat","L'écran Climat de Firmaty sur un téléphone, au pied d'un jeune agrume","34% center")) + \
svc_row(4, "nutrition", "Nutrition et analyses de laboratoire", "Corriger ce qui compte, avant la fin du stade",
  "Vos rapports de sol, foliaires et d'eau sont confrontés aux cibles de la culture et du stade. Nous détectons les antagonismes nutritionnels, ces blocages où un élément présent devient inaccessible à la plante, et vous indiquons la correction à apporter.",
  ["Score de fertilité par secteur","Écarts aux cibles du stade, élément par élément","Équilibre cationique et antagonismes","Correction par fertigation et calendrier"],
  photo("situ-labo","L'écran Laboratoire de Firmaty sur un ordinateur, au milieu d'échantillons de sol et de feuilles"), rev=True) + \
svc_row(5, "accompagnement", "Accompagnement et pilotage", "Un agronome à vos côtés, des données derrière chaque décision",
  "La vue d'ensemble de l'exploitation ou de la coopérative : secteurs configurés, actions de la semaine, historique daté. Nous restons à vos côtés pour lire les résultats et prioriser les interventions.",
  ["Vue d'ensemble de tous les secteurs ou de tous les adhérents","Priorisation des visites du technicien","Historique daté, utile pour un conseil, un financement ou un sinistre","Interlocuteur dédié"],
  photo("situ-pilotage","Le tableau de bord Pilotage de Firmaty au bureau d'une station de conditionnement")) + f'''
<section class="sec">
  <div class="sec-head">
    <p class="eyebrow a2">Les outils derrière nos services</p>
    <h2 class="h2 a2" style="transition-delay:.1s">Ce que vous voyez sur votre écran</h2>
  </div>
</section>
''' + scrolly() + f'''
<p class="demo-note">Interfaces reconstituées avec des données de démonstration. Aucune donnée d'exploitation réelle n'est affichée.</p>
</main>
''' + cta(h2="Commencez par un diagnostic de vos parcelles", p="Nous analysons vos secteurs sur les mois écoulés, sans rien installer. Découvrez ensuite les offres adaptées à votre exploitation.", btn="Voir les tarifs", href="tarifs.html")

# ---------------------------------------------------------------- MISSION
MISSION = '''<header class="s3" id="scan3d" data-ch="0">
  <div class="s3-stage" aria-hidden="true"></div>
  <img class="s3-fallback" src="img/vue-aerienne.jpg" alt="">
  <div class="s3-labels" aria-hidden="true"></div>
  <div class="s3-ui">
    <div class="s3-copy">
      <p class="crumb"><a href="index.html">Accueil</a><span aria-hidden="true">/</span><span>Notre mission</span></p>
      <div class="s3-step on" aria-live="polite">
        <img class="s3-mark" src="img/logo-feuille.png" alt="" aria-hidden="true">
        <h1>Démocratiser l'agriculture de précision</h1>
        <p>Chaque agriculteur devrait pouvoir lire ses parcelles comme le voit un satellite. Lancez le scan d'une exploitation et suivez ce que Firmaty fait de vos données.</p>
      </div>
      <div class="s3-step"><span class="s3-k">01 · Observer</span><h2>Le satellite balaie chaque secteur</h2><p>Chaque nouvelle image Sentinel-2 est analysée. La vigueur, l'eau et l'azote de chaque parcelle se dessinent, du rouge au vert.</p></div>
      <div class="s3-step"><span class="s3-k">02 · Croiser</span><h2>Trois sources se rejoignent</h2><p>L'image satellite descend sur le terrain avec le climat de la période et vos analyses de laboratoire. C'est ce croisement qui écarte les fausses alertes.</p></div>
      <div class="s3-step"><span class="s3-k">03 · Décider</span><h2>Une décision par secteur</h2><p>B4 baisse, mais c'est physiologique : personne ne se déplace. C1 manque de potassium : on corrige. D2 est sous surveillance. Voilà ce que nous mettons entre les mains de chaque agriculteur.</p></div>
    </div>
    <div class="s3-act">
      <div class="s3-dots" role="group" aria-label="Étapes du scan"><button type="button" aria-label="Introduction"></button><button type="button" aria-label="Observer"></button><button type="button" aria-label="Croiser"></button><button type="button" aria-label="Décider"></button></div>
      <button type="button" class="s3-go"><span class="s3-go-t">Lancer le scan</span><span class="s3-go-i" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg></span></button>
      <p class="s3-hint">Exploitation de démonstration · scène 3D interactive</p>
    </div>
  </div>
  <div class="s3-legend" aria-hidden="true"><span><i style="background:#d2463c"></i>Faible</span><span><i style="background:#e8c04a"></i>Moyen</span><span><i style="background:#43b06a"></i>Vigoureux</span></div>
</header>
<script src="vendor/three.min.js" defer></script>
<script src="scan.js" defer></script>
''' + f'''
<main>
<section class="manifesto" id="notre-conviction">
  <img class="mf-mark fi" src="img/logo-feuille.png" alt="" aria-hidden="true">
  <p class="eyebrow a2">Notre conviction</p>
  <p class="manifesto-q a2" style="transition-delay:.1s">L'agriculture de précision ne doit pas être <em>réservée aux grandes structures</em>. Ce que les satellites voient de vos parcelles, vous devez pouvoir le comprendre et l'utiliser, quelle que soit la taille de votre exploitation.</p>
</section>

<section class="mission page" id="notre-mission">
  <div class="mission-txt">
    <p class="eyebrow sl">Notre mission</p>
    <h2 class="h2 sl" style="transition-delay:.1s">Rendre l'agriculture de précision accessible à tous</h2>
    <p class="sl" style="transition-delay:.2s">Fondée en 2026, Firmaty s'est donnée pour mission de <b>rendre l'agriculture de précision accessible à tous</b>, des petites exploitations familiales aux grandes structures agricoles.</p>
    <p class="sl" style="transition-delay:.2s">Nous croyons que l'avenir de l'agriculture passe par une utilisation intelligente des données satellitaires et de l'intelligence artificielle. En combinant <b>l'imagerie Sentinel-2 gratuite</b> avec des algorithmes d'analyse avancés, nous permettons à chaque agriculteur de :</p>
    <ul class="mission-list sl" style="transition-delay:.25s">
      <li><span>01</span><div><b>Détecter 15 jours avant</b>Les problèmes, avant qu'ils ne deviennent visibles.</div></li>
      <li><span>02</span><div><b>Réduire les coûts</b>En optimisant l'irrigation et la fertilisation.</div></li>
      <li><span>03</span><div><b>Produire en préservant</b>Augmenter les rendements tout en préservant l'environnement.</div></li>
      <li><span>04</span><div><b>Décider sur des faits</b>Des décisions basées sur des données objectives.</div></li>
    </ul>
  </div>
  <div class="media fi"><img src="img/avocat.jpg" alt="Main d'agronome examinant une feuille d'avocatier" loading="lazy" style="object-position:72% center"></div>
</section>

<section class="wrap20 sec-gap">
  <div class="box road-box">
    <p class="eyebrow a2">Notre ambition</p>
    <h2 class="h2 a2" style="transition-delay:.1s">De 20 exploitations pilotes à plus de 1 000 fermes</h2>
    <p class="lede a2" style="transition-delay:.15s">Actuellement en phase pilote avec 20 exploitations au Maroc sur 200 hectares, Firmaty vise à accompagner plus de 1 000 fermes dans les deux prochaines années.</p>
    <ol class="road" data-play>
      <li class="r-done"><span class="road-dot"></span><p class="road-y">2026</p><h3>Création de Firmaty</h3><p>La conviction devient une entreprise : rendre l'observation de la Terre utile à chaque exploitation.</p></li>
      <li class="r-now"><span class="road-dot"></span><p class="road-y">Aujourd'hui</p><h3>Phase pilote au Maroc</h3><p><b>20 exploitations</b> et <b>200 hectares</b> suivis, pour éprouver le diagnostic sur le terrain, culture par culture.</p></li>
      <li class="r-next"><span class="road-dot"></span><p class="road-y">D'ici deux ans</p><h3>Plus de 1 000 fermes</h3><p>Étendre l'accompagnement aux exploitations familiales comme aux grandes structures, et démocratiser l'accès à l'agriculture de précision au Maroc.</p></li>
    </ol>
    <div class="road-stats">
      <div class="a2"><b data-count="20">20</b><span>exploitations pilotes</span></div>
      <div class="a2" style="transition-delay:.1s"><b data-count="200" data-suffix=" ha">200 ha</b><span>suivis aujourd'hui</span></div>
      <div class="a2" style="transition-delay:.2s"><b data-count="1000" data-sep="1" data-suffix="+">1 000+</b><span>fermes visées d'ici deux ans</span></div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="sec-head">
    <p class="eyebrow a2">Nos engagements</p>
    <h2 class="h2 a2" style="transition-delay:.1s">Ce en quoi nous croyons</h2>
  </div>
  <div class="grid4 values">
    <article class="card line a2"><span class="v-n">01</span><div class="txt"><h3>Accessible</h3><p>Des petites exploitations familiales aux grandes structures : sans capteur à installer, avec l'imagerie Sentinel-2 gratuite.</p></div></article>
    <article class="card line a2" style="transition-delay:.1s"><span class="v-n">02</span><div class="txt"><h3>Objectif</h3><p>Chaque recommandation s'appuie sur des mesures datées : satellite, climat et laboratoire, croisés plutôt que lus séparément.</p></div></article>
    <article class="card line a2" style="transition-delay:.2s"><span class="v-n">03</span><div class="txt"><h3>Sobre</h3><p>La bonne quantité d'eau et d'engrais, au bon endroit : produire plus en préservant les ressources.</p></div></article>
    <article class="card line a2" style="transition-delay:.3s"><span class="v-n">04</span><div class="txt"><h3>Transparent</h3><p>Vos analyses et vos parcelles restent votre propriété. Nous en parlons ouvertement avant tout engagement.</p></div></article>
  </div>
</section>

<section class="sec">
  <div class="sec-head">
    <p class="eyebrow a2">Sur quoi nous nous appuyons</p>
    <h2 class="h2 a2" style="transition-delay:.1s">Des données ouvertes, une lecture agronomique</h2>
  </div>
  <div class="grid3">
    <article class="card line a2">{ico("sat")}<div class="txt"><span class="k">COPERNICUS · SENTINEL-2</span><h3>L'œil du satellite</h3><p>L'imagerie multispectrale gratuite du programme européen, en résolution 10 mètres, avec une revisite régulière.</p></div></article>
    <article class="card line a2" style="transition-delay:.1s">{ico("cli")}<div class="txt"><span class="k">CLIMAT</span><h3>Le contexte de la période</h3><p>Historique, temps réel et prévisions, rapportés au stade de chaque culture.</p></div></article>
    <article class="card line a2" style="transition-delay:.2s">{ico("lab")}<div class="txt"><span class="k">LABORATOIRE ET IA</span><h3>La mesure et l'analyse</h3><p>Vos analyses de sol, foliaires et d'eau, et des algorithmes qui recoupent les trois sources.</p></div></article>
  </div>
  <p class="more-link a2"><a href="ressources.html">Nos ressources sur l'imagerie satellite et l'agriculture de précision →</a></p>
</section>
</main>
''' + cta(h2="Rejoignez la phase pilote", p="Nous accompagnons aujourd'hui 20 exploitations au Maroc. Parlez-nous de la vôtre : nous analysons vos secteurs sur les mois écoulés, sans rien installer.", btn="Rejoindre la phase pilote")

# ---------------------------------------------------------------- RESSOURCES
def res(cat, label, title, text, date, read, href, icon, external=True):
    tgt = ' target="_blank" rel="noopener"' if external else ''
    more = "Lire la ressource" if external else "Lire"
    return f'''<a class="res a2" data-cat="{cat}" href="{href}"{tgt}>
      <span class="res-art {cat}">{ico(icon, 40)}</span>
      <span class="res-cat">{label}</span>
      <h3>{title}</h3><p>{text}</p>
      <span class="res-meta"><span>{date}</span><span>{read}</span></span>
      <span class="res-more">{more}{' ↗' if external else ' →'}</span>
    </a>'''

RESSOURCES = phero("laboratoire", "Ressources",
  "Guides, références et formations",
  "Nos ressources pour maîtriser l'agriculture de précision et tirer parti de l'imagerie satellite sur vos cultures.", "60% center") + f'''
<main>
<section class="sec">
  <div class="chips a2" role="group" aria-label="Filtrer les ressources"><button type="button" class="chip-btn on" data-r="all" aria-pressed="true">Toutes</button><button type="button" class="chip-btn" data-r="guide" aria-pressed="false">Guides pratiques</button><button type="button" class="chip-btn" data-r="tech" aria-pressed="false">Technologie</button><button type="button" class="chip-btn" data-r="form" aria-pressed="false">Formation</button><button type="button" class="chip-btn" data-r="firm" aria-pressed="false">Firmaty</button></div>
  <div class="res-grid">
    {res("guide","Guides pratiques","Copernicus Sentinel-2 : Agriculture Applications","Guide officiel de l'ESA sur l'utilisation des données Sentinel-2 pour l'agriculture de précision et le suivi des cultures.","Janvier 2026","8 min de lecture","https://www.esa.int/Applications/Observing_the_Earth/Copernicus/Sentinel-2","sat")}
    {res("tech","Technologie","NASA Earth Observatory : Remote Sensing Agriculture","Comment la NASA utilise l'imagerie satellite pour surveiller la santé des cultures et optimiser les rendements agricoles mondiaux.","Janvier 2026","10 min de lecture","https://earthobservatory.nasa.gov/","cli")}
    {res("form","Formation","FAO : Digital Agriculture and Remote Sensing","Rapport de la FAO sur l'agriculture numérique, la télédétection satellite et leur impact sur la sécurité alimentaire mondiale.","Décembre 2025","12 min de lecture","https://www.fao.org/digital-agriculture/en/","lab")}
    {res("firm","Firmaty","Lexique : les indicateurs de la plateforme","Vigueur, teneur en eau, ET0, VPD, antagonismes nutritionnels : les mots de vos écrans et de vos synthèses, expliqués simplement.","Octobre 2026","5 min de lecture","methode.html#lexique","doc",False)}
    {res("firm","Firmaty","La méthode : pourquoi croiser trois sources","Un indice qui baisse ne veut rien dire tout seul. Comment le croisement satellite, climat et laboratoire écarte les fausses alertes.","Octobre 2026","6 min de lecture","methode.html","flow",False)}
    {res("firm","Firmaty","Questions fréquentes","Tarification, matériel, résolution de l'imagerie, cultures couvertes et propriété de vos données.","Octobre 2026","4 min de lecture","questions.html","ask",False)}
  </div>
</section>
</main>
''' + cta(h2="Une question sur vos parcelles ?", p="Nos ressources ne remplacent pas un diagnostic. Parlez-nous de votre exploitation et nous vous montrons ce que la plateforme en tire.", btn="Demander une démo")
