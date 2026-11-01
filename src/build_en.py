#!/usr/bin/env python3
"""JUNIN website: English pages (/en/).
Runs the Korean build first (build.py), then writes OUT/en/*.html, sitemap.xml and robots.txt.
Same design and data as the Korean site; only copy changes."""
import datetime, os, sys, urllib.parse
sys.path.insert(0, os.path.dirname(__file__))
import build as ko
from build import esc, stats, prof_stair, IBAR, FBAR, WEIGHT, rows4, ANNUAL, PROJECTS, MIX, INK
from bars import bar_svg

SITE = ko.SITE
OUT = os.path.join(ko.OUT, 'en')
os.makedirs(OUT, exist_ok=True)
A = '../assets'

# ---- draft values to confirm with the company ----
CO = 'JUNIN INDUSTRY Co., Ltd.'           # 회사 영문 표기 (2026.11 대표 확정)
CEOS = 'Lee Deok-geun and Koo Hyung-geun'   # 공동대표이사 영문 표기 (초안)
TEL, FAX, EMAIL = '+82-31-351-3142', '+82-31-351-3149', ko.EMAIL
TEL_HREF = '+82313513142'
ADDR_HQ = '16, Maebawi-ro 366beon-gil, Jangan-myeon, Manse-gu, Hwaseong-si, Gyeonggi-do, Republic of Korea'
ADDR_LAB = '#1512, BIFC2, 128 Namdongcheon-ro, Nam-gu, Busan, Republic of Korea'

NAV = [
    ('company.html', 'Company'),
    ('products.html', 'Products'),
    ('facility.html', 'Facility'),
    ('projects.html', 'Track Record'),
]

def url(page):
    return '' if page == 'index' else page + '.html'

def head(title, desc, page):
    full = f'{title} | {CO}' if page != 'index' else f'{CO} | Steel Grating Manufacturer, Korea'
    u = url(page)
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(full)}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<meta name="description" content="{esc(desc)}">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(full)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="{SITE}/assets/img/hero-line.jpg">
<meta property="og:url" content="{SITE}/en/{u}">
<meta property="og:site_name" content="{CO}">
<meta property="og:locale" content="en_US">
<meta property="og:locale:alternate" content="ko_KR">
<link rel="canonical" href="{SITE}/en/{u}">
<link rel="alternate" hreflang="ko" href="{SITE}/{u}">
<link rel="alternate" hreflang="en" href="{SITE}/en/{u}">
<link rel="alternate" hreflang="x-default" href="{SITE}/{u}">
<link rel="icon" type="image/png" sizes="32x32" href="{A}/img/mark-32.png">
<link rel="apple-touch-icon" href="{A}/img/mark-180.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700&family=IBM+Plex+Sans+KR:wght@400;500;700&display=swap">
<link rel="stylesheet" href="{A}/css/site.css">
</head>
<body>
'''

def header(page):
    links = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href.startswith(page + '.') else ''
        links.append(f'<a href="{href}"{cur}>{label}</a>')
    cur = ' aria-current="page"' if page == 'contact' else ''
    links.append(f'<a class="nav-cta" href="contact.html"{cur}>Request a Quote</a>')
    return f'''<a class="sr-only" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="./" aria-label="{CO} home"><img src="{A}/img/logo-en.svg" alt="{CO}" width="233" height="34"></a>
    <div class="lang" aria-label="Language"><a href="../{url(page)}" lang="ko" hreflang="ko">KO</a><a href="./{url(page)}" lang="en" hreflang="en" aria-current="true">EN</a></div>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav"><span></span><span class="sr-only">Menu</span></button>
    <nav class="nav" id="site-nav" aria-label="Main menu">
      {chr(10).join(links)}
    </nav>
  </div>
</header>
<main id="main">
'''

def cta_band():
    return f'''<section class="cta-band grating-bg">
  <div class="wrap">
    <div>
      <h2>Send us your drawings for a spec and lead-time review</h2>
      <p>We will propose bearing bar sizes that suit your span and load conditions.</p>
    </div>
    <div class="contact-quick">
      <a class="tel" href="tel:{TEL_HREF}">{TEL}</a>
      <a class="btn btn-red" href="contact.html">Request a Quote</a>
    </div>
  </div>
</section>
'''

def footer():
    nav = ''.join(f'<a href="{h}">{l}</a>' for h, l in NAV) + '<a href="contact.html">Request a Quote</a>'
    return f'''</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="foot-top">
      <img src="{A}/img/logo-en-white.svg" alt="{CO}" width="206" height="30">
      <nav class="foot-nav" aria-label="Footer menu">{nav}<a href="{A}/docs/junin-catalog-en.pdf" download>Catalog</a></nav>
    </div>
    <div class="foot-info">
      <p><span>{CO}</span><span>Co-CEOs {CEOS}</span></p>
      <p><span>Head Office &amp; Plant: {ADDR_HQ}</span></p>
      <p><span>R&amp;D Center: {ADDR_LAB}</span></p>
      <p><span>TEL <a href="tel:{TEL_HREF}">{TEL}</a></span><span>FAX {FAX}</span><span>E-mail <a href="mailto:{EMAIL}">{EMAIL}</a></span></p>
    </div>
    <p class="foot-copy">© 2026 {CO} All rights reserved.</p>
  </div>
</footer>
<script src="{A}/js/site.js"></script>
</body>
</html>
'''

def page(name, title, desc, body):
    doc = head(title, desc, name) + header(name) + body + footer()
    fn = 'index.html' if name == 'index' else f'{name}.html'
    with open(os.path.join(OUT, fn), 'w') as f:
        f.write(doc)

def sub_hero(eyebrow, h1, lead, img, btns=''):
    return f'''<section class="hero hero-sub-page">
  <div class="hero-media"><img src="{A}/img/{img}" alt="" fetchpriority="high"></div>
  <div class="wrap">
    <span class="eyebrow">{eyebrow}</span>
    <h1>{h1}</h1>
    <p class="lead">{lead}</p>
    {btns}
  </div>
</section>
'''

def stats_en(items, light=False):
    return stats(items, light).replace('aria-label="주요 수치"', 'aria-label="Key figures"')

# ---------- translations of data ----------
FIELD = {'반도체': 'Semiconductor', '석유화학': 'Petrochemical', '공항': 'Airport', '해외 플랜트': 'Overseas Plant',
         '데이터센터': 'Data Center', '발전': 'Power', '이차전지 소재': 'Battery Materials', '자동차': 'Automotive'}
CLIENT = {'삼성물산': 'Samsung C&T', 'S-OIL': 'S-OIL', 'GS칼텍스': 'GS Caltex', '현대케미칼': 'Hyundai Chemical',
          '인천공항공사': 'Incheon International Airport Corp.', '삼성엔지니어링': 'Samsung Engineering (now Samsung E&A)',
          'DL이앤씨': 'DL E&C', '한국남동발전': 'Korea South-East Power (KOEN)', 'LS MnM': 'LS MnM',
          '롯데GS케미칼': 'Lotte GS Chemical', 'GS건설': 'GS E&C', '현대모비스': 'Hyundai Mobis'}
PROJ = {
    '삼성전자 고덕·동탄 공장 신설(P3 P4 등)': 'Samsung Electronics Godeok & Dongtan fabs (P3, P4, etc.)',
    'SHAHEEN PROJECT': 'SHAHEEN Project',
    'MFC Project': 'MFC Project',
    'HPC Project': 'HPC Project',
    '4단계 T2 수하물처리시설': 'Phase 4, Terminal 2 Baggage Handling System',
    'PEMEX DNBR MODULE(멕시코)': 'PEMEX DNBR Module (Mexico)',
    '김포 데이터센터': 'Gimpo Data Center',
    '영흥화력 발전소(옥내저탄장 등)': 'Yeongheung Thermal Power Plant (indoor coal yard, etc.)',
    'EVBM 온산 PROJECT': 'EVBM Onsan Project',
    'G1-C3 PJT': 'G1-C3 Project',
    '안양 EPOCH 데이터센터': 'Anyang EPOCH Data Center',
    '현대자동차 울산 전기차 공장': 'Hyundai Motor Ulsan EV Plant',
}
def tr(d, k):
    if k not in d:
        raise KeyError(f'missing English for: {k}')
    return d[k]

def period(s):
    return s.replace('~', '–')

def proj_cards(rows):
    out = []
    for r in rows:
        out.append(f'''<article class="proj">
  <span class="field">{esc(tr(FIELD, r["분야"]))}</span>
  <h3>{esc(tr(PROJ, r["프로젝트"]))}</h3>
  <span class="client">{esc(tr(CLIENT, r["발주처"]))}</span>
  <div class="meta"><span>{esc(period(r["시기"]))}</span><span class="num">approx. {int(r["납품량(톤)"]):,}<small>t</small></span></div>
</article>''')
    return '\n'.join(out)

def anatomy_svg():
    x0, y0, L, W = 70, 50, 500, 240
    s = [f'<rect x="{x0}" y="{y0}" width="{L}" height="{W}" fill="#f3f4f4"/>']
    for i in range(9):
        y = y0 + i * 30
        s.append(f'<rect x="{x0}" y="{y-2}" width="{L}" height="4" fill="{INK}"/>')
    for j in range(1, 5):
        x = x0 + j * 100
        s.append(f'<rect x="{x-1.5}" y="{y0-2}" width="3" height="{W+4}" fill="#767E83"/>')
    s.append(f'<rect x="{x0-4}" y="{y0-2}" width="6" height="{W+4}" fill="#E60013"/>')
    s.append(f'<rect x="{x0+L-2}" y="{y0-2}" width="6" height="{W+4}" fill="#E60013"/>')
    t = 'font-family="IBM Plex Sans KR, sans-serif" font-size="15" fill="#231916"'
    tn = 'font-family="Barlow Condensed, sans-serif" font-size="16" font-weight="600" fill="#767E83"'
    s.append(f'<path d="M{x0+L+22} {y0} v30 M{x0+L+16} {y0} h12 M{x0+L+16} {y0+30} h12" stroke="#767E83" stroke-width="1.5" fill="none"/>')
    s.append(f'<text x="{x0+L+34}" y="{y0+21}" {tn}>30</text>')
    s.append(f'<path d="M{x0+100} {y0-22} h100 M{x0+100} {y0-28} v12 M{x0+200} {y0-28} v12" stroke="#767E83" stroke-width="1.5" fill="none"/>')
    s.append(f'<text x="{x0+140}" y="{y0-30}" {tn}>100</text>')
    s.append(f'<path d="M{x0+430} {y0+90} L{x0+470} {y0+W+40}" stroke="#231916" stroke-width="1" fill="none"/>')
    s.append(f'<text x="{x0+400}" y="{y0+W+58}" {t} font-weight="700">Bearing bar</text>')
    s.append(f'<path d="M{x0+300} {y0+150} L{x0+260} {y0+W+40}" stroke="#231916" stroke-width="1" fill="none"/>')
    s.append(f'<text x="{x0+215}" y="{y0+W+58}" {t} font-weight="700">Cross bar</text>')
    s.append(f'<path d="M{x0} {y0+W} L{x0-20} {y0+W+40}" stroke="#231916" stroke-width="1" fill="none"/>')
    s.append(f'<text x="{x0-60}" y="{y0+W+58}" {t} font-weight="700" fill="#E60013">End bar</text>')
    s.append(f'<text x="{x0+L/2}" y="{y0+W+90}" {t} text-anchor="middle" fill="#767E83">Length = bearing bar direction  ·  Width = cross bar direction</text>')
    return f'<svg viewBox="0 0 680 400" role="img" aria-label="Grating plan view: bearing bar pitch 30 mm, cross bar spacing 100 mm, end bars at both ends">{"".join(s)}</svg>'

def annual_chart():
    svg = ko.annual_chart()
    svg = svg.replace('<title id="annual-title">연도별 납품량</title>', '<title id="annual-title">Annual delivery volume</title>')
    i, j = svg.index('<desc id="annual-desc">'), svg.index('</desc>')
    svg = svg[:i] + '<desc id="annual-desc">' + ', '.join(f'{y}: {v:,.0f} t' for y, v in ANNUAL) + svg[j:]
    svg = svg.replace('>단위: 톤<', '>Unit: metric tons<').replace('>3,000톤<', '>3,000 t<')
    assert not any('가' <= ch <= '힣' for ch in svg), 'Korean left in chart'
    return svg

# =====================================================================
# Home
# =====================================================================
home = f'''<section class="hero">
  <div class="hero-media"><img src="{A}/img/hero-line.jpg" alt="Automatic projection welding line for steel grating at the JUNIN plant" fetchpriority="high"></div>
  <div class="wrap">
    <span class="eyebrow">Steel Grating Manufacturer · Korea</span>
    <h1>Steel grating for Korea's industrial plants, made by <em>JUNIN</em></h1>
    <p class="lead">From petrochemical plants and power stations to semiconductor fabs and data centers, we have delivered 37,300 tons of steel grating over the past ten years.</p>
    <div class="btns">
      <a class="btn btn-red" href="contact.html">Request a Quote</a>
      <a class="btn btn-line" href="products.html">View Products</a>
    </div>
  </div>
</section>
''' + stats_en([
    ('37,300<small>t</small>', 'Delivered over 10 years'),
    ('6,205', 'Delivery orders'),
    ('350<small>+</small>', 'Customers'),
    ('<span class="pre">Up to</span>1,000<small>t/mo</small>', 'Grating production capacity'),
]) + f'''
<section class="section">
  <div class="wrap split">
    <div class="split-text" style="display:grid;gap:22px">
      <span class="eyebrow">About</span>
      <h2 style="font-size:clamp(26px,3.2vw,38px)">From rolled bar to shipment,<br>one site, one continuous flow</h2>
      <div class="prose">
        <p>Founded in 2016, JUNIN has focused on one product: steel grating. At our plant in Hwaseong, Gyeonggi-do, we control every step in house: automatic projection welding, fabrication, hot-dip galvanizing, three inspections and packing.</p>
        <p>Every panel is made to the customer's drawings, with dimensional tolerances per NAAMM (National Association of Architectural Metal Manufacturers). Our quality and environmental management systems are certified to ISO 9001 and ISO 14001.</p>
      </div>
      <div><a class="link-more" href="company.html">About the company</a></div>
    </div>
    <div class="split-media"><img src="{A}/img/02-press-welder-2-front.jpg" alt="Front of automatic projection welding machine No. 2" loading="lazy"></div>
  </div>
</section>

<section class="section section-paper">
  <div class="wrap">
    <div class="sec-head sec-head-row">
      <div><span class="eyebrow">Products</span><h2>Grating made for your site</h2><p>Bearing bar profile, pitch and end finish are selected to match your design conditions.</p></div>
      <div style="display:flex;gap:20px;flex-wrap:wrap"><a class="link-more" href="{A}/docs/junin-catalog-en.pdf" download>Download catalog</a><a class="link-more" href="products.html">Full specifications</a></div>
    </div>
    <div class="cards">
      <a class="card" href="products.html#types">
        <div class="profile">{bar_svg("i")}</div>
        <span class="code">I-BAR · FLAT BAR</span>
        <h3>Steel Grating</h3>
        <p>Standard grating with cross bars projection-welded to I-bar or flat bearing bars. Pitch 30, 35.3 and 40 mm.</p>
        <span class="link-more">View specs</span>
      </a>
      <a class="card" href="products.html#types">
        <div class="profile">{bar_svg("si")}</div>
        <span class="code">SERRATED</span>
        <h3>Serrated Grating</h3>
        <p>Serrations on the top edge of the bearing bars improve slip resistance. Available in serrated I-bar and serrated flat bar.</p>
        <span class="link-more">View specs</span>
      </a>
      <a class="card" href="products.html#stair">
        <div class="profile">{prof_stair()}</div>
        <span class="code">STAIR TREAD</span>
        <h3>Stair Treads</h3>
        <p>Welded or bolted type, 215, 245 and 275 mm wide, in lengths from 500 to 1,200 mm.</p>
        <span class="link-more">View specs</span>
      </a>
    </div>
  </div>
</section>

<section class="section section-dark grating-bg">
  <div class="wrap">
    <div class="sec-head sec-head-row">
      <div><span class="eyebrow">Process</span><h2>A production line built on three automatic projection welding machines</h2><p>Three 2,230 kVA automatic projection welding machines run in parallel, so we can handle large project volumes and tight delivery dates at the same time.</p></div>
      <a class="link-more" href="facility.html">Facility &amp; capacity</a>
    </div>
    <ol class="flow">
      <li><figure><img src="{A}/img/v-01-press-welding.jpg" alt="Automatic projection welding" loading="lazy"></figure><span class="step">STEP 1</span><h3>Projection Welding</h3><p>Bearing bars and cross bars are joined into one piece by electric resistance projection welding.</p></li>
      <li><figure><img src="{A}/img/v-02-high-speed-cutting.jpg" alt="High-speed cutting" loading="lazy"></figure><span class="step">STEP 2</span><h3>High-speed Cutting</h3><p>Panels are cut to the dimensions on the drawing.</p></li>
      <li><figure><img src="{A}/img/v-03-shape-cutting.jpg" alt="Shape cutting" loading="lazy"></figure><span class="step">STEP 3</span><h3>Shape Cutting</h3><p>Cut-outs are made for pipes and columns.</p></li>
      <li><figure><img src="{A}/img/v-04-welding.jpg" alt="Welding" loading="lazy"></figure><span class="step">STEP 4</span><h3>Welding</h3><p>End bars and cut-out banding are welded on.</p></li>
      <li><figure><img src="{A}/img/v-05-grinding.jpg" alt="Grinding" loading="lazy"></figure><span class="step">STEP 5</span><h3>Grinding &amp; Inspection</h3><p>Welds are ground and checked against NAAMM tolerances.</p></li>
      <li><figure><img src="{A}/img/v-06-galvanized-product.jpg" alt="Hot-dip galvanized grating" loading="lazy"></figure><span class="step">STEP 6</span><h3>Galvanizing &amp; Shipment</h3><p>Hot-dip galvanized, inspected and shipped.</p></li>
    </ol>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head sec-head-row">
      <div><span class="eyebrow">Projects</span><h2>Where JUNIN grating is installed</h2><p>Supplied through steel structure fabricators to semiconductor, petrochemical, airport and overseas plant projects.</p></div>
      <a class="link-more" href="projects.html">10-year track record</a>
    </div>
    <div class="proj-grid">
{proj_cards(PROJECTS[:6])}
    </div>
  </div>
</section>
''' + cta_band()
page('index', 'Home', f'{CO}, a steel grating manufacturer in Korea. Three automatic projection welding machines, capacity up to 1,000 t per month, 37,300 t delivered over 10 years.', home)

# =====================================================================
# Company
# =====================================================================
HISTORY = [
    ('2016.04', f'{CO} founded (Co-CEOs {CEOS})'),
    ('2016.05', 'ISO 9001 and ISO 14001 certified'),
    ('2016.09', 'Certified as a venture company'),
    ('2016.10', 'Acquired and commissioned automatic grating projection welding equipment'),
    ('2017.01', 'Corporate R&D center established'),
    ('2017.03', 'Registered on KONEPS, the Korean public procurement system'),
    ('2017.04', 'Design registration for drainage grating'),
    ('2018.10', 'Began exports to Vietnam (DOOSAN VINA)'),
    ('2019.06', 'Certified as an innovative SME in management (MAIN-BIZ)'),
    ('2025.05', 'ISO 9001 and ISO 14001 renewed'),
    ('2026.08', 'R&D center relocated to BIFC2, Busan'),
]
hist = ''.join(f'<li><span class="num">{d}</span><span>{esc(t)}</span></li>' for d, t in HISTORY)

def maplinks(addr_ko):
    q = urllib.parse.quote(addr_ko)
    return f'<div class="maps"><a href="https://www.google.com/maps/search/?api=1&amp;query={q}" target="_blank" rel="noopener">Google Maps</a><a href="https://map.naver.com/p/search/{q}" target="_blank" rel="noopener">Naver Map</a></div>'

company = sub_hero('Company', 'A steel grating specialist<br>built on skill and trust', 'Since 2016 we have made one thing: steel grating. At our Hwaseong plant we run every step ourselves, from projection welding to shipment.', '13-welding-shop.jpg') + f'''
<nav class="subnav" aria-label="Company sections"><div class="wrap">
  <a href="#greeting">Message</a><a href="#vision">Vision</a><a href="#history">History</a><a href="#cert">Certification</a><a href="#location">Location</a>
</div></nav>

<section class="section" id="greeting">
  <div class="wrap split" style="align-items:start">
    <div style="display:grid;gap:18px">
      <span class="eyebrow">Message from the CEOs</span>
      <h2 style="font-size:clamp(26px,3.2vw,38px)">We put our customers' sites first</h2>
    </div>
    <div class="prose">
      <p>Thank you for visiting {CO}.</p>
      <p>Founded in 2016, JUNIN is a manufacturer dedicated to steel grating. At our head office and plant in Hwaseong, Gyeonggi-do, we manage the entire process, from receiving raw material through automatic projection welding, fabrication, hot-dip galvanizing and inspection to shipment. Over the past ten years we have delivered 37,300 tons of grating and stair treads to more than 350 customers.</p>
      <p>Our grating is in service where safety matters most: petrochemical plants, power stations, data centers and airports. Every product is made to the customer's design, with tolerances per NAAMM and quality and environmental management certified to ISO 9001 and ISO 14001.</p>
      <p>We will keep our promise of "skill and trust" and continue to put our customers' sites first.</p>
      <p style="font-weight:700;margin-top:.6em">{CEOS}, Co-CEOs, {CO}</p>
    </div>
  </div>
</section>

<section class="section section-dark grating-bg" id="vision">
  <div class="wrap">
    <div class="sec-head">
      <span class="eyebrow">Vision</span>
      <h2 class="num" style="font-size:clamp(34px,5vw,60px);font-weight:600;letter-spacing:-.01em;color:#fff">Innovative Challenger for Your Dream</h2>
      <p>We lead the market with forward thinking and acting one step ahead.</p>
    </div>
    <div class="values">
      <div><span class="en">Technology</span><h3>Technology</h3><p>A quality management system and fabrication marks let us trace every piece we make.</p></div>
      <div><span class="en">Market Intelligence</span><h3>Market Insight</h3><p>We understand what customers and sites need before they ask.</p></div>
      <div><span class="en">Customer First</span><h3>Customer First</h3><p>We think and build together with our customers.</p></div>
    </div>
  </div>
</section>

<section class="section" id="history">
  <div class="wrap split" style="align-items:start">
    <div style="display:grid;gap:18px">
      <span class="eyebrow">History</span>
      <h2 style="font-size:clamp(26px,3.2vw,38px)">History</h2>
      <p class="note" style="font-size:16px">Founded in April 2016. Grating production began that October with the start-up of our automatic projection welding equipment.</p>
    </div>
    <ol class="timeline">{hist}</ol>
  </div>
</section>

<section class="section section-paper" id="cert">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">Certification</span><h2>Certification</h2><p>We have maintained quality and environmental management certification since 2016.</p></div>
    <div class="certs">
      <div class="cert"><span class="std">ISO 9001</span><h3>Quality Management System</h3>
        <dl><dt>Scope</dt><dd>Manufacture of grating and steel structures</dd><dt>Valid until</dt><dd>May 25, 2028</dd></dl></div>
      <div class="cert"><span class="std">ISO 14001</span><h3>Environmental Management System</h3>
        <dl><dt>Scope</dt><dd>Manufacture of grating and steel structures</dd><dt>Valid until</dt><dd>May 25, 2028</dd></dl></div>
    </div>
  </div>
</section>

<section class="section" id="location">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">Location</span><h2>Location</h2></div>
    <div class="locs">
      <div class="loc"><span class="tag">Head Office · Plant</span><h3>Hwaseong Plant</h3><address>{ADDR_HQ}</address>
        <p>TEL {TEL} · FAX {FAX}</p>{maplinks(ko.ADDR_HQ)}</div>
      <div class="loc"><span class="tag">Corporate R&amp;D Center</span><h3>Busan R&amp;D Center</h3><address>{ADDR_LAB}</address>
        <p>Design and load review</p>{maplinks('부산광역시 남구 남동천로 128')}</div>
    </div>
  </div>
</section>
''' + cta_band()
page('company', 'Company', f'{CO}: message from the CEOs, vision, history, ISO 9001 and ISO 14001 certification, and location.', company)

# =====================================================================
# Products
# =====================================================================
WEIGHT_EN = [(r[0].replace('F-Bar', 'Flat bar').replace('I-Bar', 'I-bar'),) + tuple(r[1:]) for r in WEIGHT]
wrows = ''.join('<tr><th scope="row">' + r[0] + '</th>' + ''.join(f'<td class="{"muted" if v=="–" else ""}">{v}</td>' for v in r[1:]) + '</tr>' for r in WEIGHT_EN)

products = sub_hero('Products', 'Steel grating made<br>to your design conditions', 'Bearing bar profile, pitch and end finish are chosen to suit the site, and every panel is fabricated to the dimensions on your drawings.', 'v-06-galvanized-product.jpg',
    f'<div class="btns"><a class="btn btn-red" href="contact.html">Request a Quote</a><a class="btn btn-line" href="{A}/docs/junin-grating-spec-2026-10.pdf" target="_blank" rel="noopener">Spec Sheet PDF (Korean)</a></div>') + f'''
<nav class="subnav" aria-label="Product sections"><div class="wrap">
  <a href="#structure">Structure</a><a href="#types">Types</a><a href="#spec">Dimensions</a><a href="#bars">Bearing Bars</a><a href="#weight">Unit Weight</a><a href="#stair">Stair Treads</a><a href="#fixing">Fixing</a><a href="#galv">Galvanizing</a>
</div></nav>

<section class="section" id="structure">
  <div class="wrap anatomy">
    <div style="display:grid;gap:18px">
      <span class="eyebrow">Structure</span>
      <h2 style="font-size:clamp(26px,3.2vw,38px)">How steel grating is built</h2>
      <div class="prose">
        <p>Steel grating is an open-grid floor panel. Load-carrying <strong>bearing bars</strong> stand on edge at a fixed spacing (pitch), and <strong>cross bars</strong> run across them, joined into a single piece by electric resistance projection welding.</p>
        <p>It lets light, air and rainwater through and has a high strength-to-weight ratio, which makes it the standard choice for plant walkways, platforms, trench covers and stairs. The panel ends are either closed with end bars (banded type) or left open (open type).</p>
      </div>
    </div>
    <div>{anatomy_svg()}</div>
  </div>
</section>

<section class="section section-paper" id="types">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">Types</span><h2>Bearing bar profiles</h2><p>Grating is classified into four types by bearing bar profile. Each is available as banded type or open type.</p></div>
    <div class="types types-4">
      <div class="type"><div class="profile">{bar_svg("i")}</div><span class="code">I-BAR</span><h3>I-Bar Grating</h3><p>Grating whose bearing bars have an I-shaped cross section.</p></div>
      <div class="type"><div class="profile">{bar_svg("f")}</div><span class="code">FLAT BAR</span><h3>Flat Bar Grating</h3><p>Grating whose bearing bars are plain rectangular flat bars.</p></div>
      <div class="type"><div class="profile">{bar_svg("si")}</div><span class="code">SERRATED I-BAR</span><h3>Serrated I-Bar Grating</h3><p>Grating whose bearing bars combine an I-shaped section with a serrated top edge.</p></div>
      <div class="type"><div class="profile">{bar_svg("sf")}</div><span class="code">SERRATED</span><h3>Serrated Grating</h3><p>Grating whose flat bearing bars have a serrated top edge.</p></div>
    </div>
  </div>
</section>

<section class="section" id="spec">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">Specification</span><h2>Standard dimensions</h2></div>
    <div class="table-scroll"><table class="tbl">
      <tbody>
        <tr><th scope="row">Bearing bar profile</th><td>I-bar, flat bar, serrated I-bar (SI), serrated flat bar (SF)</td></tr>
        <tr><th scope="row">Bearing bar pitch</th><td class="num" style="font-size:17px">12.5 / 15 / 25 / 30 / 35.3 / 40 mm</td></tr>
        <tr><th scope="row">Cross bar spacing</th><td class="num" style="font-size:17px">100 mm</td></tr>
        <tr><th scope="row">Cross bar</th><td>Pitch 30 mm: 6×6 square bar · 35.3 mm: 8×8 square bar · 15 mm: ø6 round bar · 12.5 mm: ø5 round bar</td></tr>
        <tr><th scope="row">Max. standard width</th><td>995 mm (set by number of bearing bars and pitch)</td></tr>
        <tr><th scope="row">Length</th><td>Made to design dimensions (length = bearing bar direction, width = cross bar direction)</td></tr>
        <tr><th scope="row">End finish</th><td>Banded type (end bars) / open type (cut end)</td></tr>
        <tr><th scope="row">Material</th><td>Hot-rolled carbon steel bar, JIS G3101 SS400, SS275</td></tr>
        <tr><th scope="row">Surface finish</th><td>Hot-dip galvanizing to KS D 8308, JIS H8641, ASTM A123</td></tr>
        <tr><th scope="row">Fabrication tolerance</th><td>Per NAAMM (National Association of Architectural Metal Manufacturers)</td></tr>
      </tbody>
    </table></div>
  </div>
</section>

<section class="section section-paper" id="bars">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">Bearing Bar</span><h2>Bearing bar sizes</h2><p>I = moment of inertia, Z = section modulus (per bearing bar)</p></div>
    <div class="split" style="align-items:start">
      <div><h3 style="font-size:18px;margin-bottom:12px">I-Bar</h3><div class="table-scroll"><table class="tbl tbl-compact tbl-spec">
        <thead><tr><th>Type</th><th>Size H×W×T (mm)</th><th>I (cm⁴)</th><th>Z (cm³)</th></tr></thead>
        <tbody>{rows4(IBAR)}</tbody></table></div></div>
      <div><h3 style="font-size:18px;margin-bottom:12px">Flat Bar</h3><div class="table-scroll"><table class="tbl tbl-compact tbl-spec">
        <thead><tr><th>Type</th><th>Size H×T (mm)</th><th>I (cm⁴)</th><th>Z (cm³)</th></tr></thead>
        <tbody>{rows4(FBAR)}</tbody></table></div></div>
    </div>
    <div class="split" style="align-items:start;margin-top:48px">
      <div><h3 style="font-size:18px;margin-bottom:12px">Serrated</h3><div class="table-scroll"><table class="tbl tbl-compact tbl-spec">
        <thead><tr><th>Type</th><th>Sizes</th><th>Pitch (mm)</th><th>Cross bar</th></tr></thead>
        <tbody><tr><th scope="row">Serrated I-bar</th><td>SI-25 to SI-44 (×5×3)</td><td>30 / 15</td><td>6×6 / ø6</td></tr>
        <tr><th scope="row">Serrated flat bar</th><td>SF-25 to SF-44 (×5)</td><td>30</td><td>6×6</td></tr></tbody></table></div>
        <p class="note" style="margin-top:10px">Serrated bars have the same unit weight as unserrated bars of the same size.</p></div>

    </div>
  </div>
</section>

<section class="section" id="weight">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">Unit Weight</span><h2>Unit weight</h2><p>kg/m², after hot-dip galvanizing</p></div>
    <div class="table-scroll"><table class="tbl tbl-compact tbl-spec">
      <thead>
        <tr><th rowspan="2" style="text-align:left">Bearing bar</th><th colspan="2">Pitch 30 mm</th><th colspan="2">Pitch 35.3 mm</th><th colspan="2">Pitch 40 mm</th></tr>
        <tr><th>Banded</th><th>Open</th><th>Banded</th><th>Open</th><th>Banded</th><th>Open</th></tr>
      </thead>
      <tbody>{wrows}</tbody>
    </table></div>
    <p class="note" style="margin-top:12px">'–' means no standard unit weight data for that combination. Sizes not listed can also be made to order.</p>
  </div>
</section>

<section class="section section-paper" id="stair">
  <div class="wrap split" style="align-items:start">
    <div style="display:grid;gap:18px">
      <span class="eyebrow">Stair Tread</span>
      <h2 style="font-size:clamp(26px,3.2vw,38px)">Stair treads</h2>
      <p class="note" style="font-size:16px">End plates are attached to both ends of the grating, which is then welded or bolted to the stair stringers.</p>
      <div style="max-width:260px;margin-top:8px">{prof_stair()}</div>
    </div>
    <div class="table-scroll"><table class="tbl">
      <tbody>
        <tr><th scope="row">Connection</th><td>Welded type / bolted type</td></tr>
        <tr><th scope="row">Width (bolt hole spacing)</th><td>215 mm (120) · 245 mm (150) · 275 mm (180)</td></tr>
        <tr><th scope="row">Length</th><td>500 – 1,200 mm</td></tr>
        <tr><th scope="row">Bearing bar</th><td>F25×5, F32×5, I25×5×3, I32×5×3</td></tr>
        <tr><th scope="row">End plate</th><td>Fillet welded to every bearing bar, 3 mm minimum</td></tr>
      </tbody>
    </table></div>
  </div>
</section>

<section class="section" id="fixing">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">Fixing</span><h2>Fixing methods</h2><p>Chosen by vibration, need for removal and installation speed.</p></div>
    <div class="fix">
      <div><h3>Saddle Clip</h3><p>Bolted in place and removable.</p></div>
      <div><h3>Upper / Lower Clip</h3><p>Clamps from above and below; resists vibration.</p></div>
      <div><h3>Self-drilling Screw</h3><p>Fast installation with no pre-drilling.</p></div>
      <div><h3>Field Welding</h3><p>For areas that never need to be removed.</p></div>
    </div>
  </div>
</section>

<section class="section section-paper" id="galv">
  <div class="wrap split">
    <div style="display:grid;gap:18px">
      <span class="eyebrow">Hot-dip Galvanizing</span>
      <h2 style="font-size:clamp(26px,3.2vw,38px)">Hot-dip galvanizing</h2>
      <div class="prose">
        <p>After fabrication, the grating is dipped in molten zinc so that every surface is covered with a zinc coating. This protects it from corrosion outdoors and in humid plant environments.</p>
        <p>Galvanizing is done to KS D 8308, JIS H8641 and ASTM A123, and coating thickness and surface condition are measured before shipment.</p>
      </div>
    </div>
    <div class="split-media"><img src="{A}/img/15-sorting-after-galvanizing.jpg" alt="Sorting grating after galvanizing" loading="lazy"></div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="callout">
      <h3>Load review</h3>
      <p>Allowable load and deflection depend on span, load type (pedestrian, vehicle, concentrated load) and support conditions. Send us your layout drawings and load conditions, and our R&amp;D center will review them and propose suitable bearing bar sizes.</p>
      <div class="btns" style="margin-top:10px"><a class="btn btn-red" href="contact.html">Request a Load Review</a><a class="btn btn-line" href="{A}/docs/junin-grating-spec-2026-10.pdf" target="_blank" rel="noopener">Spec Sheet PDF (Korean)</a><a class="btn btn-line" href="{A}/docs/junin-catalog-en.pdf" download>Catalog</a></div>
    </div>
    <p class="note" style="margin-top:14px">Specifications may change without notice for product improvement.</p>
  </div>
</section>
''' + cta_band()
page('products', 'Products', 'Steel grating structure, bearing bar profiles (I-bar, flat bar, serrated I-bar, serrated), standard dimensions, unit weight table, stair treads and fixing methods.', products)

# =====================================================================
# Facility
# =====================================================================
EQUIP = [
 ('Grating', 'Automatic projection welding machine', '2,230 kVA, 2-bar (two cross bars welded at once); Nisseki Eng. (Japan) ×1, Taeyang Industrial ×2', '3'),
 ('Grating', 'High-speed cutter', '30 kW × 2P', '3'),
 ('Grating', 'Disc cutter', '3.7 kW × 4P', '3'),
 ('Grating', 'Saw blade grinder', 'OD 609 mm × 10 mm, made in Germany', '2'),
 ('Grating', 'CO₂ / arc welder', '500 A, 20–25 kVA', '15'),
 ('Machining', 'Lathe, milling, radial drill, drill press, surface grinder', 'Hwacheon and others', '11'),
 ('Handling', 'Overhead crane', '3 t / 5 t', '4'),
 ('Handling', 'Hoist', '1 t', '8'),
 ('Handling', 'Forklift', '3 t', '2'),
 ('Measuring &amp; testing', 'Surface plates, height and cylinder gauges, micrometers, coating thickness gauges, etc.', 'Mostly made in Japan', '31'),
]
eq = ''.join(f'<tr><td class="muted">{a}</td><th scope="row">{b}</th><td>{c}</td><td class="r num" style="font-size:18px">{d}</td></tr>' for a, b, c, d in EQUIP)
STEPS = [
 ('Raw Material', 'SS400 and SS275 rolled bars are sourced from Korean rolling mills.', False),
 ('Projection Welding', 'Bearing bars and cross bars are joined by electric resistance projection welding.', False),
 ('Fabrication', 'Panels are cut to drawing dimensions; end bars and cut-out banding are welded.', False),
 ('Fabrication Inspection', 'Dimensions and welds are checked against NAAMM tolerances.', True),
 ('Galvanizing', 'Hot-dip galvanized to KS D 8308, JIS H8641 and ASTM A123.', False),
 ('Coating Inspection', 'Coating thickness and surface condition are measured.', True),
 ('Final Inspection', 'Quantity, fabrication marks and final dimensions are verified.', True),
 ('Packing', 'Bundled and marked in installation sequence.', False),
 ('Delivery', 'Shipped to site on the scheduled delivery date.', False),
 ('Installation', 'Installed on site with fixing clips and similar fasteners.', False),
]
steps = ''.join(f'<li class="{"qc" if q else ""}"><span class="n">{i:02d}</span><h3>{t}</h3><p>{d}</p></li>' for i, (t, d, q) in enumerate(STEPS, 1))
TEAM = [('Projection Welding', '5', 'Operates the automatic projection welding machines; 31 years of experience on average'),
        ('Fabrication', '11', 'Cutting, welding, machining'),
        ('Packing', '3', 'Packing and shipping'),
        ('Quality Control', '3', 'Fabrication, coating and final inspection'),
        ('Production Management', '2', 'Scheduling and delivery management'),
        ('R&amp;D Center', '4', 'Design and load review')]
team = ''.join(f'<tr><th scope="row">{a}</th><td class="r num" style="font-size:18px">{b}</td><td>{c}</td></tr>' for a, b, c in TEAM)
CHAP = [(0, 'Projection welding', 'v-01-press-welding.jpg'), (5, 'High-speed cutting', 'v-02-high-speed-cutting.jpg'), (10, 'Shape cutting', 'v-03-shape-cutting.jpg'), (15, 'Welding', 'v-04-welding.jpg'), (20, 'Grinding', 'v-05-grinding.jpg'), (25, 'Galvanized product', 'v-06-galvanized-product.jpg')]
chap = ''.join(f'<li><button type="button" data-seek="{t}"><img src="{A}/img/{img}" alt="" loading="lazy"><span><span class="t">0:{t:02d}</span> {lbl}</span></button></li>' for t, lbl, img in CHAP)

facility = sub_hero('Facility', 'Three automatic projection welding machines,<br>up to 1,000 tons a month', 'Rolled bar in, finished grating out: projection welding, fabrication, hot-dip galvanizing, three inspections and packing, all in one flow on a site of approx. 29,750 m².', '01-press-welder-line-front.jpg',
    '<div class="btns"><a class="btn btn-red" href="contact.html">Request a Quote</a><a class="btn btn-line" href="products.html#spec">Product specs</a></div>') + stats_en([
    ('3', '2,230 kVA automatic projection welding machines'),
    ('<span class="pre">Up to</span>1,000<small>t/mo</small>', 'Grating production capacity'),
    ('29,750<small>m²</small>', 'Site area, approx. (9,000 pyeong)'),
    ('31<small>yrs</small>', 'Average experience of projection welding crew'),
]) + f'''
<nav class="subnav" aria-label="Facility sections"><div class="wrap">
  <a href="#equipment">Equipment</a><a href="#video">Process Film</a><a href="#process">Process</a><a href="#quality">Quality</a><a href="#people">People</a>
</div></nav>

<section class="section" id="equipment">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">Equipment</span><h2>Main equipment</h2>
      <p>Grating quality is decided at the projection welding machine. We run three 2,230 kVA automatic projection welding machines from Nisseki (Japan) and Taeyang Industrial in parallel, so large project volumes and tight delivery dates can be handled together.</p></div>
    <div class="photos" style="margin-bottom:40px">
      <figure><img src="{A}/img/02-press-welder-2-front.jpg" alt="Front of automatic projection welding machine No. 2" loading="lazy"><figcaption>Projection welding machine No. 2</figcaption></figure>
      <figure><img src="{A}/img/04-nipping-machine.jpg" alt="Nipping machine" loading="lazy"><figcaption>Nipping machine</figcaption></figure>
      <figure><img src="{A}/img/05-high-speed-cutter.jpg" alt="High-speed cutter" loading="lazy"><figcaption>High-speed cutter</figcaption></figure>
      <figure><img src="{A}/img/06-high-speed-cutter-2.jpg" alt="Cutting a panel on the high-speed cutter" loading="lazy"><figcaption>High-speed cutting</figcaption></figure>
    </div>
    <div class="table-scroll"><table class="tbl tbl-wide">
      <thead><tr><th>Category</th><th>Equipment</th><th>Specification</th><th class="r">Qty</th></tr></thead>
      <tbody>{eq}</tbody>
    </table></div>
  </div>
</section>

<section class="section section-dark grating-bg" id="video">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">Process Film</span><h2>Grating production in 30 seconds</h2><p>From projection welding to the galvanized product, filmed in our plant. Click a scene below to jump to it.</p></div>
    <div class="video-frame"><video id="process-video" controls playsinline muted preload="metadata" poster="{A}/img/v-01-press-welding.jpg"><source src="{A}/video/grating-process.mp4" type="video/mp4"></video></div>
    <ol class="chapters">{chap}</ol>
  </div>
</section>

<section class="section" id="process">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">10 Steps</span><h2>Ten-step production process</h2><p>Every product is made to the customer's drawings and inspected three times before shipment. <span style="color:var(--red);font-weight:700">Red numbers</span> mark the inspection steps.</p></div>
    <ol class="steps">{steps}</ol>
    <div class="photos" style="margin-top:40px">
      <figure><img src="{A}/img/07-hole-shape-cutting.jpg" alt="Cutting an opening" loading="lazy"><figcaption>Cut-out shaping</figcaption></figure>
      <figure><img src="{A}/img/08-fit-up.jpg" alt="Fit-up work" loading="lazy"><figcaption>Fit-up</figcaption></figure>
      <figure><img src="{A}/img/11-grinding.jpg" alt="Grinding work" loading="lazy"><figcaption>Grinding</figcaption></figure>
      <figure><img src="{A}/img/16-bundle-packing.jpg" alt="Grating bundles ready for shipment" loading="lazy"><figcaption>Packed, ready to ship</figcaption></figure>
    </div>
  </div>
</section>

<section class="section section-paper" id="quality">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">Quality</span><h2>Quality control</h2></div>
    <dl class="facts">
      <div><dt>Tolerances</dt><dd>Per NAAMM (National Association of Architectural Metal Manufacturers).</dd></div>
      <div><dt>Three inspections</dt><dd>Fabrication, coating and final inspections are carried out by the Quality Control team with 31 measuring and testing instruments.</dd></div>
      <div><dt>Certification</dt><dd>ISO 9001 (quality) and ISO 14001 (environment), scope "Manufacture of grating and steel structures", valid until May 25, 2028.</dd></div>
      <div><dt>Traceability</dt><dd>Every piece carries a fabrication mark, tracked by work order number from drawing to shipment.</dd></div>
    </dl>
  </div>
</section>

<section class="section" id="people">
  <div class="wrap split" style="align-items:start">
    <div style="display:grid;gap:20px">
      <span class="eyebrow">People</span>
      <h2 style="font-size:clamp(26px,3.2vw,38px)">Our projection welding crew averages<br><span class="num" style="color:var(--red);font-size:1.25em">31</span> years of experience</h2>
      <p class="prose">However good the machine, it takes people to read the variations in rolled bar and welding current. Our projection welding team is built around operators who have made nothing but grating for over 30 years.</p>
      <img src="{A}/img/14-welding-shop-2.jpg" alt="Work in the welding shop" loading="lazy" style="width:100%;aspect-ratio:4/3;object-fit:cover">
    </div>
    <div class="table-scroll"><table class="tbl">
      <thead><tr><th>Team</th><th class="r">Staff</th><th>Role</th></tr></thead>
      <tbody>{team}</tbody>
    </table></div>
  </div>
</section>
''' + cta_band()
page('facility', 'Facility & Capacity', 'Three automatic projection welding machines with capacity up to 1,000 t per month. Main equipment, ten-step process, quality control, and a projection welding crew averaging 31 years of experience.', facility)

# =====================================================================
# Track record
# =====================================================================
MIXNAME = {'I-Bar': 'I-bar', '톱니 I-Bar': 'Serrated I-bar', '톱니 Flat Bar': 'Serrated flat bar', 'Flat Bar': 'Flat bar'}
mix_max = max(float(r['납품량(톤)']) for r in MIX)
mix = ''.join(f'''<div class="row"><span>{esc("Other" if r["베어링 바 형식"].startswith("Dense") else tr(MIXNAME, r["베어링 바 형식"]))}</span><div class="track"><div class="fill" style="width:{float(r["납품량(톤)"])/mix_max*100:.1f}%"></div></div><span class="val">{float(r["비중(%)"]):.0f}<small>%</small></span></div>''' for r in MIX)
CLIENTS = ['Daewoo ST', 'Geumseong E&C', 'Hanmaek Heavy Industries', 'POSCO Plantec', 'Sebang Tech', 'Seungyoung', 'Shinan', 'Yakdong Industrial', 'Younghwa Engineering', 'Youngshin']
clients = ''.join(f'<li>{esc(c)}</li>' for c in CLIENTS)
ptable = ''.join(f'<tr><td><span style="color:var(--red);font-weight:700;font-size:14px">{esc(tr(FIELD, r["분야"]))}</span></td><th scope="row">{esc(tr(PROJ, r["프로젝트"]))}</th><td>{esc(tr(CLIENT, r["발주처"]))}</td><td class="num" style="font-size:17px">{esc(period(r["시기"]))}</td><td class="r num" style="font-size:18px">approx. {int(r["납품량(톤)"]):,}</td></tr>' for r in PROJECTS)

projects = sub_hero('Track Record', '37,300 tons in ten years, chosen by more than 350 customers', 'From April 2016 to early November 2026 we delivered 6,205 orders. Floors and walkways at petrochemical plants, semiconductor fabs, power stations, data centers and airports are built with JUNIN grating.', '17-bundle-packing-2.jpg',
    '<div class="btns"><a class="btn btn-red" href="contact.html">Request a Quote</a></div>') + stats_en([
    ('37,300<small>t</small>', 'Delivered over 10 years'),
    ('6,205', 'Delivery orders'),
    ('350<small>+</small>', 'Customers'),
    ('4,736<small>t</small>', 'Delivered in 2020'),
]) + f'''
<section class="section">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">Annual Delivery</span><h2>Over 3,000 tons delivered every year since 2018</h2>
      <p>With capacity of up to 1,000 tons a month, we have headroom to meet delivery dates even in years when large projects overlap.</p></div>
    <div class="chart-box">
      <div class="chart-scroll">{annual_chart()}</div>
      <p class="note">By delivery date. 2016 covers April onward (after founding); 2026 covers deliveries through early November (grey bars). Ten-year total approx. 37,300 t.</p>
    </div>
  </div>
</section>

<section class="section section-paper">
  <div class="wrap split" style="align-items:start">
    <div style="display:grid;gap:18px">
      <span class="eyebrow">Product Mix</span>
      <h2 style="font-size:clamp(26px,3.2vw,38px)">What we deliver</h2>
      <p class="prose">Over the same period, 95% of volume (approx. 35,400 t) was grating and 5% (approx. 1,950 t) was stair treads. By bearing bar type, I-bar and serrated I-bar account for 70%.</p>
    </div>
    <div class="chart-box">
      <span class="chart-title">Share of deliveries by bearing bar type</span>
      <div class="bars-h">{mix}</div>
      <p class="note">April 2016 to early November 2026, by material specification</p>
    </div>
  </div>
</section>

<section class="section" id="key-projects">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">Key Projects</span><h2>Key projects by sector</h2><p>JUNIN grating was installed at the sites below, supplied through steel structure fabricators. Projects with 200 t or more delivered.</p></div>
    <div class="table-scroll"><table class="tbl tbl-wide">
      <thead><tr><th>Sector</th><th>Project</th><th>Owner / EPC</th><th>Period</th><th class="r">Delivered (t)</th></tr></thead>
      <tbody>{ptable}</tbody>
    </table></div>
    <div class="callout" style="margin-top:32px">
      <h3>Overseas projects</h3>
      <p>We began exporting to Vietnam (DOOSAN VINA) in 2018, and have supplied a PEMEX plant in Mexico through a Korean EPC contractor.</p>
    </div>
  </div>
</section>

<section class="section section-paper">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">Partners</span><h2>Main customers</h2><p>Steel structure and plant companies we have worked with over the past ten years (alphabetical).</p></div>
    <ul class="clients">{clients}</ul>
  </div>
</section>
''' + cta_band()
page('projects', 'Track Record', '37,300 t and 6,205 orders delivered over ten years since 2016. Annual delivery volume, key projects by sector and main customers.', projects)

# =====================================================================
# Contact
# =====================================================================
contact = f'''<section class="section-tight section-paper">
  <div class="wrap" style="display:grid;gap:14px">
    <span class="eyebrow">Contact</span>
    <h1 style="font-size:clamp(30px,4vw,46px)">Request a Quote</h1>
    <p class="note" style="font-size:17px;max-width:40em">Tell us the project, specification and quantity, and our team will review it and get back to you. If you have drawings, please send them by e-mail as well. We reply in English or Korean.</p>
  </div>
</section>
<section class="section">
  <div class="wrap contact-grid">
    <form class="form" id="quote-form" data-mailto="{EMAIL}" data-endpoint="" novalidate>
      <div class="field"><span class="lbl">Inquiry type<span class="req">*</span></span>
        <div class="chips" role="radiogroup" aria-label="Inquiry type">
          <label><input type="radio" name="type" id="type-quote" value="Quotation" checked><span>Quotation</span></label>
          <label><input type="radio" name="type" id="type-spec" value="Spec / load review"><span>Spec / load review</span></label>
          <label><input type="radio" name="type" id="type-etc" value="Other"><span>Other</span></label>
        </div>
      </div>
      <div class="row2">
        <div class="field"><label for="f-company">Company<span class="req">*</span></label><input id="f-company" name="company" required autocomplete="organization"></div>
        <div class="field"><label for="f-name">Contact name<span class="req">*</span></label><input id="f-name" name="name" required autocomplete="name"></div>
      </div>
      <div class="row2">
        <div class="field"><label for="f-email">E-mail<span class="req">*</span></label><input id="f-email" name="email" type="email" required autocomplete="email"></div>
        <div class="field"><label for="f-phone">Phone</label><input id="f-phone" name="phone" type="tel" autocomplete="tel" placeholder="+00 0000 0000"></div>
      </div>
      <div class="row2">
        <div class="field"><label for="f-country">Country</label><input id="f-country" name="country" autocomplete="country-name"></div>
        <div class="field"><label for="f-project">Project name</label><input id="f-project" name="project" placeholder="e.g. Refinery expansion, Phase 2"></div>
      </div>
      <div class="row2">
        <div class="field"><label for="f-spec">Specification / quantity</label><input id="f-spec" name="spec" placeholder="e.g. I-32, pitch 30, approx. 40 t"></div>
        <div class="field"><label for="f-due">Required delivery date</label><input id="f-due" name="due" type="date"></div>
      </div>
      <div class="field"><label for="f-message">Message<span class="req">*</span></label><textarea id="f-message" name="message" required placeholder="Span, load conditions, end finish (banded / open), stair treads, delivery terms (Incoterms, destination port), etc."></textarea>
        <span class="hint">Please send drawing files to {EMAIL}.</span></div>
      <label class="agree"><input type="checkbox" id="f-agree" name="agree" required>
        <span>I agree to the collection and use of my personal information. (Required)
          <details><summary>Details</summary>Data collected: company, contact name, phone, e-mail · Purpose: responding to quotations and inquiries · Retention: one year after the inquiry is handled</details>
        </span></label>
      <div><button class="btn btn-red" type="submit">Send Inquiry</button></div>
      <div class="form-status" id="form-status" role="status" hidden></div>
    </form>
    <aside style="display:grid;gap:36px">
      <div><h2 style="font-size:20px;margin-bottom:14px">Contact</h2>
        <dl class="info-list">
          <div><dt>Phone</dt><dd><a class="big" href="tel:{TEL_HREF}">{TEL}</a></dd></div>
          <div><dt>Fax</dt><dd class="big">{FAX}</dd></div>
          <div><dt>E-mail</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd></div>
          <div><dt>Address</dt><dd style="font-weight:500">{ADDR_HQ}</dd></div>
        </dl></div>
      <div><h2 style="font-size:20px;margin-bottom:14px">Downloads</h2>
        <a class="doc-card" href="{A}/docs/junin-grating-spec-2026-10.pdf" target="_blank" rel="noopener"><span class="ext">PDF</span><div><strong>Steel Grating Spec Sheet (Korean)</strong><span>Dimensions, bearing bars, unit weight, stair treads · Oct 2026</span></div></a>
        <a class="doc-card" style="margin-top:12px" href="{A}/docs/junin-catalog-en.pdf" download><span class="ext">PDF</span><div><strong>Steel Grating Data Book (English)</strong><span>Structure, specifications, tolerances, galvanizing · 16 pages · 3.3 MB</span></div></a></div>
    </aside>
  </div>
</section>
'''
page('contact', 'Request a Quote', f'Request a steel grating quotation from {CO}. TEL {TEL}, FAX {FAX}, {EMAIL}', contact)

# ---- sanity: no Korean text left in English pages (except Korean map queries / alt-free URLs) ----
for fn in os.listdir(OUT):
    t = open(os.path.join(OUT, fn)).read()
    import re
    t2 = re.sub(r'href="[^"]*"', '', t)
    left = sorted(set(re.findall(r'[가-힣]+', t2)))
    assert not left, f'{fn}: Korean left: {left}'

# ---- sitemap with hreflang alternates, robots ----
pages = ['', 'company.html', 'products.html', 'facility.html', 'projects.html', 'contact.html']
today = datetime.date.today().isoformat()
with open(os.path.join(ko.OUT, 'sitemap.xml'), 'w') as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n')
    for u in pages:
        alts = (f'<xhtml:link rel="alternate" hreflang="ko" href="{SITE}/{u}"/>'
                f'<xhtml:link rel="alternate" hreflang="en" href="{SITE}/en/{u}"/>'
                f'<xhtml:link rel="alternate" hreflang="x-default" href="{SITE}/{u}"/>')
        for loc in (f'{SITE}/{u}', f'{SITE}/en/{u}'):
            f.write(f'  <url><loc>{loc}</loc><lastmod>{today}</lastmod>{alts}</url>\n')
    f.write('</urlset>\n')
with open(os.path.join(ko.OUT, 'robots.txt'), 'w') as f:
    f.write(f'User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n')
print('en ok')
