# Shared building blocks for every Firmaty page.
LOGO = '<svg viewBox="0 0 84 46" fill="none" aria-hidden="true"><g stroke="{c}" stroke-width="3" stroke-linecap="round"><rect x="5" y="16" width="22" height="22" rx="3" transform="rotate(-30 16 27)"/><rect x="30" y="10" width="22" height="22" rx="3" transform="rotate(-30 41 21)"/><path d="M57 34c8-1 15-5 21-12"/></g><g fill="{c}"><circle cx="16" cy="27" r="3.5"/><circle cx="41" cy="21" r="3.5"/><circle cx="78" cy="9" r="4.5"/></g></svg>'

PAGES = [
    ("mission.html", "Notre mission"),
    ("services.html", "Services"),
    ("methode.html", "La méthode"),
    ("pour-qui.html", "Pour qui"),
    ("tarifs.html", "Tarifs"),
]


def leaf(blue="#274B9C", green="#5CBB4C", vein="#FFFBF3", size=None):
    """Firmaty mark: a two-tone leaf whose veins converge on the midrib (three sources, one decision)."""
    wh = f' width="{size}" height="{size}"' if size else ''
    return (f'<svg class="leaf" viewBox="0 0 48 48"{wh} aria-hidden="true">'
            f'<path d="M9 39C9 19 22 6 42 6L9 39Z" fill="{blue}"/>'
            f'<path d="M9 39L42 6C42 26 29 39 9 39Z" fill="{green}"/>'
            f'<path d="M9 39L36 12M17 31C15.5 26.5 15.5 22 17 18M24 24C23 20 23.5 16 26 12.5M17 31C21.5 32.5 26 32.5 30 30.5M24 24C28 25 32 24.5 35.5 22" '
            f'fill="none" stroke="{vein}" stroke-width="1.8" stroke-linecap="round"/>'
            f'<path d="M9 39L4.5 43.5" stroke="{blue}" stroke-width="2.6" stroke-linecap="round"/></svg>')

def logo_html(alt):
    return f'<span class="logo-mark">{leaf()}</span><b>Firmaty</b><span class="vh">{alt}</span>'

CUR = ' aria-current="page"'

def header(current):
    links = ''.join(
        f'<li><a href="{h}"{CUR if h == current else ""}>{t}</a></li>' for h, t in PAGES)
    drop = ''.join(f'<a href="{h}"{CUR if h == current else ""}>{t}</a>' for h, t in PAGES)
    return f'''<div class="hdr" id="hdr">
  <nav class="bar" aria-label="Navigation principale">
    <a class="logo" href="index.html"><img src="img/logo-firmaty.png" alt="Firmaty, accueil" width="529" height="140"></a>
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
    nav = '<li><a href="index.html">Accueil</a></li>' + ''.join(f'<li><a href="{h}">{t}</a></li>' for h, t in PAGES) + '<li><a href="galerie.html">Galerie</a></li><li><a href="questions.html">Questions</a></li><li><a href="contact.html">Démonstration</a></li>'
    return f'''<footer>
  <div class="foot-wrap">
    <div class="foot">
      <div class="grid">
        <div>
          <a class="logo" href="index.html"><img src="img/logo-firmaty.png" alt="Firmaty" width="529" height="140" loading="lazy"></a>
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
        <div class="ct"><h4>Contact</h4><p>Firmaty<br>Agriculture de précision<br>Maroc</p><p>{contact_lines() or "Démonstration sur demande<br>web : firmaty.com"}</p></div>
        <div class="follow"><h4>Ressources</h4><ul><li><a href="ressources.html">Ressources</a></li><li><a href="methode.html#lexique">Lexique</a></li><li><a href="questions.html">Questions fréquentes</a></li><li><a href="confidentialite.html">Vos données</a></li><li><a href="contact.html">Demander une démo</a></li></ul></div>
      </div>
    </div>
  </div>
  <div class="legal"><span>© 2026 Firmaty. Tous droits réservés.</span><a href="mentions-legales.html">Mentions légales</a><a href="confidentialite.html">Politique de confidentialité</a><a href="cookies.html">Cookies</a></div>
</footer>
<a class="up" id="up" href="#top" aria-label="Revenir en haut"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M12 19V5M5 12l7-7 7 7"/></svg></a>
'''

# ------------------------------------------------------------------
# Real contact details and pilot-farmer testimonials.
# Leave a value as None (or the list empty) and the matching block
# stays hidden on the site. Fill them in with the client's real data.
CONTACT = {
    "whatsapp": None,   # international format without + or spaces, e.g. "2126XXXXXXXX"
    "phone": None,      # as displayed, e.g. "+212 6 XX XX XX XX"
    "address": None,    # e.g. "Rue ..., Agadir, Maroc"
}
TESTIMONIALS = [
    # {"name": "...", "role": "Exploitant pilote", "farm": "...", "place": "...",
    #  "crop": "...", "surface": "... ha", "photo": "img/temoin-1.jpg",
    #  "quote": "...", "since": "Phase pilote 2026"},
]

def _wa_link(text="Bonjour Firmaty, je souhaite un diagnostic gratuit de mes parcelles."):
    from urllib.parse import quote
    return f"https://wa.me/{CONTACT['whatsapp']}?text={quote(text)}"

WA_ICON = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38a9.9 9.9 0 0 0 4.74 1.21h.01c5.46 0 9.91-4.45 9.91-9.91A9.85 9.85 0 0 0 12.04 2Zm0 18.15h-.01a8.2 8.2 0 0 1-4.19-1.15l-.3-.18-3.12.82.83-3.04-.2-.31a8.23 8.23 0 0 1-1.26-4.38c0-4.54 3.7-8.24 8.25-8.24a8.24 8.24 0 0 1 8.24 8.25c0 4.54-3.7 8.23-8.24 8.23Zm4.52-6.16c-.25-.12-1.47-.72-1.7-.81-.23-.08-.39-.12-.56.13-.16.25-.64.81-.79.97-.14.17-.29.19-.54.06-.25-.12-1.05-.39-1.99-1.23-.74-.66-1.23-1.47-1.38-1.72-.14-.25-.02-.38.11-.51.11-.11.25-.29.37-.43.13-.15.17-.25.25-.42.08-.17.04-.31-.02-.43-.06-.13-.56-1.34-.76-1.84-.2-.48-.41-.42-.56-.42h-.48a.92.92 0 0 0-.66.31c-.23.25-.87.85-.87 2.07 0 1.22.89 2.4 1.01 2.56.12.17 1.75 2.67 4.24 3.74.59.26 1.05.41 1.41.52.59.19 1.13.16 1.56.1.48-.07 1.47-.6 1.67-1.18.21-.58.21-1.07.15-1.18-.06-.1-.23-.16-.48-.29Z"/></svg>'

def whatsapp_fab():
    if not CONTACT.get("whatsapp"):
        return ""
    return f'<a class="wa-fab" href="{_wa_link()}" target="_blank" rel="noopener" aria-label="Écrire à Firmaty sur WhatsApp">{WA_ICON}<span>WhatsApp</span></a>\n'

def contact_lines():
    out = []
    if CONTACT.get("phone"):
        tel = CONTACT["phone"].replace(" ", "")
        out.append(f'<a href="tel:{tel}">{CONTACT["phone"]}</a>')
    if CONTACT.get("whatsapp"):
        out.append(f'<a href="{_wa_link()}" target="_blank" rel="noopener">WhatsApp</a>')
    if CONTACT.get("address"):
        out.append(CONTACT["address"])
    return "<br>".join(out)

def testimonials():
    if not TESTIMONIALS:
        return ""
    cards = ""
    for i, t in enumerate(TESTIMONIALS):
        facts = "".join(f"<li><small>{k}</small>{t[v]}</li>" for k, v in [("Culture", "crop"), ("Surface", "surface"), ("Depuis", "since")] if t.get(v))
        cards += f'''<figure class="tm a2" style="transition-delay:{i*.1:.1f}s">
      <img class="tm-photo" src="{t['photo']}" alt="Portrait de {t['name']}" loading="lazy">
      <div class="tm-body">
        <blockquote>« {t['quote']} »</blockquote>
        <figcaption><b>{t['name']}</b><span>{t.get('role','')}{' · ' + t['farm'] if t.get('farm') else ''}{', ' + t['place'] if t.get('place') else ''}</span></figcaption>
        {f'<ul class="tm-facts">{facts}</ul>' if facts else ''}
      </div>
    </figure>'''
    wa = f'<a class="btn btn-blue tm-wa" href="{_wa_link()}" target="_blank" rel="noopener">{WA_ICON}Parler à un exploitant Firmaty</a>' if CONTACT.get("whatsapp") else ""
    return f'''<section class="tms" id="temoignages">
  <div class="tms-head">
    <p class="eyebrow a2">Ils pilotent avec Firmaty</p>
    <h2 class="h2 a2" style="transition-delay:.1s">La parole aux exploitants pilotes</h2>
  </div>
  <div class="tms-grid">{cards}</div>
  {wa}
</section>
'''

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Rethink+Sans:wght@500;600;700&family=Noto+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">'

FAVICON = "img/favicon-64.png"
SITE = "https://firmaty.com/"
SKIP = '<a class="skip" href="#contenu">Aller au contenu</a>\n'

def page(title, desc, current, body, is_index=False, full=False):
    url = SITE + ("" if current == "index.html" else current)
    head = (f'<title>{title}</title>\n<meta name="description" content="{desc}">\n'
            f'<link rel="canonical" href="{url}">\n<link rel="icon" type="image/png" href="{FAVICON}"><link rel="apple-touch-icon" href="img/apple-touch-icon.png">\n<meta name="theme-color" content="#274B9C">\n'
            f'<meta property="og:type" content="website"><meta property="og:site_name" content="Firmaty"><meta property="og:locale" content="fr_FR">\n'
            f'<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:url" content="{url}"><meta property="og:image" content="{SITE}img/hero.jpg">\n'
            f'<meta name="twitter:card" content="summary_large_image">\n{FONTS}\n<link rel="stylesheet" href="site.css">\n')
    body = body.replace('<main>', '<main id="contenu">', 1)
    body = body.replace('<!--TESTIMONIALS-->', testimonials())
    content = head + SKIP + header(current) + body + footer() + whatsapp_fab() + '<script src="site.js"></script>\n'
    if is_index and not full:
        return content  # the publisher wraps the main page in its own skeleton
    return ('<!doctype html>\n<html lang="fr">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            + head + '</head>\n<body>\n' + SKIP + header(current) + body + footer() + whatsapp_fab() + '<script src="site.js"></script>\n</body>\n</html>\n')

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
