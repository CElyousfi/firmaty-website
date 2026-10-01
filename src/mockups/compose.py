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
    "climat": (CLIMAT, 360, 830, False, True, .96, (255, 248, 236)),
    "labo": (LABO, 780, 500, True, False, .985, (248, 250, 255)),
}
CSS = os.path.join(ROOT, 'site', 'site.css')

def page(inner, w, h, chrome, mobile):
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
