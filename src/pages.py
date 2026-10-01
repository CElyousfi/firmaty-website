from parts import phero, cta, dots
from screens import CLIMAT, SATELLITE, LABO, PILOTAGE, screen

ICON = {
 "sat": '<rect x="19" y="17" width="10" height="10" rx="1.5" transform="rotate(-45 24 22)"/><g transform="rotate(-45 24 22)"><rect x="2" y="18" width="13" height="8" rx="1"/><rect x="33" y="18" width="13" height="8" rx="1"/><path d="M15 22h4M29 22h4M24 27v4M19.5 33.5a4.5 4.5 0 0 0 9 0z"/></g><path d="M7 37a8 8 0 0 0 5 5M3 36a13 13 0 0 0 9 9"/>',
 "cli": '<path d="M10 9a4 4 0 0 1 8 0v18.5a7.5 7.5 0 1 1-8 0z"/><path d="M14 16v15"/><path d="M27 27h13a5 5 0 0 0 0-10 7.5 7.5 0 0 0-14 2.5 4 4 0 0 0 1 7.5z"/><path d="M29 33l-2 4M35 33l-2 4M41 33l-2 4"/>',
 "lab": '<path d="M18 5h12M20.5 5v13L9.5 37.5A3.2 3.2 0 0 0 12.3 42h23.4a3.2 3.2 0 0 0 2.8-4.5L27.5 18V5"/><path d="M14 29h20"/><path d="M19 38c0-5 3.5-7.5 8-7.5 0 4.5-3.5 7.5-8 7.5zM19 38l4.5-4"/>',
 "coop": '<circle cx="24" cy="14" r="5"/><circle cx="10" cy="19" r="4"/><circle cx="38" cy="19" r="4"/><path d="M14 40c0-6 4.5-10 10-10s10 4 10 10M3 37c0-5 3-8 7-8M45 37c0-5-3-8-7-8"/>',
 "truck": '<rect x="3" y="14" width="25" height="18" rx="2"/><path d="M28 20h8l6 7v5H28"/><circle cx="12" cy="36" r="4"/><circle cx="35" cy="36" r="4"/>',
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
    <a class="btn btn-blue sl" style="transition-delay:.2s;margin-top:30px" href="plateforme.html">Voir la plateforme</a>
  </div>
  <div class="media fi"><img src="img/prelevement-sol.jpg" alt="Agronome prélevant un échantillon de sol dans un verger d'agrumes" loading="lazy"></div>
</section>

<section class="wrap20 sec-gap">
  <div class="box">
    <p class="eyebrow a2">Pourquoi le croisement change tout</p>
    <h2 class="h2 a2" style="transition-delay:.1s">Le même secteur, deux lectures</h2>
    <p class="lede a2" style="transition-delay:.15s">Exemple tiré de notre exploitation de démonstration : agrumes et avocat en plein champ, 340 hectares, 12 secteurs.</p>
    <div class="grid2">
      <article class="card a2">
        <span class="pill bad">Plateforme satellite seule</span>
        <div class="txt">
          <p class="stat">−11 % <small>/ 15 jours</small></p>
          <h3>Vigueur du secteur B4 : alerte envoyée</h3>
          <p>L'indice sort de sa moyenne, le système déclenche. Sans le stade de la culture ni les conditions de la période, il ne peut faire que ça. L'équipe se déplace sur B4 et ne trouve rien.</p>
          <p class="note">Pendant ce temps, la vraie carence sur C1 n'est pas détectée. Elle n'est visible que dans les analyses de laboratoire.</p>
        </div>
      </article>
      <article class="card a2" style="transition-delay:.1s">
        <span class="pill good">Firmaty · satellite + climat + laboratoire</span>
        <div class="txt">
          <p class="stat">3 sources</p>
          <h3>Fausse alerte écartée, vrai problème trouvé</h3>
          <p>Sur B4, les deux indices baissent ensemble en phase de développement des fruits et les conditions climatiques sont conformes : c'est physiologique, personne ne se déplace. Sur C1, l'analyse foliaire montre un potassium en retrait de 25 % sur la cible du stade.</p>
          <p class="note"><b>Recommandation générée :</b> corriger le potassium sur C1 par fertigation avant la fin du stade. Le calibre du fruit est le premier poste affecté.</p>
        </div>
      </article>
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
  <div class="grid4">
    <article class="card a2">{dots(1,"Étape 1 sur 4")}<div class="txt"><h3>Détecter</h3><p>Un indice satellite sort de sa tendance sur un secteur : vigueur, teneur en eau ou statut azoté.</p></div></article>
    <article class="card a2" style="transition-delay:.1s">{dots(2,"Étape 2 sur 4")}<div class="txt"><h3>Replacer dans le contexte</h3><p>L'écart est comparé au stade phénologique de la culture et aux conditions climatiques de la période.</p></div></article>
    <article class="card a2" style="transition-delay:.2s">{dots(3,"Étape 3 sur 4")}<div class="txt"><h3>Confronter aux mesures</h3><p>Les analyses de sol, foliaires et d'eau sont confrontées aux cibles du stade pour confirmer ou écarter une cause.</p></div></article>
    <article class="card a2" style="transition-delay:.3s">{dots(4,"Étape 4 sur 4")}<div class="txt"><h3>Qualifier et recommander</h3><p>Normal : aucune action. À surveiller : suivi rapproché. À corriger : priorité et correction proposées, secteur par secteur.</p></div></article>
  </div>
</section>

<section class="cta-wrap">
  <div class="band big a3">
    <div class="band-txt">
      <p class="eyebrow sl">L'avance</p>
      <p class="bignum sl" style="transition-delay:.1s">7 à 10 <small>jours</small></p>
    </div>
    <div class="band-side sl" style="transition-delay:.2s">
      <h3>C'est l'avance que vous prenez sur un stress hydrique.</h3>
      <p>L'indice de teneur en eau détecte un déficit avant que la plante ne l'exprime visuellement. Quand vos équipes le voient au champ, il est déjà installé. Sur une culture d'export, cette semaine et demie se lit directement dans le calibre du fruit et dans le tonnage que vous pourrez engager.</p>
    </div>
  </div>
</section>

<section class="sec">
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
  service_row(1, "Climat et pression sanitaire",
    "Conditions en temps réel, prévisions et recommandation d'irrigation calculée à partir de l'évapotranspiration et du déficit de pression de vapeur. La pression maladies et ravageurs est calculée en continu pour la culture et son stade en cours.",
    ["Historique","Prévisions 24h et 5j","Irrigation pilotée","Risques par stade"], CLIMAT, "Écran Climat avec données de démonstration",
    extra='<p class="sl" style="transition-delay:.2s">Exemple : sur le secteur B4, l\'évapotranspiration cumulée atteint 32,1 mm sur cinq jours sans pluie annoncée. La plateforme conseille un apport modéré sur les créneaux de nuit et signale une pression cochenille en hausse.</p>') + \
  service_row(2, "Analyse satellite",
    "Chaque secteur est suivi image après image, avec des seuils agronomiques qui distinguent l'optimal, l'acceptable et le critique. La tendance sur douze semaines révèle ce qu'une image isolée ne montrera jamais.",
    ["Tendances","Stress hydrique","Santé végétale","Nutrition","Cartographie"], SATELLITE, "Écran Satellite avec données de démonstration", rev=True,
    extra='<p class="sl" style="transition-delay:.2s">Exemple : la vigueur de B4 recule de 12 % en douze semaines mais reste en zone optimale. La baisse conjointe des deux indices correspond à la réallocation des ressources vers le fruit. C1, lui, remonte en tête des priorités.</p>') + \
  service_row(3, "Analyses de laboratoire",
    "Vos rapports sont importés et confrontés aux cibles de la culture. La plateforme détecte les antagonismes nutritionnels, ces blocages où un élément présent en quantité suffisante devient inaccessible à la plante à cause d'un autre.",
    ["Sol","Foliaire","Eau et sondes","Équilibre cationique","Conformité"], LABO, "Écran Laboratoire avec données de démonstration",
    extra='<p class="sl" style="transition-delay:.2s">Exemple : score de fertilité de 68/100, avec six paramètres conformes, trois à surveiller et une action requise. Le potassium est à 25,3 % sous la cible du stade.</p>') + \
  service_row(4, "Pilotage de l'exploitation",
    "La vue d'ensemble : secteurs configurés, services actifs, actions à traiter. Vous voyez d'un coup d'œil où en est chaque partie de l'exploitation et ce qui demande votre attention cette semaine.",
    ["Connaissance du terrain","Surveillance","Nutrition et irrigation","Production"], PILOTAGE, "Écran Pilotage avec données de démonstration", rev=True,
    extra='<p class="sl" style="transition-delay:.2s">Exemple : 340 hectares, 12 secteurs configurés, 11 services sur 12 actifs et 4 actions à traiter cette semaine.</p>') + f'''
<p class="demo-note">Interfaces reconstituées avec des données de démonstration. Aucune donnée d'exploitation réelle n'est affichée.</p>

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
  "Coopérative de deux cents adhérents ou domaine d'un seul tenant, la question est la même : à partir d'une certaine surface, vous ne pouvez plus tout voir. C'est là que la détection à distance change l'économie de votre exploitation.") + '<main>' + \
  audience("prelevement-sol","Agronome prélevant un échantillon de sol entre deux rangs d'agrumes","Coopératives et groupements","Un compte, tous les adhérents",
    "Vous voyez quelles exploitations décrochent et vous envoyez votre technicien là où il sert.",
    "Le technicien apprend le problème quand l'adhérent appelle. Souvent trop tard.",
    "Les secteurs qui décrochent remontent d'eux-mêmes, avant l'appel de l'adhérent.",
    ["Vue d'ensemble de toutes les exploitations adhérentes","Priorisation des visites du technicien","Historique daté pour chaque adhérent"]) + \
  audience("station","Caisses d'oranges dans une station de conditionnement","Domaines, stations et exportateurs","Vos volumes se jouent des mois avant la récolte",
    "Une anomalie détectée au printemps est corrigeable. Constatée en réception, c'est une perte.",
    "La mauvaise nouvelle arrive au quai de réception, contrat déjà signé.",
    "Les écarts de vigueur, d'eau ou de nutrition sont repérés pendant la saison, quand ils se corrigent encore.",
    ["Suivi du calibre et du tonnage à engager","Avance de 7 à 10 jours sur un stress hydrique","Corrections ciblées secteur par secteur"], rev=True) + \
  audience("vue-aerienne","Vue aérienne de parcelles de vergers","Agrégateurs, bureaux d'études et assurance récolte","Des preuves, pas du déclaratif",
    "Historique daté, mesures horodatées, analyses rattachées au secteur. De quoi objectiver un conseil, un financement ou un sinistre.",
    "La preuve repose sur du déclaratif et des visites ponctuelles.",
    "Chaque constat s'appuie sur des images datées et des mesures rattachées au secteur.",
    ["Historique satellite rétroactif sur les mois écoulés","Mesures horodatées et traçables","Analyses rattachées au secteur concerné"]) + f'''
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
    return f'<figure class="gitem fd"><button type="button" class="gbtn" data-full="img/{src}.jpg" data-cap="{cap}" aria-label="Agrandir : {cap}"><img src="img/{src}.jpg" alt="{cap}" width="{w}" height="{h}" loading="lazy" style="object-position:{pos}"></button><figcaption>{cap}</figcaption></figure>'
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
  </div>
  <div class="masonry">
    {fig("hero","Verger d'agrumes au coucher du soleil",1536,1024,"70% center")}
    {figscr(SATELLITE,"Écran Satellite : tendance de vigueur sur douze semaines")}
    {fig("goutte-a-goutte","Goutteur d'irrigation au pied d'un jeune agrume",1100,733)}
    {fig("avocat","Contrôle d'une feuille d'avocatier",1300,867)}
    {fig("vue-aerienne","Vue aérienne : un bloc moins vigoureux entre deux parcelles saines",1100,733)}
    {figscr(LABO,"Écran Laboratoire : écarts aux cibles du stade")}
    {fig("prelevement-sol","Prélèvement de sol à la tarière entre deux rangs",1100,733)}
    {fig("laboratoire","Échantillons de feuilles et de sol au laboratoire",1100,733)}
    {figscr(CLIMAT,"Écran Climat : irrigation et pression sanitaire")}
    {fig("station","Arrivée des oranges à la station de conditionnement",1100,733)}
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
        <div class="f"><label for="type">Type de structure</label><select id="type" name="type"><option value="">Sélectionner</option><option>Coopérative ou groupement</option><option>Station de conditionnement ou exportateur</option><option>Domaine agricole</option><option>Agrégateur ou bureau d'études</option><option>Assurance ou financement</option><option>Autre</option></select></div>
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
