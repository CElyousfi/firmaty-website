# Firmaty · site vitrine

Site statique multipage (FR) : accueil, la méthode, la plateforme, pour qui, galerie, questions, démonstration.

## Structure

- `site/` : le site publié (HTML, `site.css`, `site.js`, `img/`). C'est le dossier servi par Vercel.
- `src/` : les sources qui génèrent `site/` (en-tête, pied de page et contenu de chaque page).
- `img/` : photos d'origine compressées, copiées dans `site/img/` à la génération.

## Modifier le site

1. Modifier les textes dans `src/pages.py` (pages intérieures) ou `src/home_body.html` (accueil), les styles dans `src/base.css` / `src/extra.css`.
2. Régénérer : `STANDALONE=1 python3 src/build.py`
3. Commit + push sur `main` : Vercel redéploie automatiquement.

## À compléter avant la mise en production

- Brancher le formulaire de démonstration sur un email ou un CRM (actuellement il valide et confirme sans envoyer).
- Liens LinkedIn / Instagram du pied de page.
- Pages mentions légales et politique de confidentialité.
- Services du module « Production ».
