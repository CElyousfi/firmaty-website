import os, shutil, sys
sys.path.insert(0, os.path.dirname(__file__))
from parts import page
import pages

SRC = os.path.dirname(__file__)
OUT = os.path.join(SRC, '..', 'site')
os.makedirs(OUT, exist_ok=True)

css = open(os.path.join(SRC, 'base.css')).read() + open(os.path.join(SRC, 'extra.css')).read()
open(os.path.join(OUT, 'site.css'), 'w').write(css)
shutil.copy(os.path.join(SRC, 'site.js'), os.path.join(OUT, 'site.js'))
if os.path.exists(os.path.join(OUT, 'img')):
    shutil.rmtree(os.path.join(OUT, 'img'))
shutil.copytree(os.path.join(SRC, '..', 'img'), os.path.join(OUT, 'img'))

# home: same content as before, links now point to the inner pages
home = open(os.path.join(SRC, 'home_body.html')).read()
swaps = [
    ('href="#plateforme">En savoir plus</a>', 'href="methode.html">En savoir plus</a>'),
    ('href="#action"><img', 'href="plateforme.html"><img'),
    ('<a class="btn btn-blue" href="#demo">Voir une démonstration</a>', '<a class="btn btn-blue" href="galerie.html">Voir toute la galerie</a>'),
]
for a, b in swaps:
    assert a in home, a
    home = home.replace(a, b)
desc = "Firmaty croise imagerie satellite, données climatiques et analyses de laboratoire pour vous dire où intervenir, secteur par secteur."
standalone = os.environ.get('STANDALONE') == '1'  # full HTML document for normal hosting (Vercel)
open(os.path.join(OUT, 'index.html'), 'w').write(page('Firmaty · Agriculture de précision', desc, 'index.html', home, is_index=not standalone))

for fname, title, body, d in [
    ('methode.html', 'La méthode · Firmaty', pages.METHODE, "Pourquoi croiser satellite, climat et laboratoire, comment le moteur qualifie un écart, et le lexique des indicateurs."),
    ('plateforme.html', 'La plateforme · Firmaty', pages.PLATEFORME, "Les quatre écrans et les douze services de la plateforme Firmaty."),
    ('pour-qui.html', 'Pour qui · Firmaty', pages.POURQUI, "Coopératives, domaines, stations, exportateurs, agrégateurs et assureurs : ce que Firmaty change pour chacun."),
    ('galerie.html', 'Galerie · Firmaty', pages.GALERIE, "Photos du terrain et écrans de la plateforme Firmaty."),
    ('questions.html', 'Questions · Firmaty', pages.QUESTIONS, "Tarification, matériel, imagerie, cultures et données : les réponses aux questions fréquentes."),
    ('tarifs.html', 'Tarifs · Firmaty', pages.TARIFS, "Les offres Firmaty : diagnostic, exploitation et coopérative, et ce qui détermine le tarif."),
    ('mentions-legales.html', 'Mentions légales · Firmaty', pages.MENTIONS, "Éditeur, hébergeur et propriété intellectuelle du site Firmaty."),
    ('confidentialite.html', 'Politique de confidentialité · Firmaty', pages.CONFID, "Comment Firmaty traite les informations transmises via le site."),
    ('cookies.html', 'Cookies · Firmaty', pages.COOKIES, "Le site Firmaty ne dépose aucun cookie de suivi."),
    ('contact.html', 'Démonstration · Firmaty', pages.CONTACT, "Demandez une démonstration de Firmaty sur vos propres secteurs."),
]:
    open(os.path.join(OUT, fname), 'w').write(page(title, d, fname, body))
print('built', sorted(os.listdir(OUT)))
