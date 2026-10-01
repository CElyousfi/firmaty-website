# Shared building blocks for every Firmaty page.
LOGO = '<svg viewBox="0 0 84 46" fill="none" aria-hidden="true"><g stroke="{c}" stroke-width="3" stroke-linecap="round"><rect x="5" y="16" width="22" height="22" rx="3" transform="rotate(-30 16 27)"/><rect x="30" y="10" width="22" height="22" rx="3" transform="rotate(-30 41 21)"/><path d="M57 34c8-1 15-5 21-12"/></g><g fill="{c}"><circle cx="16" cy="27" r="3.5"/><circle cx="41" cy="21" r="3.5"/><circle cx="78" cy="9" r="4.5"/></g></svg>'

PAGES = [
    ("methode.html", "La méthode"),
    ("plateforme.html", "La plateforme"),
    ("pour-qui.html", "Pour qui"),
    ("galerie.html", "Galerie"),
    ("questions.html", "Questions"),
]

CUR = ' aria-current="page"'

def header(current):
    links = ''.join(
        f'<li><a href="{h}"{CUR if h == current else ""}>{t}</a></li>' for h, t in PAGES)
    drop = ''.join(f'<a href="{h}"{CUR if h == current else ""}>{t}</a>' for h, t in PAGES)
    return f'''<div class="hdr" id="hdr">
  <nav class="bar" aria-label="Navigation principale">
    <a class="logo" href="index.html" aria-label="Firmaty, accueil">{LOGO.format(c="#274B9C")}<b>Firmaty</b></a>
    <ul class="links">
      {links}
      <li class="cta"><a class="btn btn-blue" href="contact.html">Demander une démo</a></li>
      <li class="bl"><button class="burger" id="burger" aria-expanded="false" aria-controls="drop" aria-label="Ouvrir le menu"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button></li>
    </ul>
  </nav>
</div>
<div class="drop" id="drop"><a href="index.html">Accueil</a>{drop}<a class="btn btn-blue" href="contact.html">Demander une démo</a></div>
'''

def footer():
    nav = '<li><a href="index.html">Accueil</a></li>' + ''.join(f'<li><a href="{h}">{t}</a></li>' for h, t in PAGES) + '<li><a href="contact.html">Démonstration</a></li>'
    return f'''<footer>
  <div class="foot-wrap">
    <div class="foot">
      <div class="grid">
        <div>
          <a class="logo" href="index.html" aria-label="Firmaty">{LOGO.format(c="#274B9C")}<b>Firmaty</b></a>
          <div class="ft-text">
            <p>Firmaty · Agriculture de précision<br>Le diagnostic agronomique qui croise toutes vos sources de données<br>Maroc</p>
            <p>firmaty.com</p>
            <p>Imagerie satellite : programme européen Copernicus<br>Résolution 10 m, couverture nuageuse filtrée</p>
          </div>
          <div class="marks">
            <div class="mark"><svg viewBox="0 0 42 42" fill="none" stroke="#274B9C" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><circle cx="21" cy="21" r="19"/><rect x="16" y="16" width="10" height="10" rx="1.5" transform="rotate(45 21 21)"/><path d="M12 12l-4-4M30 30l4 4"/></svg><span>Satellite<small>Multispectral</small></span></div>
            <div class="mark"><svg viewBox="0 0 42 42" fill="none" stroke="#274B9C" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><circle cx="21" cy="21" r="19"/><path d="M15 28h13a5 5 0 0 0 0-10 7 7 0 0 0-13 2 4 4 0 0 0 0 8z"/></svg><span>Climat<small>Temps réel et prévisions</small></span></div>
            <div class="mark"><svg viewBox="0 0 42 42" fill="none" stroke="#274B9C" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><circle cx="21" cy="21" r="19"/><path d="M17 11h8M18.5 11v8L12 29a2 2 0 0 0 2 3h14a2 2 0 0 0 2-3l-6.5-10v-8"/></svg><span>Laboratoire<small>Sol, foliaire, eau</small></span></div>
          </div>
        </div>
        <div><h4>Navigation</h4><ul>{nav}</ul></div>
        <div class="ct"><h4>Contact</h4><p>Firmaty<br>Agriculture de précision<br>Maroc</p><p>Démonstration sur demande<br>web : firmaty.com</p></div>
        <div class="follow"><h4>Ressources</h4><ul><li><a href="methode.html#lexique">Lexique</a></li><li><a href="questions.html">Questions fréquentes</a></li><li><a href="confidentialite.html">Vos données</a></li><li><a href="contact.html">Demander une démo</a></li></ul></div>
      </div>
    </div>
  </div>
  <div class="legal"><span>© 2026 Firmaty. Tous droits réservés.</span><a href="mentions-legales.html">Mentions légales</a><a href="confidentialite.html">Politique de confidentialité</a><a href="cookies.html">Cookies</a></div>
</footer>
<a class="up" id="up" href="#top" aria-label="Revenir en haut"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M12 19V5M5 12l7-7 7 7"/></svg></a>
'''

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Rethink+Sans:wght@500;600;700&family=Noto+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">'

FAVICON = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='16' fill='%23274B9C'/%3E%3Cg transform='translate(8 14) scale(.58)' fill='none' stroke='%23FFFBF3' stroke-width='4.5' stroke-linecap='round'%3E%3Crect x='5' y='16' width='22' height='22' rx='3' transform='rotate(-30 16 27)'/%3E%3Crect x='30' y='10' width='22' height='22' rx='3' transform='rotate(-30 41 21)'/%3E%3Cpath d='M57 34c8-1 15-5 21-12'/%3E%3C/g%3E%3C/svg%3E"
SITE = "https://firmaty.com/"
SKIP = '<a class="skip" href="#contenu">Aller au contenu</a>\n'

def page(title, desc, current, body, is_index=False, full=False):
    url = SITE + ("" if current == "index.html" else current)
    head = (f'<title>{title}</title>\n<meta name="description" content="{desc}">\n'
            f'<link rel="canonical" href="{url}">\n<link rel="icon" href="{FAVICON}">\n<meta name="theme-color" content="#274B9C">\n'
            f'<meta property="og:type" content="website"><meta property="og:site_name" content="Firmaty"><meta property="og:locale" content="fr_FR">\n'
            f'<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:url" content="{url}"><meta property="og:image" content="{SITE}img/hero.jpg">\n'
            f'<meta name="twitter:card" content="summary_large_image">\n{FONTS}\n<link rel="stylesheet" href="site.css">\n')
    body = body.replace('<main>', '<main id="contenu">', 1)
    content = head + SKIP + header(current) + body + footer() + '<script src="site.js"></script>\n'
    if is_index and not full:
        return content  # the publisher wraps the main page in its own skeleton
    return ('<!doctype html>\n<html lang="fr">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            + head + '</head>\n<body>\n' + SKIP + header(current) + body + footer() + '<script src="site.js"></script>\n</body>\n</html>\n')

def phero(img, crumb, h1, lead, pos='center'):
    return f'''<header class="phero" id="top">
  <img class="bg" src="img/{img}.jpg" alt="" fetchpriority="high" style="object-position:{pos}">
  <p class="crumb a1"><a href="index.html">Accueil</a><span aria-hidden="true">/</span><span>{crumb}</span></p>
  <h1 class="a1">{h1}</h1>
  <p class="lead a1">{lead}</p>
</header>
'''

def cta(h2="Voyons ce que vos parcelles disent déjà", p="L'historique satellite est rétroactif : nous analysons vos secteurs sur les mois écoulés, sans rien installer et sans attendre. Dites-nous ce que vous pilotez, on vous montre ce que la plateforme en tire.", btn="Demander une démonstration", href="contact.html"):
    return f'''<section class="cta-wrap">
  <div class="band a3">
    <div class="band-txt">
      <p class="eyebrow sl">Démonstration</p>
      <h2 class="h2 sl" style="transition-delay:.1s">{h2}</h2>
    </div>
    <div class="band-side sl" style="transition-delay:.2s">
      <p>{p}</p>
      <a class="btn btn-cream" href="{href}">{btn}</a>
    </div>
  </div>
</section>
'''

def dots(n, label=None):
    d = ''.join('<i class="f"></i>' if k < n else '<i></i>' for k in range(4))
    lab = f' aria-label="{label}"' if label else ' aria-hidden="true"'
    return f'<div class="dots"{lab}>{d}</div>'
