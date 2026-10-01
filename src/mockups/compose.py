"""Fit the real Firmaty screens into the device photos (src/mockups/photos/*.png).

Usage: python3 src/mockups/compose.py  (after `STANDALONE=1 python3 src/build.py`)
Renders each screen with Playwright, warps it onto the white screen of the photo
and writes img/situ-<name>.jpg.
"""
import json, os, re, subprocess, sys, tempfile
import cv2, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from screens import CLIMAT, SATELLITE, LABO, PILOTAGE

JOBS = {  # name: (screen, css width, css height, browser bar, phone layout, light tone multiplier, RGB cast)
    "pilotage": (PILOTAGE, 780, 490, True, False, .975, (255, 251, 245)),
    "satellite": (SATELLITE, 700, 515, False, False, .975, (255, 250, 242)),
    "climat": ("PHONE", 380, 870, False, True, .97, (255, 250, 240)),
    "labo": (LABO, 780, 500, True, False, .985, (248, 250, 255)),
}
CSS = os.path.join(ROOT, 'site', 'site.css')

PHONE_CLIMAT = """<div class="ph">
<div class="ph-status"><b>9:41</b><span>●●● 5G ▮</span></div>
<div class="ph-head"><span class="ph-logo"></span><div><b>Climat</b><small>Secteur B4 · Agrumes</small></div></div>
<div class="ph-now"><div><span class="ph-temp">26°</span><small>ressenti 26° · ciel dégagé</small></div><span class="chip ok">VPD optimal</span></div>
<div class="ph-kpis"><div><small>Humidité</small><b>67 %</b></div><div><small>ET0 (5j)</small><b>32,1 mm</b></div><div><small>VPD moyen</small><b>0,93 kPa</b></div><div><small>Pluie 24 h</small><b>0 mm</b></div></div>
<div class="ph-card"><small>Températures max · 5 jours</small>
<div class="ph-bars"><div><span>31°</span><i style="height:72%"></i><em>ven</em></div><div><span>33°</span><i style="height:86%"></i><em>sam</em></div><div><span>32°</span><i style="height:79%"></i><em>dim</em></div><div><span>29°</span><i style="height:60%;opacity:.6"></i><em>lun</em></div><div><span>28°</span><i style="height:54%;opacity:.6"></i><em>mar</em></div></div></div>
<div class="ph-alert"><b>Irrigation recommandée · 24 h</b>Aucune pluie attendue, évapotranspiration élevée. Apport modéré conseillé de nuit.</div>
<div class="ph-card"><small>Pression maladies et ravageurs</small>
<div class="ph-risk"><span>Cochenille farineuse</span><b class="chip warn">48 %</b></div>
<div class="ph-risk"><span>Pourriture des racines</span><b class="chip ok">19 %</b></div>
<div class="ph-risk"><span>Anthracnose</span><b class="chip ok">13 %</b></div></div>
<nav class="ph-nav"><span class="on">Météo</span><span>Satellite</span><span>Labo</span><span>Pilotage</span></nav>
</div>"""
PHONE_CSS = """.ph{height:100%;display:flex;flex-direction:column;gap:12px;padding:0 18px 0;background:#fff;color:#274B9C;font-family:'Noto Sans',sans-serif}
.ph-status{display:flex;justify-content:space-between;font-size:14px;padding:14px 4px 0}.ph-status span{font-size:11px;letter-spacing:1px}
.ph-head{display:flex;align-items:center;gap:12px;margin-top:4px}.ph-head b{display:block;font-family:'Rethink Sans',sans-serif;font-size:24px;line-height:1.1}.ph-head small{font-size:13.5px;opacity:.65}
.ph-logo{width:40px;height:40px;border-radius:12px;background:#274B9C url(file://LOGO) center/70% no-repeat}
.ph-now{display:flex;justify-content:space-between;align-items:center;background:#F9F4E6;border-radius:18px;padding:14px 16px}
.ph-temp{font-family:'Rethink Sans',sans-serif;font-weight:700;font-size:54px;line-height:1}.ph-now small{display:block;font-size:13px;opacity:.7;margin-top:4px}
.ph-kpis{display:grid;grid-template-columns:1fr 1fr;gap:8px}.ph-kpis div{background:#FFFBF3;border:1px solid rgba(39,75,156,.1);border-radius:14px;padding:10px 12px}
.ph-kpis small,.ph-card>small{display:block;font-size:12.5px;opacity:.65}.ph-kpis b{font-family:'Rethink Sans',sans-serif;font-size:20px}
.ph-card{background:#FFFBF3;border:1px solid rgba(39,75,156,.1);border-radius:16px;padding:12px 14px}
.ph-bars{display:grid;grid-template-columns:repeat(5,1fr);gap:8px;height:96px;align-items:end;margin-top:8px}.ph-bars div{display:flex;flex-direction:column;align-items:center;justify-content:flex-end;height:100%;gap:3px;font-size:12px}
.ph-bars i{display:block;width:100%;background:#274B9C;border-radius:7px 7px 3px 3px}.ph-bars em{font-style:normal;opacity:.6}
.ph-alert{background:#274B9C;color:#FFFBF3;border-radius:16px;padding:13px 15px;font-size:13.5px;line-height:1.45}.ph-alert b{display:block;font-size:15px;margin-bottom:3px}
.ph-risk{display:flex;justify-content:space-between;align-items:center;font-size:14px;padding:7px 0;border-top:1px solid rgba(39,75,156,.08)}.ph-risk:first-of-type{border-top:0}
.ph .chip{font-size:12.5px;padding:3px 10px}
.ph-nav{margin-top:auto;display:flex;justify-content:space-around;border-top:1px solid rgba(39,75,156,.12);padding:12px 0 22px;font-size:13px;font-weight:600}.ph-nav span{opacity:.5}.ph-nav .on{opacity:1}"""


def page(inner, w, h, chrome, mobile):
    if inner == "PHONE":
        css = PHONE_CSS.replace("LOGO", os.path.join(ROOT, 'img', 'logo-symbole-blanc.png'))
        return (f'<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="file://{CSS}"><style>'
                f'html,body{{margin:0;width:{w}px;height:{h}px;overflow:hidden;background:#fff}}{css}</style></head><body>{PHONE_CLIMAT}</body></html>')
    if not chrome:
        inner = re.sub(r'<div class="chrome">.*?</span></div>', '', inner, count=1, flags=re.S)
    extra = '.kpis.k4,.kpis.k3{grid-template-columns:1fr 1fr!important}.app h4{font-size:19px}.screen{font-size:13.5px}.tabs{flex-wrap:nowrap;overflow:hidden}' if mobile else ''
    return (f'<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="file://{CSS}"><style>'
            f'html,body{{margin:0;background:#fff;width:{w}px;height:{h}px;overflow:hidden}}'
            f'.screen.static{{position:relative;border-radius:0!important;box-shadow:none!important;width:{w}px;height:{h}px;overflow:hidden;left:0;right:0;top:0}}'
            f'.app{{padding:16px 18px}}{extra}</style></head><body><div class="screen static">{inner}</div></body></html>')

def render(tmp):
    sizes = {}
    for n, (inner, w, h, ch, mob, *_ ) in JOBS.items():
        open(os.path.join(tmp, f'scr-{n}.html'), 'w').write(page(inner, w, h, ch, mob)); sizes[n] = [w, h]
    json.dump(sizes, open(os.path.join(tmp, 'sizes.json'), 'w'))
    js = ("const {chromium}=require('playwright');const d=process.argv[2];const s=require(d+'/sizes.json');(async()=>{const b=await chromium.launch();"
          "for(const [n,[w,h]] of Object.entries(s)){const p=await b.newPage({viewport:{width:w,height:h},deviceScaleFactor:2.6});"
          "await p.goto('file://'+d+'/scr-'+n+'.html');await p.waitForTimeout(400);await p.screenshot({path:d+'/scr-'+n+'.png'});await p.close()}await b.close()})();")
    open(os.path.join(tmp, 'r.js'), 'w').write(js)
    env = dict(os.environ, NODE_PATH=subprocess.check_output(['npm', 'root', '-g'], text=True).strip())
    subprocess.check_call(['node', os.path.join(tmp, 'r.js'), tmp], env=env)

def compose(tmp, K=2.0):
    corners = json.load(open(os.path.join(HERE, 'corners.json')))
    for n, (*_, k, rgb) in JOBS.items():
        ph = cv2.imread(os.path.join(HERE, 'photos', f'{n}.png')); ph = cv2.resize(ph, None, fx=K, fy=K, interpolation=cv2.INTER_LANCZOS4)
        H, W = ph.shape[:2]; scr = cv2.imread(os.path.join(tmp, f'scr-{n}.png')); sh, sw = scr.shape[:2]
        q = np.array(corners[n], np.float32) * K; c = q.mean(0); q = q + (q - c) / np.linalg.norm(q - c, axis=1, keepdims=True) * 3
        M = cv2.getPerspectiveTransform(np.float32([[0, 0], [sw, 0], [sw, sh], [0, sh]]), q)
        warp = cv2.warpPerspective(scr, M, (W, H), flags=cv2.INTER_AREA)
        m = (ph.min(2) > 215).astype(np.uint8) * 255
        _, cc, st, _ = cv2.connectedComponentsWithStats(m); big = 1 + np.argmax(st[1:, cv2.CC_STAT_AREA])
        m = np.where(cc == big, 255, 0).astype(np.uint8)
        m = cv2.dilate(cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8)), np.ones((3, 3), np.uint8))
        m = cv2.GaussianBlur(m, (5, 5), 0).astype(np.float32)[..., None] / 255.0
        w = warp.astype(np.float32) * k * (np.array(rgb[::-1], np.float32) / 255.0)
        yy, xx = np.mgrid[0:H, 0:W]; x0, x1, y0, y1 = q[:, 0].min(), q[:, 0].max(), q[:, 1].min(), q[:, 1].max()
        w = np.clip(w + np.clip(1 - ((xx - x0) / (x1 - x0 + 1) + (yy - y0) / (y1 - y0 + 1)) / 2, 0, 1)[..., None] * 8, 0, 255)
        out = (w * m + ph.astype(np.float32) * (1 - m)).astype(np.uint8)
        cv2.imwrite(os.path.join(ROOT, 'img', f'situ-{n}.jpg'), out, [cv2.IMWRITE_JPEG_QUALITY, 82, cv2.IMWRITE_JPEG_PROGRESSIVE, 1])
        print(n, os.path.getsize(os.path.join(ROOT, 'img', f'situ-{n}.jpg')) // 1024, 'KB')

if __name__ == '__main__':
    with tempfile.TemporaryDirectory() as t:
        render(t); compose(t)
