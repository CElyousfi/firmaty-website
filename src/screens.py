# Full-size platform screens, rebuilt with the demonstration data from the Firmaty brief.
ON = ' class="on"'

def chrome(url, active):
    tabs = ''.join(f'<span{ON if t == active else ""}>{t}</span>' for t in ["Météo", "Satellite", "Analyses labo", "Pilotage"])
    return f'<div class="chrome"><b><i></i><i></i><i></i></b><span>firmaty.com/app/{url}</span></div><div class="app"><div class="tabs">{tabs}</div>'

CLIMAT = chrome("climat", "Météo") + '''
<h4>Climat et risques agricoles</h4><div class="meta">Secteur B4 · Agrumes · Historique · Instant · Prévisions 24h · Prévisions 5j</div>
<div class="kpis k4">
  <div class="kpi"><small>Température</small><b>26°</b><em>ressenti 26°</em></div>
  <div class="kpi"><small>Humidité</small><b>67 %</b><em>rosée 20°</em></div>
  <div class="kpi"><small>ET0 (5j)</small><b>32,1</b><em>mm cumulés</em></div>
  <div class="kpi"><small>VPD moyen</small><b>0,93</b><em>kPa · optimal</em></div>
</div>
<div class="lbl">Températures maximales · 5 jours</div>
<div class="bars5">
  <div><span>31°</span><i style="height:72%"></i><span>ven</span></div>
  <div><span>33°</span><i style="height:82%"></i><span>sam</span></div>
  <div><span>32°</span><i style="height:77%"></i><span>dim</span></div>
  <div><span>29°</span><i style="height:62%;opacity:.7"></i><span>lun</span></div>
  <div><span>28°</span><i style="height:57%;opacity:.7"></i><span>mar</span></div>
</div>
<div class="lbl">Pression maladies et ravageurs</div>
<div class="risk"><span>Pourriture des racines</span><div class="track"><i style="width:19%;background:var(--ok)"></i></div><span class="chip ok">Faible 19 %</span></div>
<div class="risk"><span>Cochenille farineuse</span><div class="track"><i style="width:48%;background:var(--warn)"></i></div><span class="chip warn">Modéré 48 %</span></div>
<div class="risk"><span>Anthracnose</span><div class="track"><i style="width:13%;background:var(--ok)"></i></div><span class="chip ok">Faible 13 %</span></div>
<div class="alert"><b>Irrigation recommandée sur les prochaines 24 h</b>Aucune précipitation attendue et évapotranspiration élevée. Apport modéré conseillé sur les créneaux de nuit.</div>
</div>'''

SATELLITE = chrome("satellite", "Satellite") + '''
<h4>Analyse satellite</h4><div class="meta">Secteur B4 · 12 semaines · Tendances · Stress hydrique · Santé végétale · Nutrition</div>
<div class="kpis k3">
  <div class="kpi"><small>Vigueur optimale</small><b>83,3 %</b><em>de la surface</em></div>
  <div class="kpi"><small>Surface en stress</small><b>0,0 %</b><em>hydratation correcte</em></div>
  <div class="kpi"><small>Tendance 12 sem.</small><b style="color:var(--warn)">−12 %</b><em>à surveiller</em></div>
</div>
<svg viewBox="0 0 360 132" style="margin-top:10px;width:100%" role="img" aria-label="Vigueur du secteur B4 passée de 0,82 à 0,72 sur douze semaines, toujours en zone optimale">
  <rect x="40" y="6" width="314" height="30" fill="rgba(47,125,74,.12)"/><rect x="40" y="36" width="314" height="30" fill="rgba(39,75,156,.06)"/><rect x="40" y="66" width="314" height="30" fill="rgba(185,122,14,.10)"/><rect x="40" y="96" width="314" height="20" fill="rgba(190,59,51,.09)"/>
  <g font-size="7.5" font-family="Noto Sans,sans-serif" fill="#274B9C" fill-opacity=".75"><text x="0" y="24">OPTIMAL</text><text x="0" y="54">ACCEPT.</text><text x="0" y="84">ALERTE</text><text x="0" y="109">CRITIQUE</text></g>
  <polyline fill="none" stroke="#274B9C" stroke-width="2.2" stroke-linejoin="round" points="40,13 66,12 92,15 118,14 144,18 170,20 196,22 222,25 248,27 274,30 300,32 327,34 354,35"/>
  <circle cx="354" cy="35" r="4" fill="#274B9C"/>
  <g font-size="8" font-family="Noto Sans,sans-serif" fill="#274B9C" fill-opacity=".7"><text x="40" y="129">S-12</text><text x="190" y="129">S-6</text><text x="338" y="129">S-0</text></g>
</svg>
<table class="mini"><thead><tr><th>Secteur</th><th>Vigueur</th><th>Eau</th><th>Statut</th></tr></thead><tbody>
  <tr><td>B4 · Agrumes</td><td>0,72</td><td>0,31</td><td><span class="chip ok">Optimal</span></td></tr>
  <tr><td>B5 · Agrumes</td><td>0,58</td><td>0,22</td><td><span class="chip n">Acceptable</span></td></tr>
  <tr><td>C1 · Avocat</td><td>0,47</td><td>0,14</td><td><span class="chip crit">À vérifier</span></td></tr>
</tbody></table>
<div class="alert"><b>Vigueur stable en phase productive</b>La baisse conjointe des deux indices correspond à la réallocation des ressources vers le fruit. Le secteur C1 fait exception et remonte en tête des priorités.</div>
</div>'''

LABO = chrome("laboratoire", "Analyses labo") + '''
<h4>Analyses de laboratoire</h4><div class="meta">Secteur B4 · composition sol · Conformité · Eau · Sol · Foliaire</div>
<div class="ring">
  <svg viewBox="0 0 60 60" role="img" aria-label="Score de fertilité 68 sur 100"><circle cx="30" cy="30" r="24" fill="none" stroke="#E7E8EB" stroke-width="7"/><circle cx="30" cy="30" r="24" fill="none" stroke="#274B9C" stroke-width="7" stroke-linecap="round" stroke-dasharray="102.5 150.8" transform="rotate(-90 30 30)"/><text x="30" y="34.5" text-anchor="middle" font-size="14" font-weight="700" font-family="Rethink Sans,sans-serif" fill="#274B9C">68</text></svg>
  <div><b>Score de fertilité 68/100</b>6 paramètres conformes · 3 à surveiller · 1 action requise</div>
</div>
<div class="lbl">Écart aux cibles du stade</div>
<div class="dev"><span>Potassium</span><div class="ax"><i style="right:50%;width:42.2%;background:var(--crit)"></i></div><span>−25,3 %</span></div>
<div class="dev"><span>Conductivité</span><div class="ax"><i style="right:50%;width:16.7%;background:var(--warn)"></i></div><span>−10,0 %</span></div>
<div class="dev"><span>pH</span><div class="ax"><i style="left:50%;width:12.2%;background:var(--warn)"></i></div><span>+7,3 %</span></div>
<div class="dev"><span>Magnésium</span><div class="ax"><i style="right:50%;width:6.2%;background:var(--warn)"></i></div><span>−3,7 %</span></div>
<div class="dev"><span>Calcium</span><div class="ax"><i style="left:50%;width:3%;background:var(--ok)"></i></div><span>+1,8 %</span></div>
<div class="alert crit"><b>Antagonisme nutritionnel détecté</b>Le potassium disponible est en retrait par rapport à la cible du stade. Le calibre du fruit est le premier poste affecté. Correction par fertigation recommandée avant la fin du stade.</div>
</div>'''

PILOTAGE = chrome("pilotage", "Pilotage") + '''
<h4>Exploitation de démonstration</h4><div class="meta">Agrumes et avocat · plein champ</div>
<div class="kpis k4">
  <div class="kpi"><small>Surface</small><b>340</b><em>hectares</em></div>
  <div class="kpi"><small>Secteurs</small><b>12</b><em>configurés</em></div>
  <div class="kpi"><small>Services</small><b>11/12</b><em>actifs</em></div>
  <div class="kpi"><small>Actions</small><b>4</b><em>à traiter</em></div>
</div>
<div class="lbl" style="display:flex;justify-content:space-between"><span>Configuration</span><span>90 %</span></div>
<div class="prog"><i></i></div>
<div class="meta">11 services sur 12 actifs · 4 actions à traiter cette semaine</div>
<div class="svc"><h5>1 · Connaissance du terrain</h5><div>Géolocalisation<span class="chip ok">Actif</span></div><div>Cultures<span class="chip ok">Actif</span></div><div>Secteurs<span class="chip ok">Actif</span></div></div>
<div class="svc"><h5>2 · Surveillance et protection</h5><div>Météorologie<span class="chip ok">Actif</span></div><div>Imagerie satellite<span class="chip ok">Actif</span></div><div>Phytosanitaire<span class="chip warn">4 risques</span></div></div>
<div class="svc"><h5>3 · Nutrition et irrigation</h5><div>Fertilisation<span class="chip ok">Actif</span></div><div>Analyses labo<span class="chip ok">Actif</span></div><div>Programmes<span class="chip crit">1 action</span></div></div>
</div>'''

def screen(inner, label):
    return f'<div class="screen static" role="img" aria-label="{label}">{inner}</div>'
