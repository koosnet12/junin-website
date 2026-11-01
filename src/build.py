#!/usr/bin/env python3
"""준인산업 홈페이지 정적 페이지 생성기.
공통 머리말·꼬리말을 한 곳에서 관리하고, 결과는 site/*.html 로 씁니다."""
import csv, html, os, sys, urllib.parse
sys.path.insert(0, os.path.dirname(__file__))
from bars import bar_svg

OUT = os.environ.get('JUNIN_OUT', '/home/claude/site')
DATA = '/mnt/project-files/facility-track-record'

SITE = 'https://www.junin-grating.com'
TEL, FAX, EMAIL = '031-351-3142', '031-351-3149', 'hgkoo@juninmail.com'
ADDR_HQ = '경기도 화성시 만세구 장안면 매바위로366번길 16'
ADDR_LAB = '부산광역시 남구 남동천로 128, BIFC2 1512호'

NAV = [
    ('company.html', '회사소개'),
    ('products.html', '제품'),
    ('facility.html', '설비·생산능력'),
    ('projects.html', '실적'),
]

def esc(s):
    return html.escape(s, quote=True)

def head(title, desc, page):
    full = f'{title} | (주)준인산업' if page != 'index' else '(주)준인산업 | 스틸 그레이팅 전문 제조'
    return f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(full)}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<meta name="description" content="{esc(desc)}">
<meta name="naver-site-verification" content="c93af0cdd106b1a8a34fe475d96d57010b993415">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(full)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="{SITE}/assets/img/hero-line.jpg">
<meta property="og:url" content="{SITE}/{'' if page == 'index' else page + '.html'}">
<meta property="og:site_name" content="(주)준인산업">
<meta property="og:locale" content="ko_KR">
<meta property="og:locale:alternate" content="en_US">
<link rel="canonical" href="{SITE}/{'' if page == 'index' else page + '.html'}">
<link rel="alternate" hreflang="ko" href="{SITE}/{'' if page == 'index' else page + '.html'}">
<link rel="alternate" hreflang="en" href="{SITE}/en/{'' if page == 'index' else page + '.html'}">
<link rel="alternate" hreflang="x-default" href="{SITE}/{'' if page == 'index' else page + '.html'}">
<link rel="icon" type="image/png" sizes="32x32" href="assets/img/mark-32.png">
<link rel="apple-touch-icon" href="assets/img/mark-180.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700&family=IBM+Plex+Sans+KR:wght@400;500;700&display=swap">
<link rel="stylesheet" href="assets/css/site.css">
</head>
<body>
'''

def header(page):
    links = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href.startswith(page + '.') else ''
        links.append(f'<a href="{href}"{cur}>{label}</a>')
    cur = ' aria-current="page"' if page == 'contact' else ''
    links.append(f'<a class="nav-cta" href="contact.html"{cur}>견적 문의</a>')
    return f'''<a class="sr-only" href="#main">본문 바로가기</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="./" aria-label="(주)준인산업 홈"><img src="assets/img/logo.svg" alt="(주)준인산업" width="155" height="34"></a>
    <div class="lang" aria-label="언어 선택"><a href="./{'' if page == 'index' else page + '.html'}" lang="ko" hreflang="ko" aria-current="true">KO</a><a href="en/{'' if page == 'index' else page + '.html'}" lang="en" hreflang="en">EN</a></div>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav"><span></span><span class="sr-only">메뉴</span></button>
    <nav class="nav" id="site-nav" aria-label="주 메뉴">
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
      <h2>도면을 보내주시면 규격과 납기를 검토해 드립니다</h2>
      <p>스팬과 하중 조건에 맞는 베어링 바 규격을 함께 제안합니다.</p>
    </div>
    <div class="contact-quick">
      <a class="tel" href="tel:{TEL.replace('-', '')}">{TEL}</a>
      <a class="btn btn-red" href="contact.html">견적 문의</a>
    </div>
  </div>
</section>
'''

def footer():
    nav = ''.join(f'<a href="{h}">{l}</a>' for h, l in NAV) + '<a href="contact.html">견적 문의</a>'
    return f'''</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="foot-top">
      <img src="assets/img/logo-white.svg" alt="(주)준인산업" width="137" height="30">
      <nav class="foot-nav" aria-label="하단 메뉴">{nav}<a href="assets/docs/junin-catalog.pdf" download>카탈로그</a></nav>
    </div>
    <div class="foot-info">
      <p><span>(주)준인산업</span><span>공동대표이사 이덕근, 구형근</span></p>
      <p><span>본사·공장 {ADDR_HQ}</span><span>기업부설연구소 {ADDR_LAB}</span></p>
      <p><span>TEL <a href="tel:{TEL.replace('-', '')}">{TEL}</a></span><span>FAX {FAX}</span><span>E-mail <a href="mailto:{EMAIL}">{EMAIL}</a></span></p>
    </div>
    <p class="foot-copy">© 2026 JUNIN INDUSTRY Co., Ltd. All rights reserved.</p>
  </div>
</footer>
<script src="assets/js/site.js"></script>
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
  <div class="hero-media"><img src="assets/img/{img}" alt="" fetchpriority="high"></div>
  <div class="wrap">
    <span class="eyebrow">{eyebrow}</span>
    <h1>{h1}</h1>
    <p class="lead">{lead}</p>
    {btns}
  </div>
</section>
'''

def stats(items, light=False):
    lis = ''.join(f'<li><span class="num">{n}</span><span class="label">{l}</span></li>' for n, l in items)
    cls = 'stats stats-light' if light else 'stats'
    return f'<section class="{cls}" aria-label="주요 수치"><div class="wrap"><ul>{lis}</ul></div></section>\n'

# ---------- data ----------
with open(f'{DATA}/annual-delivery.csv') as f:
    ANNUAL = [(int(r['연도']), float(r['납품량(톤)'])) for r in csv.DictReader(f)]
with open(f'{DATA}/key-projects.csv') as f:
    PROJECTS = list(csv.DictReader(f))
with open(f'{DATA}/product-mix.csv') as f:
    MIX = list(csv.DictReader(f))

# ---------- product profile icons (단면) ----------
INK = '#231916'
def prof_ibar():
    # 베어링 바 3본 단면, I형
    g = ''
    for x in (10, 50, 90):
        g += f'<path d="M{x} 4h14v5h-4.5v42h4.5v5h-14v-5h4.5v-42h-4.5z" fill="{INK}"/>'
    return f'<svg viewBox="0 0 114 60" aria-hidden="true">{g}</svg>'
def prof_flat():
    g = ''.join(f'<rect x="{x}" y="4" width="8" height="52" fill="{INK}"/>' for x in (13, 53, 93))
    return f'<svg viewBox="0 0 114 60" aria-hidden="true">{g}</svg>'
def prof_serr(kind='i'):
    # 측면도: 윗면 톱니
    teeth = ''.join(f'<path d="M{6+i*12} 14l6-8l6 8z" fill="{INK}"/>' for i in range(9))
    body = f'<rect x="6" y="14" width="108" height="38" fill="{INK}"/>'
    if kind == 'i':
        body += '<rect x="6" y="20" width="108" height="26" fill="#f3f4f4" opacity=".0"/>'
    return f'<svg viewBox="0 0 120 60" aria-hidden="true">{teeth}{body}<rect x="6" y="52" width="108" height="3" fill="#E60013"/></svg>'
def prof_dense():
    g = ''.join(f'<rect x="{6+i*14}" y="8" width="5" height="48" fill="{INK}"/>' for i in range(8))
    return f'<svg viewBox="0 0 114 60" aria-hidden="true">{g}</svg>'
def prof_stair():
    g = f'<rect x="8" y="22" width="96" height="10" fill="{INK}"/>'
    g += f'<rect x="8" y="22" width="5" height="34" fill="{INK}"/><rect x="99" y="22" width="5" height="34" fill="{INK}"/>'
    g += '<rect x="8" y="22" width="96" height="3" fill="#E60013"/>'
    g += f'<circle cx="10.5" cy="46" r="2" fill="#f3f4f4"/><circle cx="101.5" cy="46" r="2" fill="#f3f4f4"/>'
    return f'<svg viewBox="0 0 114 60" aria-hidden="true">{g}</svg>'

def anatomy_svg():
    # 평면도: 베어링 바(가로, 피치 30) / 크로스 바(세로, 100 간격) / 엔드 바
    x0, y0, L, W = 70, 50, 500, 240
    s = []
    s.append(f'<rect x="{x0}" y="{y0}" width="{L}" height="{W}" fill="#f3f4f4"/>')
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
    # 피치 30 치수선
    s.append(f'<path d="M{x0+L+22} {y0} v30 M{x0+L+16} {y0} h12 M{x0+L+16} {y0+30} h12" stroke="#767E83" stroke-width="1.5" fill="none"/>')
    s.append(f'<text x="{x0+L+34}" y="{y0+21}" {tn}>30</text>')
    # 100 치수선
    s.append(f'<path d="M{x0+100} {y0-22} h100 M{x0+100} {y0-28} v12 M{x0+200} {y0-28} v12" stroke="#767E83" stroke-width="1.5" fill="none"/>')
    s.append(f'<text x="{x0+140}" y="{y0-30}" {tn}>100</text>')
    # 라벨
    s.append(f'<path d="M{x0+430} {y0+90} L{x0+470} {y0+W+40}" stroke="#231916" stroke-width="1" fill="none"/>')
    s.append(f'<text x="{x0+380}" y="{y0+W+58}" {t} font-weight="700">베어링 바</text>')
    s.append(f'<path d="M{x0+300} {y0+150} L{x0+260} {y0+W+40}" stroke="#231916" stroke-width="1" fill="none"/>')
    s.append(f'<text x="{x0+200}" y="{y0+W+58}" {t} font-weight="700">크로스 바</text>')
    s.append(f'<path d="M{x0} {y0+W} L{x0-20} {y0+W+40}" stroke="#231916" stroke-width="1" fill="none"/>')
    s.append(f'<text x="{x0-60}" y="{y0+W+58}" {t} font-weight="700" fill="#E60013">엔드 바</text>')
    s.append(f'<text x="{x0+L/2}" y="{y0+W+90}" {t} text-anchor="middle" fill="#767E83">길이 = 베어링 바 방향  ·  폭 = 크로스 바 방향</text>')
    return f'<svg viewBox="0 0 680 400" role="img" aria-label="그레이팅 평면도: 베어링 바 피치 30mm, 크로스 바 간격 100mm, 양 끝 엔드 바">{"".join(s)}</svg>'

def annual_chart():
    W, H = 760, 360
    ml, mr, mt, mb = 52, 12, 34, 44
    pw, ph = W - ml - mr, H - mt - mb
    ymax = 5000
    n = len(ANNUAL)
    slot = pw / n
    bw = slot * 0.62
    s = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-labelledby="annual-title annual-desc">',
         '<title id="annual-title">연도별 납품량</title>',
         '<desc id="annual-desc">' + ', '.join(f'{y}년 {v:,.0f}톤' for y, v in ANNUAL) + '</desc>']
    for t in range(0, ymax + 1, 1000):
        y = mt + ph - ph * t / ymax
        s.append(f'<line x1="{ml}" x2="{W-mr}" y1="{y:.1f}" y2="{y:.1f}" stroke="#d8dcde" stroke-width="1"/>')
        s.append(f'<text x="{ml-8}" y="{y+5:.1f}" text-anchor="end" font-family="Barlow Condensed, sans-serif" font-size="15" fill="#767E83">{t:,}</text>')
    # 3,000톤 기준선
    y3 = mt + ph - ph * 3000 / ymax
    s.append(f'<line x1="{ml}" x2="{W-mr}" y1="{y3:.1f}" y2="{y3:.1f}" stroke="#E60013" stroke-width="1.5" stroke-dasharray="5 4"/>')
    for i, (yr, v) in enumerate(ANNUAL):
        x = ml + slot * i + (slot - bw) / 2
        h = ph * v / ymax
        y = mt + ph - h
        partial = yr in (2016, 2026)
        fill = '#a9b0b4' if partial else '#231916'
        s.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bw:.1f}" height="{h:.1f}" fill="{fill}"/>')
        s.append(f'<text x="{x+bw/2:.1f}" y="{y-8:.1f}" text-anchor="middle" font-family="Barlow Condensed, sans-serif" font-size="16" font-weight="600" fill="#231916">{v:,.0f}</text>')
        s.append(f'<text x="{x+bw/2:.1f}" y="{H-mb+22}" text-anchor="middle" font-family="Barlow Condensed, sans-serif" font-size="16" fill="#231916">{yr}</text>')
    s.append(f'<text x="{ml}" y="{mt-16}" font-family="IBM Plex Sans KR, sans-serif" font-size="13" fill="#767E83">단위: 톤</text>')
    s.append(f'<text x="{ml+6}" y="{y3-7:.1f}" text-anchor="start" font-family="IBM Plex Sans KR, sans-serif" font-size="13" fill="#E60013">3,000톤</text>')
    s.append('</svg>')
    return '\n'.join(s)

# =====================================================================
# 홈
# =====================================================================
top6 = PROJECTS[:6]
def proj_cards(rows):
    out = []
    for r in rows:
        out.append(f'''<article class="proj">
  <span class="field">{esc(r["분야"])}</span>
  <h3>{esc(r["프로젝트"].replace("(P3 P4 등)", "(P3, P4 등)"))}</h3>
  <span class="client">{esc(r["발주처"])}</span>
  <div class="meta"><span>{esc(r["시기"])}</span><span class="num">약 {int(r["납품량(톤)"]):,}<small>톤</small></span></div>
</article>''')
    return '\n'.join(out)

home = f'''<section class="hero">
  <div class="hero-media"><img src="assets/img/hero-line.jpg" alt="준인산업 공장의 그레이팅 자동 압접 라인" fetchpriority="high"></div>
  <div class="wrap">
    <span class="eyebrow">Steel Grating Manufacturer</span>
    <h1>대한민국 산업 현장을 받치는 그레이팅, <em>준인산업</em>이 만듭니다</h1>
    <p class="lead">석유화학 플랜트에서 발전소, 반도체 공장, 데이터센터까지. 지난 10년간 37,300톤의 스틸 그레이팅을 납품했습니다.</p>
    <div class="btns">
      <a class="btn btn-red" href="contact.html">견적 문의</a>
      <a class="btn btn-line" href="products.html">제품 보기</a>
    </div>
  </div>
</section>
''' + stats([
    ('37,300<small>톤</small>', '10년간 누적 납품'),
    ('6,205<small>건</small>', '납품 작업'),
    ('350<small>곳+</small>', '거래 기업'),
    ('<span class="pre">월 최대</span>1,000<small>톤</small>', '그레이팅 생산 규모'),
]) + f'''
<section class="section">
  <div class="wrap split">
    <div class="split-text" style="display:grid;gap:22px">
      <span class="eyebrow">About</span>
      <h2 style="font-size:clamp(26px,3.2vw,38px)">압연바 입고부터 출고까지,<br>한 사업장에서 한 흐름으로</h2>
      <div class="prose">
        <p>준인산업은 2016년 설립 이래 스틸 그레이팅 한 길을 걸어온 제조기업입니다. 경기도 화성 사업장에서 자동 압접, 제작, 용융아연도금, 세 번의 검사, 포장까지 전 공정을 관리합니다.</p>
        <p>모든 제품은 고객의 도면에 맞춰 만들고, 치수 공차는 미국 건축금속제조협회(NAAMM) 기준을 따릅니다. ISO 9001·ISO 14001 품질·환경경영 시스템으로 관리합니다.</p>
      </div>
      <div><a class="link-more" href="company.html">회사소개 보기</a></div>
    </div>
    <div class="split-media"><img src="assets/img/02-press-welder-2-front.jpg" alt="자동 압접기 2호기 전면" loading="lazy"></div>
  </div>
</section>

<section class="section section-paper">
  <div class="wrap">
    <div class="sec-head sec-head-row">
      <div><span class="eyebrow">Products</span><h2>현장에 맞춰 만드는 그레이팅</h2><p>베어링 바 형태와 피치, 끝 마감을 설계 조건에 맞춰 고릅니다.</p></div>
      <div style="display:flex;gap:20px;flex-wrap:wrap"><a class="link-more" href="assets/docs/junin-catalog.pdf" download>카탈로그 내려받기</a><a class="link-more" href="products.html">전체 규격 보기</a></div>
    </div>
    <div class="cards">
      <a class="card" href="products.html#types">
        <div class="profile">{bar_svg("i")}</div>
        <span class="code">I-BAR · FLAT BAR</span>
        <h3>스틸 그레이팅</h3>
        <p>I-Bar와 Flat Bar 베어링 바에 크로스 바를 압접한 표준 그레이팅입니다. 피치 30·35.3·40mm.</p>
        <span class="link-more">규격 보기</span>
      </a>
      <a class="card" href="products.html#types">
        <div class="profile">{bar_svg("si")}</div>
        <span class="code">SERRATED</span>
        <h3>톱니형 그레이팅</h3>
        <p>베어링 바 윗면에 톱니를 내 미끄럼을 줄입니다. 톱니 I-Bar형과 톱니형이 있습니다.</p>
        <span class="link-more">규격 보기</span>
      </a>
      <a class="card" href="products.html#stair">
        <div class="profile">{prof_stair()}</div>
        <span class="code">STAIR TREAD</span>
        <h3>계단 발판</h3>
        <p>용접형과 볼트형, 폭 215·245·275mm. 길이 500~1,200mm로 제작합니다.</p>
        <span class="link-more">규격 보기</span>
      </a>
    </div>
  </div>
</section>

<section class="section section-dark grating-bg">
  <div class="wrap">
    <div class="sec-head sec-head-row">
      <div><span class="eyebrow">Process</span><h2>자동 압접기 3기가 만드는 생산 라인</h2><p>2,230kVA급 자동 압접기 3기를 동시에 가동해 큰 프로젝트 물량과 급한 납기를 함께 소화합니다.</p></div>
      <a class="link-more" href="facility.html">설비·생산능력 보기</a>
    </div>
    <ol class="flow">
      <li><figure><img src="assets/img/v-01-press-welding.jpg" alt="자동 압접" loading="lazy"></figure><span class="step">STEP 1</span><h3>자동 압접</h3><p>베어링 바와 크로스 바를 전기 저항 압접으로 한 몸으로 만듭니다.</p></li>
      <li><figure><img src="assets/img/v-02-high-speed-cutting.jpg" alt="고속 절단" loading="lazy"></figure><span class="step">STEP 2</span><h3>고속 절단</h3><p>도면 치수대로 패널을 자릅니다.</p></li>
      <li><figure><img src="assets/img/v-03-shape-cutting.jpg" alt="형상 절단" loading="lazy"></figure><span class="step">STEP 3</span><h3>형상 가공</h3><p>배관·기둥 자리의 개구부를 따냅니다.</p></li>
      <li><figure><img src="assets/img/v-04-welding.jpg" alt="용접" loading="lazy"></figure><span class="step">STEP 4</span><h3>용접</h3><p>엔드 바와 개구부 보강을 용접합니다.</p></li>
      <li><figure><img src="assets/img/v-05-grinding.jpg" alt="사상" loading="lazy"></figure><span class="step">STEP 5</span><h3>사상·검사</h3><p>용접부를 다듬고 NAAMM 공차로 확인합니다.</p></li>
      <li><figure><img src="assets/img/v-06-galvanized-product.jpg" alt="용융아연도금 완제품" loading="lazy"></figure><span class="step">STEP 6</span><h3>도금·출고</h3><p>용융아연도금 후 검사를 거쳐 출고합니다.</p></li>
    </ol>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head sec-head-row">
      <div><span class="eyebrow">Projects</span><h2>준인산업 그레이팅이 설치된 현장</h2><p>철구조물 전문업체를 거쳐 반도체, 석유화학, 공항, 해외 플랜트 현장에 납품했습니다.</p></div>
      <a class="link-more" href="projects.html">10년 실적 보기</a>
    </div>
    <div class="proj-grid">
{proj_cards(top6)}
    </div>
  </div>
</section>
''' + cta_band()

page('index', '홈', '스틸 그레이팅 전문 제조기업 (주)준인산업. 자동 압접기 3기, 월 최대 1,000톤 규모, 10년간 37,300톤 납품.', home)

# =====================================================================
# 회사소개
# =====================================================================
HISTORY = [
    ('2016.04', '㈜준인산업 설립(공동대표 이덕근·구형근)'),
    ('2016.05', 'ISO 9001, ISO 14001 인증'),
    ('2016.09', '벤처기업 인증'),
    ('2016.10', '그레이팅 자동 압접설비 인수, 가동'),
    ('2017.01', '기업부설연구소 설립'),
    ('2017.03', '나라장터(조달청) 등록'),
    ('2017.04', '배수용 그레이팅 디자인 등록'),
    ('2018.10', '베트남 수출 시작(DOOSAN VINA)'),
    ('2019.06', '경영혁신형 중소기업(MAIN-BIZ) 인증'),
    ('2025.05', 'ISO 9001·14001 갱신'),
    ('2026.08', '기업부설연구소 부산 이전(BIFC2)'),
]
hist = ''.join(f'<li><span class="num">{d}</span><span>{esc(t)}</span></li>' for d, t in HISTORY)

def maplinks(addr):
    q = urllib.parse.quote(addr)
    return f'<div class="maps"><a href="https://map.naver.com/p/search/{q}" target="_blank" rel="noopener">네이버 지도</a><a href="https://map.kakao.com/?q={q}" target="_blank" rel="noopener">카카오맵</a></div>'

company = sub_hero('Company', '기술과 신뢰로 이어가는<br>스틸 그레이팅 전문기업', '2016년 설립 이래 그레이팅 한 길을 걸어왔습니다. 화성 사업장에서 압접부터 출고까지 전 공정을 직접 관리합니다.', '13-welding-shop.jpg') + f'''
<nav class="subnav" aria-label="회사소개 바로가기"><div class="wrap">
  <a href="#greeting">인사말</a><a href="#vision">비전</a><a href="#history">연혁</a><a href="#cert">인증</a><a href="#location">오시는 길</a>
</div></nav>

<section class="section" id="greeting">
  <div class="wrap split" style="align-items:start">
    <div style="display:grid;gap:18px">
      <span class="eyebrow">Greeting</span>
      <h2 style="font-size:clamp(26px,3.2vw,38px)">고객의 현장을 먼저 생각하는 회사가 되겠습니다</h2>
    </div>
    <div class="prose">
      <p>안녕하십니까. 주식회사 준인산업 홈페이지를 찾아주셔서 감사합니다.</p>
      <p>준인산업은 2016년 설립 이래 스틸 그레이팅 한 길을 걸어온 전문 제조기업입니다. 경기도 화성 본사·공장에서 원자재 입고부터 자동 압접, 제작, 용융아연도금, 검사, 출고까지 전 공정을 관리하며, 지난 10년간 350곳이 넘는 고객사에 37,300톤의 그레이팅과 계단 발판을 납품했습니다.</p>
      <p>석유화학 플랜트, 발전소, 데이터센터, 공항 등 안전이 가장 중요한 현장에서 준인산업의 그레이팅이 쓰이고 있습니다. 모든 제품은 고객의 설계에 맞추어 제작하고, 미국 건축금속제조협회(NAAMM) 기준의 공차와 ISO 9001·ISO 14001 품질·환경경영 시스템으로 관리합니다.</p>
      <p>앞으로도 "기술과 신뢰로 이어가는 준인산업"이라는 약속을 지키며, 고객의 현장을 먼저 생각하는 회사가 되겠습니다.</p>
      <p style="font-weight:700;margin-top:.6em">주식회사 준인산업 공동대표이사 이덕근, 구형근</p>
    </div>
  </div>
</section>

<section class="section section-dark grating-bg" id="vision">
  <div class="wrap">
    <div class="sec-head">
      <span class="eyebrow">Vision</span>
      <h2 class="num" style="font-size:clamp(34px,5vw,60px);font-weight:600;letter-spacing:-.01em;color:#fff">Innovative Challenger for Your Dream</h2>
      <p>진취적인 생각과 한 발 앞선 행동으로 시장을 이끕니다.</p>
    </div>
    <div class="values">
      <div><span class="en">Technology</span><h3>기술</h3><p>품질관리 시스템과 제작표시로 제품 하나하나를 추적합니다.</p></div>
      <div><span class="en">Market Intelligence</span><h3>시장 이해</h3><p>고객과 현장이 요구하는 것을 앞서 파악합니다.</p></div>
      <div><span class="en">Customer First</span><h3>고객 우선</h3><p>고객과 함께 생각하고 함께 만듭니다.</p></div>
    </div>
  </div>
</section>

<section class="section" id="history">
  <div class="wrap split" style="align-items:start">
    <div style="display:grid;gap:18px">
      <span class="eyebrow">History</span>
      <h2 style="font-size:clamp(26px,3.2vw,38px)">연혁</h2>
      <p class="note" style="font-size:16px">2016년 4월 설립, 같은 해 10월 자동 압접설비를 가동하며 그레이팅 생산을 시작했습니다.</p>
    </div>
    <ol class="timeline">{hist}</ol>
  </div>
</section>

<section class="section section-paper" id="cert">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">Certification</span><h2>인증</h2><p>품질·환경경영 시스템 인증을 2016년부터 유지하고 있습니다.</p></div>
    <div class="certs">
      <div class="cert"><span class="std">ISO 9001</span><h3>품질경영시스템</h3>
        <dl><dt>인증범위</dt><dd>그레이팅 및 철구조물의 제조</dd><dt>유효기간</dt><dd>2028년 5월 25일까지</dd></dl></div>
      <div class="cert"><span class="std">ISO 14001</span><h3>환경경영시스템</h3>
        <dl><dt>인증범위</dt><dd>그레이팅 및 철구조물의 제조</dd><dt>유효기간</dt><dd>2028년 5월 25일까지</dd></dl></div>
    </div>
  </div>
</section>

<section class="section" id="location">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">Location</span><h2>오시는 길</h2></div>
    <div class="locs">
      <div class="loc"><span class="tag">본사 · 공장</span><h3>화성 사업장</h3><address>{ADDR_HQ}</address>
        <p>TEL {TEL} · FAX {FAX}</p>{maplinks(ADDR_HQ)}</div>
      <div class="loc"><span class="tag">기업부설연구소</span><h3>부산 연구소</h3><address>{ADDR_LAB}</address>
        <p>설계, 하중 검토</p>{maplinks('부산광역시 남구 남동천로 128')}</div>
    </div>
  </div>
</section>
''' + cta_band()
page('company', '회사소개', '(주)준인산업 인사말, 비전, 연혁, ISO 9001·14001 인증, 오시는 길.', company)

# =====================================================================
# 제품
# =====================================================================
IBAR = [('I-25','25×5×3','0.605','0.484'),('I-32','32×5×3','1.251','0.782'),('I-38','38×5×3','2.083','1.096'),('I-44','44×5×3','3.221','1.464'),('I-50','50×5×3','4.609','1.844'),('I-50 (7T)','50×7×4','6.432','2.573'),('I-55','55×7×4','8.488','3.086'),('I-65','65×7×4','13.960','4.295'),('I-75','75×7×4','21.387','5.703')]
FBAR = [('F-25','25×5','0.651','0.521'),('F-32','32×5','1.365','0.853'),('F-38','38×5','2.286','1.203'),('F-44','44×5','3.549','1.613'),('F-50','50×5','5.208','2.083'),('F-50 (6T)','50×6','6.250','2.500'),('F-65','65×6','13.731','4.225'),('F-75','75×6','21.094','5.625'),('F-90','90×6','36.450','8.100')]
WEIGHT = [
 ('I-Bar 25×5×3','31.4','29.5','27.4','25.4','25.1','23.1'),('I-Bar 32×5×3','38.6','36.1','33.8','31.3','30.9','28.4'),('I-Bar 38×5×3','44.2','41.3','38.6','35.6','35.2','32.2'),('I-Bar 44×5×3','50.5','47.1','44.0','40.5','40.1','36.6'),('I-Bar 50×5×3','55.4','51.5','48.3','44.4','44.0','40.1'),
 ('I-Bar 50×7×4','–','–','67.5','62.8','61.5','56.8'),('I-Bar 55×7×4','–','–','73.2','68.0','66.6','61.4'),('I-Bar 65×7×4','–','–','85.2','79.1','77.4','71.3'),('I-Bar 75×7×4','–','–','97.4','90.3','88.5','81.4'),
 ('F-Bar 25×3','23.3','22.1','–','–','–','–'),('F-Bar 32×3','29.1','27.6','–','–','–','–'),('F-Bar 38×3','34.2','32.4','–','–','–','–'),
 ('F-Bar 25×5','38.1','36.2','33.2','31.2','30.3','28.3'),('F-Bar 32×5','48.1','45.6','41.8','39.3','38.1','35.6'),('F-Bar 38×5','56.5','53.5','49.1','46.1','44.7','41.7'),('F-Bar 44×5','65.0','61.6','56.4','53.0','51.3','47.8'),('F-Bar 50×5','73.6','69.7','–','–','–','–'),
]
def rows4(data):
    return ''.join(f'<tr><th scope="row">{a}</th><td>{b}</td><td>{c}</td><td>{d}</td></tr>' for a, b, c, d in data)
wrows = ''.join('<tr><th scope="row">' + r[0] + '</th>' + ''.join(f'<td class="{"muted" if v=="–" else ""}">{v}</td>' for v in r[1:]) + '</tr>' for r in WEIGHT)

products = sub_hero('Products', '설계 조건에 맞춰 만드는<br>스틸 그레이팅', '베어링 바 형태와 피치, 끝 마감을 현장에 맞게 고르고, 모든 제품을 도면 치수대로 제작합니다.', 'v-06-galvanized-product.jpg',
    '<div class="btns"><a class="btn btn-red" href="assets/docs/junin-catalog.pdf" download>카탈로그 내려받기</a><a class="btn btn-line" href="assets/docs/junin-grating-spec-2026-10.pdf" target="_blank" rel="noopener">규격표 PDF</a></div>') + f'''
<nav class="subnav" aria-label="제품 바로가기"><div class="wrap">
  <a href="#structure">구조</a><a href="#types">종류</a><a href="#spec">기본 치수</a><a href="#bars">베어링 바</a><a href="#weight">단위중량</a><a href="#stair">계단 발판</a><a href="#fixing">고정 방법</a><a href="#galv">용융아연도금</a>
</div></nav>

<section class="section" id="structure">
  <div class="wrap anatomy">
    <div style="display:grid;gap:18px">
      <span class="eyebrow">Structure</span>
      <h2 style="font-size:clamp(26px,3.2vw,38px)">스틸 그레이팅의 구조</h2>
      <div class="prose">
        <p>스틸 그레이팅은 하중을 받는 <strong>베어링 바</strong>를 일정한 간격(피치)으로 세우고, 그 위를 <strong>크로스 바</strong>로 가로질러 전기 저항 압접으로 한 몸으로 만든 격자형 바닥재입니다.</p>
        <p>빛과 공기, 빗물이 통과하고 무게에 비해 강도가 높아 플랜트의 통로와 작업대, 배수로 덮개, 계단에 쓰입니다. 패널 양 끝은 엔드 바로 막거나(엔드바형) 열어 둡니다(컷엔드형).</p>
      </div>
    </div>
    <div>{anatomy_svg()}</div>
  </div>
</section>

<section class="section section-paper" id="types">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">Types</span><h2>베어링 바 형태</h2><p>베어링 바의 단면 형태에 따라 네 가지로 나뉘고, 각각 엔드바형과 오픈엔드형으로 만듭니다.</p></div>
    <div class="types types-4">
      <div class="type"><div class="profile">{bar_svg("i")}</div><span class="code">I-BAR</span><h3>I-Bar형 그레이팅</h3><p>베어링 바의 단면형이 I형일 때 I-Bar형 그레이팅이라고 합니다.</p></div>
      <div class="type"><div class="profile">{bar_svg("f")}</div><span class="code">FLAT BAR</span><h3>플렛 바 그레이팅</h3><p>베어링 바의 단면이 평면일 때 플렛 바 그레이팅이라고 합니다.</p></div>
      <div class="type"><div class="profile">{bar_svg("si")}</div><span class="code">SERRATED I-BAR</span><h3>톱니 I-Bar형 그레이팅</h3><p>베어링 바의 단면형이 톱니형과 I형을 접목한 형태일 때 톱니 I-Bar형 그레이팅이라고 합니다.</p></div>
      <div class="type"><div class="profile">{bar_svg("sf")}</div><span class="code">SERRATED</span><h3>톱니형 그레이팅</h3><p>베어링 바의 상부면이 톱니형일 때 톱니형 그레이팅이라고 합니다.</p></div>
    </div>
  </div>
</section>

<section class="section" id="spec">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">Specification</span><h2>기본 치수</h2></div>
    <div class="table-scroll"><table class="tbl">
      <tbody>
        <tr><th scope="row">베어링 바 형태</th><td>I-Bar, Flat Bar, 톱니 I-Bar(SI), 톱니 Flat Bar(SF)</td></tr>
        <tr><th scope="row">베어링 바 간격</th><td class="num" style="font-size:17px">12.5 / 15 / 25 / 30 / 35.3 / 40 mm</td></tr>
        <tr><th scope="row">크로스 바 간격</th><td class="num" style="font-size:17px">100 mm</td></tr>
        <tr><th scope="row">크로스 바</th><td>피치 30mm: 6×6 사각봉 · 35.3mm: 8×8 사각봉 · 15mm: ø6 환봉 · 12.5mm: ø5 환봉</td></tr>
        <tr><th scope="row">최대 표준 폭</th><td>995 mm (베어링 바 수와 피치로 결정)</td></tr>
        <tr><th scope="row">길이</th><td>설계 치수에 맞춰 제작 (길이 = 베어링 바 방향, 폭 = 크로스 바 방향)</td></tr>
        <tr><th scope="row">끝 마감</th><td>엔드바형 / 컷엔드(오픈엔드)형</td></tr>
        <tr><th scope="row">재질</th><td>탄소강 압연바 JIS G3101 SS400, SS275</td></tr>
        <tr><th scope="row">표면처리</th><td>용융아연도금 KS D 8308, JIS H8641, ASTM A123</td></tr>
        <tr><th scope="row">제작 공차</th><td>NAAMM(미국 건축금속제조협회) 기준</td></tr>
      </tbody>
    </table></div>
  </div>
</section>

<section class="section section-paper" id="bars">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">Bearing Bar</span><h2>베어링 바 규격</h2><p>I = 단면 2차 모멘트, Z = 단면계수 (베어링 바 1본 기준)</p></div>
    <div class="split" style="align-items:start">
      <div><h3 style="font-size:18px;margin-bottom:12px">I-Bar</h3><div class="table-scroll"><table class="tbl tbl-compact tbl-spec">
        <thead><tr><th>형식</th><th>치수 H×W×T (mm)</th><th>I (cm⁴)</th><th>Z (cm³)</th></tr></thead>
        <tbody>{rows4(IBAR)}</tbody></table></div></div>
      <div><h3 style="font-size:18px;margin-bottom:12px">Flat Bar</h3><div class="table-scroll"><table class="tbl tbl-compact tbl-spec">
        <thead><tr><th>형식</th><th>치수 H×T (mm)</th><th>I (cm⁴)</th><th>Z (cm³)</th></tr></thead>
        <tbody>{rows4(FBAR)}</tbody></table></div></div>
    </div>
    <div class="split" style="align-items:start;margin-top:48px">
      <div><h3 style="font-size:18px;margin-bottom:12px">톱니형</h3><div class="table-scroll"><table class="tbl tbl-compact tbl-spec">
        <thead><tr><th>형식</th><th>규격</th><th>피치 (mm)</th><th>크로스 바</th></tr></thead>
        <tbody><tr><th scope="row">톱니 I-Bar</th><td>SI-25 ~ SI-44 (×5×3)</td><td>30 / 15</td><td>6×6 / ø6</td></tr>
        <tr><th scope="row">톱니 Flat Bar</th><td>SF-25 ~ SF-44 (×5)</td><td>30</td><td>6×6</td></tr></tbody></table></div>
        <p class="note" style="margin-top:10px">톱니형의 단위중량은 같은 규격의 I-Bar·Flat Bar와 같습니다.</p></div>

    </div>
  </div>
</section>

<section class="section" id="weight">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">Unit Weight</span><h2>단위중량</h2><p>kg/m², 용융아연도금 후 기준</p></div>
    <div class="table-scroll"><table class="tbl tbl-compact tbl-spec">
      <thead>
        <tr><th rowspan="2" style="text-align:left">베어링 바</th><th colspan="2">피치 30mm</th><th colspan="2">피치 35.3mm</th><th colspan="2">피치 40mm</th></tr>
        <tr><th>엔드바형</th><th>컷엔드형</th><th>엔드바형</th><th>컷엔드형</th><th>엔드바형</th><th>컷엔드형</th></tr>
      </thead>
      <tbody>{wrows}</tbody>
    </table></div>
    <p class="note" style="margin-top:12px">'–'는 표준 단위중량 자료가 없는 조합입니다. 표에 없는 규격도 주문 제작합니다.</p>
  </div>
</section>

<section class="section section-paper" id="stair">
  <div class="wrap split" style="align-items:start">
    <div style="display:grid;gap:18px">
      <span class="eyebrow">Stair Tread</span>
      <h2 style="font-size:clamp(26px,3.2vw,38px)">계단 발판</h2>
      <p class="note" style="font-size:16px">그레이팅 양 끝에 엔드 플레이트를 붙여 계단 측판에 용접하거나 볼트로 고정합니다.</p>
      <div style="max-width:260px;margin-top:8px">{prof_stair()}</div>
    </div>
    <div class="table-scroll"><table class="tbl">
      <tbody>
        <tr><th scope="row">체결 방식</th><td>용접형 / 볼트형</td></tr>
        <tr><th scope="row">폭 (볼트 구멍 간격)</th><td>215 mm (120) · 245 mm (150) · 275 mm (180)</td></tr>
        <tr><th scope="row">길이</th><td>500 ~ 1,200 mm</td></tr>
        <tr><th scope="row">베어링 바</th><td>F25×5, F32×5, I25×5×3, I32×5×3</td></tr>
        <tr><th scope="row">엔드 플레이트</th><td>모든 베어링 바에 3 mm 이상 필렛 용접</td></tr>
      </tbody>
    </table></div>
  </div>
</section>

<section class="section" id="fixing">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">Fixing</span><h2>고정 방법</h2><p>진동, 탈착 필요 여부, 시공 속도에 따라 고릅니다.</p></div>
    <div class="fix">
      <div><h3>새들 클립</h3><p>볼트로 고정하며 떼어낼 수 있습니다.</p></div>
      <div><h3>상하 클립</h3><p>위아래로 물려 진동에 강합니다.</p></div>
      <div><h3>셀프 드릴링 스크류</h3><p>천공 없이 빠르게 시공합니다.</p></div>
      <div><h3>현장 용접</h3><p>떼어낼 필요가 없는 구간에 씁니다.</p></div>
    </div>
  </div>
</section>

<section class="section section-paper" id="galv">
  <div class="wrap split">
    <div style="display:grid;gap:18px">
      <span class="eyebrow">Hot-dip Galvanizing</span>
      <h2 style="font-size:clamp(26px,3.2vw,38px)">용융아연도금</h2>
      <div class="prose">
        <p>제작을 마친 그레이팅은 녹은 아연에 담가 표면 전체를 아연층으로 덮습니다. 옥외와 습한 플랜트 환경에서 부식을 막습니다.</p>
        <p>KS D 8308, JIS H8641, ASTM A123 기준으로 도금하고, 도금 두께와 표면 상태를 측정한 뒤 출고합니다.</p>
      </div>
    </div>
    <div class="split-media"><img src="assets/img/15-sorting-after-galvanizing.jpg" alt="도금 후 선별 작업" loading="lazy"></div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="callout">
      <h3>허용하중 검토</h3>
      <p>허용하중과 처짐은 스팬, 하중 종류(보행·차량·집중하중), 지지 조건에 따라 달라집니다. 설치 도면과 하중 조건을 보내주시면 기업부설연구소에서 현장에 맞는 베어링 바 규격을 검토해 제안해 드립니다.</p>
      <div class="btns" style="margin-top:10px"><a class="btn btn-red" href="contact.html">하중 검토 요청</a><a class="btn btn-line" href="assets/docs/junin-grating-spec-2026-10.pdf" target="_blank" rel="noopener">규격표 PDF</a><a class="btn btn-line" href="assets/docs/junin-catalog.pdf" download>카탈로그</a></div>
    </div>
    <p class="note" style="margin-top:14px">본 자료의 내용은 제품 개선을 위해 예고 없이 바뀔 수 있습니다.</p>
  </div>
</section>
''' + cta_band()
page('products', '제품', '스틸 그레이팅 구조, 베어링 바 형태(I-Bar, 플렛 바, 톱니 I-Bar, 톱니형), 기본 치수, 단위중량표, 계단 발판, 고정 방법.', products)

# =====================================================================
# 설비·생산능력
# =====================================================================
EQUIP = [
 ('그레이팅 제조','자동 압접기 (Auto projection welding M/C)','2,230kVA, 2 bar(크로스 바 2개 동시 압접), Nisseki Eng.(일본) 1기·태양공업 2기','3'),
 ('그레이팅 제조','고속 절단기','30kW × 2P','3'),
 ('그레이팅 제조','디스크 절단기','3.7kW × 4P','3'),
 ('그레이팅 제조','톱날 연삭기','외경 609mm × 10mm, 독일산','2'),
 ('그레이팅 제조','CO2·아크 용접기','500A, 20~25kVA','15'),
 ('기계가공','선반·밀링·레이디얼 드릴·드릴·평면 연삭기','화천기계 등','11'),
 ('운반','천장크레인','3톤·5톤','4'),
 ('운반','호이스트','1톤','8'),
 ('운반','지게차','3톤','2'),
 ('계측·시험','정반, 하이트·실린더 게이지, 마이크로미터, 도금 두께 측정기 등','대부분 일본산','31'),
]
eq = ''.join(f'<tr><td class="muted">{a}</td><th scope="row">{b}</th><td>{c}</td><td class="r num" style="font-size:18px">{d}</td></tr>' for a, b, c, d in EQUIP)
STEPS = [
 ('원자재 구매','국내 압연바 제조사에서 SS400·SS275 압연바를 들여옵니다.', False),
 ('자동 압접','베어링 바와 크로스 바를 전기 저항 압접으로 한 몸으로 만듭니다.', False),
 ('제작','도면 치수대로 절단하고 엔드 바, 개구부 보강을 용접합니다.', False),
 ('제작 검사','치수와 용접 상태를 NAAMM 공차 기준으로 확인합니다.', True),
 ('도금','KS D 8308·JIS H8641·ASTM A123 기준 용융아연도금을 합니다.', False),
 ('도금 검사','도금 두께와 표면 상태를 측정합니다.', True),
 ('최종 검사','수량, 제작표시, 최종 치수를 확인합니다.', True),
 ('포장','현장 설치 순서에 맞춰 묶고 표시합니다.', False),
 ('운반','납기일에 맞춰 현장으로 출고합니다.', False),
 ('설치','고정 클립 등으로 현장에 설치합니다.', False),
]
steps = ''.join(f'<li class="{"qc" if q else ""}"><span class="n">{i:02d}</span><h3>{t}</h3><p>{d}</p></li>' for i, (t, d, q) in enumerate(STEPS, 1))
TEAM = [('기계 압접부','5명','자동 압접기 운전, 평균 경력 31년'),('제작부','11명','절단, 용접, 가공'),('포장부','3명','포장, 출고'),('품질관리부','3명','제작·도금·최종 검사'),('생산관리본부','2명','공정·납기 관리'),('기업부설연구소','4명','설계, 하중 검토')]
team = ''.join(f'<tr><th scope="row">{a}</th><td class="r num" style="font-size:18px">{b}</td><td>{c}</td></tr>' for a, b, c in TEAM)
CHAP = [(0,'압접','v-01-press-welding.jpg'),(5,'고속 절단','v-02-high-speed-cutting.jpg'),(10,'형상 절단','v-03-shape-cutting.jpg'),(15,'용접','v-04-welding.jpg'),(20,'사상','v-05-grinding.jpg'),(25,'도금 완제품','v-06-galvanized-product.jpg')]
chap = ''.join(f'<li><button type="button" data-seek="{t}"><img src="assets/img/{img}" alt="" loading="lazy"><span><span class="t">0:{t:02d}</span> {lbl}</span></button></li>' for t, lbl, img in CHAP)

facility = sub_hero('Facility', '자동 압접기 3기,<br>월 최대 1,000톤 규모의 생산 라인', '압연바 입고부터 자동 압접, 제작, 용융아연도금, 세 번의 검사, 포장까지. 약 9,000평 사업장에서 한 흐름으로 만듭니다.', '01-press-welder-line-front.jpg',
    '<div class="btns"><a class="btn btn-red" href="contact.html">견적 문의</a><a class="btn btn-line" href="products.html#spec">제품 규격 보기</a></div>') + stats([
    ('3<small>기</small>', '2,230kVA급 그레이팅 자동 압접기'),
    ('<span class="pre">월 최대</span>1,000<small>톤</small>', '그레이팅 생산능력'),
    ('<span class="pre">약</span>9,000<small>평</small>', '사업장 부지'),
    ('<span class="pre">평균</span>31<small>년</small>', '압접 핵심 인력 경력'),
]) + f'''
<nav class="subnav" aria-label="설비 바로가기"><div class="wrap">
  <a href="#equipment">주요 설비</a><a href="#video">공정 영상</a><a href="#process">제작 공정</a><a href="#quality">품질관리</a><a href="#people">사람</a>
</div></nav>

<section class="section" id="equipment">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">Equipment</span><h2>주요 설비</h2>
      <p>그레이팅의 품질은 압접에서 결정됩니다. 준인산업은 일본 Nisseki사와 태양공업의 2,230kVA급 자동 압접기 3기를 동시에 가동해, 큰 프로젝트 물량과 급한 납기를 함께 소화합니다.</p></div>
    <div class="photos" style="margin-bottom:40px">
      <figure><img src="assets/img/02-press-welder-2-front.jpg" alt="자동 압접기 2호기 전면" loading="lazy"><figcaption>자동 압접기 2호기</figcaption></figure>
      <figure><img src="assets/img/04-nipping-machine.jpg" alt="니핑기" loading="lazy"><figcaption>니핑기</figcaption></figure>
      <figure><img src="assets/img/05-high-speed-cutter.jpg" alt="고속 절단기" loading="lazy"><figcaption>고속 절단기</figcaption></figure>
      <figure><img src="assets/img/06-high-speed-cutter-2.jpg" alt="고속 절단기로 패널을 자르는 모습" loading="lazy"><figcaption>고속 절단 작업</figcaption></figure>
    </div>
    <div class="table-scroll"><table class="tbl tbl-wide">
      <thead><tr><th>구분</th><th>설비</th><th>사양</th><th class="r">수량</th></tr></thead>
      <tbody>{eq}</tbody>
    </table></div>
  </div>
</section>

<section class="section section-dark grating-bg" id="video">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">Process Film</span><h2>30초로 보는 그레이팅 제작</h2><p>압접부터 도금 완제품까지, 실제 공장에서 촬영했습니다. 아래 장면을 누르면 해당 구간으로 이동합니다.</p></div>
    <div class="video-frame"><video id="process-video" controls playsinline muted preload="metadata" poster="assets/img/v-01-press-welding.jpg"><source src="assets/video/grating-process.mp4" type="video/mp4"></video></div>
    <ol class="chapters">{chap}</ol>
  </div>
</section>

<section class="section" id="process">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">10 Steps</span><h2>제작 공정 10단계</h2><p>모든 제품은 고객의 도면에 맞춰 만들고, 출고 전까지 세 번 검사합니다. <span style="color:var(--red);font-weight:700">빨간 번호</span>가 검사 단계입니다.</p></div>
    <ol class="steps">{steps}</ol>
    <div class="photos" style="margin-top:40px">
      <figure><img src="assets/img/07-hole-shape-cutting.jpg" alt="개구부 형상 절단" loading="lazy"><figcaption>개구부 형상 절단</figcaption></figure>
      <figure><img src="assets/img/08-fit-up.jpg" alt="취부 작업" loading="lazy"><figcaption>취부</figcaption></figure>
      <figure><img src="assets/img/11-grinding.jpg" alt="사상 작업" loading="lazy"><figcaption>사상</figcaption></figure>
      <figure><img src="assets/img/16-bundle-packing.jpg" alt="출고 대기 중인 그레이팅 묶음" loading="lazy"><figcaption>포장·출고 대기</figcaption></figure>
    </div>
  </div>
</section>

<section class="section section-paper" id="quality">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">Quality</span><h2>품질관리</h2></div>
    <dl class="facts">
      <div><dt>치수 공차</dt><dd>미국 건축금속제조협회(NAAMM) 기준을 따릅니다.</dd></div>
      <div><dt>3단계 검사</dt><dd>제작 검사, 도금 검사, 최종 검사를 품질관리부가 맡고, 계측·시험 장비 31점으로 측정합니다.</dd></div>
      <div><dt>인증</dt><dd>ISO 9001(품질)·ISO 14001(환경), 인증범위 '그레이팅 및 철구조물의 제조', 2028년 5월 25일까지 유효</dd></div>
      <div><dt>자재 추적</dt><dd>제품마다 제작표시를 달고, 작업지시번호로 도면부터 출고까지 관리합니다.</dd></div>
    </dl>
  </div>
</section>

<section class="section" id="people">
  <div class="wrap split" style="align-items:start">
    <div style="display:grid;gap:20px">
      <span class="eyebrow">People</span>
      <h2 style="font-size:clamp(26px,3.2vw,38px)">압접기를 다루는 사람의<br>평균 경력 <span class="num" style="color:var(--red);font-size:1.25em">31</span>년</h2>
      <p class="prose">자동 압접기가 아무리 좋아도, 압연바와 전류의 차이를 읽는 것은 사람입니다. 준인산업 기계 압접부는 30년 넘게 그레이팅만 만들어 온 인력이 중심입니다.</p>
      <img src="assets/img/14-welding-shop-2.jpg" alt="용접 제작장에서 작업하는 모습" loading="lazy" style="width:100%;aspect-ratio:4/3;object-fit:cover">
    </div>
    <div class="table-scroll"><table class="tbl">
      <thead><tr><th>부서</th><th class="r">인원</th><th>맡는 일</th></tr></thead>
      <tbody>{team}</tbody>
    </table></div>
  </div>
</section>
''' + cta_band()
page('facility', '설비·생산능력', '자동 압접기 3기, 월 최대 1,000톤 규모. 주요 설비, 제작 공정 10단계, 품질관리, 압접 인력 평균 경력 31년.', facility)

# =====================================================================
# 실적
# =====================================================================
mix_max = max(float(r['납품량(톤)']) for r in MIX)
mix = ''.join(f'''<div class="row"><span>{esc("기타" if r["베어링 바 형식"].startswith("Dense") else r["베어링 바 형식"])}</span><div class="track"><div class="fill" style="width:{float(r["납품량(톤)"])/mix_max*100:.1f}%"></div></div><span class="val">{float(r["비중(%)"]):.0f}<small>%</small></span></div>''' for r in MIX)
CLIENTS = ['금성E&C','대우에스티','세방테크','승영기업','신안건업','약동산업','영신','영화엔지니어링','포스코플랜텍','한맥중공업']
clients = ''.join(f'<li>{esc(c)}</li>' for c in CLIENTS)
ptable = ''.join(f'<tr><td><span style="color:var(--red);font-weight:700;font-size:14px">{esc(r["분야"])}</span></td><th scope="row">{esc(r["프로젝트"].replace("(P3 P4 등)","(P3, P4 등)"))}</th><td>{esc(r["발주처"])}</td><td class="num" style="font-size:17px">{esc(r["시기"])}</td><td class="r num" style="font-size:18px">약 {int(r["납품량(톤)"]):,}</td></tr>' for r in PROJECTS)

projects = sub_hero('Track Record', '10년간 37,300톤, 350곳 이상의 고객사가 선택한 스틸 그레이팅', '2016년 4월부터 2026년 11월 초까지 6,205건의 작업을 납품했습니다. 석유화학 플랜트와 반도체 공장, 발전소, 데이터센터, 공항까지 산업 현장의 바닥과 통로를 준인산업이 만들었습니다.', '17-bundle-packing-2.jpg',
    '<div class="btns"><a class="btn btn-red" href="contact.html">견적 문의</a></div>') + stats([
    ('37,300<small>톤</small>', '10년간 누적 납품'),
    ('6,205<small>건</small>', '납품 작업'),
    ('350<small>곳+</small>', '거래 기업'),
    ('4,736<small>톤</small>', '2020년 한 해 납품량'),
]) + f'''
<section class="section">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">Annual Delivery</span><h2>2018년부터 해마다 3,000톤 넘게 납품합니다</h2>
      <p>월 최대 1,000톤 규모의 생산능력으로 대형 프로젝트가 겹치는 해에도 납기를 맞출 여유가 있습니다.</p></div>
    <div class="chart-box">
      <div class="chart-scroll">{annual_chart()}</div>
      <p class="note">납기일 기준. 2016년은 4월 설립 이후, 2026년은 11월 초 납기분까지(회색 막대). 10년 합계 약 37,300톤.</p>
    </div>
  </div>
</section>

<section class="section section-paper">
  <div class="wrap split" style="align-items:start">
    <div style="display:grid;gap:18px">
      <span class="eyebrow">Product Mix</span>
      <h2 style="font-size:clamp(26px,3.2vw,38px)">납품 제품 구성</h2>
      <p class="prose">같은 기간 납품량의 95%(약 35,400톤)가 그레이팅, 5%(약 1,950톤)가 계단 발판입니다. 베어링 바 형식으로는 I-Bar와 톱니 I-Bar가 70%를 차지합니다.</p>
    </div>
    <div class="chart-box">
      <span class="chart-title">베어링 바 형식별 납품 비중</span>
      <div class="bars-h">{mix}</div>
      <p class="note">2016.4~2026.11 초, 자재사양 기준</p>
    </div>
  </div>
</section>

<section class="section" id="key-projects">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">Key Projects</span><h2>분야별 대표 프로젝트</h2><p>준인산업 그레이팅은 철구조물 전문업체를 거쳐 아래 현장에 설치되었습니다. 200톤 이상 납품한 프로젝트입니다.</p></div>
    <div class="table-scroll"><table class="tbl tbl-wide">
      <thead><tr><th>분야</th><th>프로젝트</th><th>발주처</th><th>시기</th><th class="r">납품량(톤)</th></tr></thead>
      <tbody>{ptable}</tbody>
    </table></div>
    <div class="callout" style="margin-top:32px">
      <h3>해외 현장</h3>
      <p>2018년 베트남(DOOSAN VINA) 수출을 시작했고, 국내 EPC사를 통해 멕시코 PEMEX 플랜트에도 납품했습니다.</p>
    </div>
  </div>
</section>

<section class="section section-paper">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">Partners</span><h2>주요 거래처</h2><p>10년간 함께한 철구조물·플랜트 기업들입니다. (가나다순)</p></div>
    <ul class="clients">{clients}</ul>
  </div>
</section>
''' + cta_band()
page('projects', '실적', '2016년부터 10년간 37,300톤, 6,205건 납품. 연도별 납품량, 분야별 대표 프로젝트, 주요 거래처.', projects)

# =====================================================================
# 견적 문의
# =====================================================================
contact = f'''<section class="section-tight section-paper">
  <div class="wrap" style="display:grid;gap:14px">
    <span class="eyebrow">Contact</span>
    <h1 style="font-size:clamp(30px,4vw,46px)">견적 문의</h1>
    <p class="note" style="font-size:17px;max-width:40em">현장명과 규격, 수량을 알려주시면 담당자가 검토 후 연락드립니다. 도면이 있으면 메일로 함께 보내 주세요.</p>
  </div>
</section>
<section class="section">
  <div class="wrap contact-grid">
    <form class="form" id="quote-form" data-mailto="{EMAIL}" data-endpoint="" novalidate>
      <div class="field"><span class="lbl">문의 유형<span class="req">*</span></span>
        <div class="chips" role="radiogroup" aria-label="문의 유형">
          <label><input type="radio" name="type" id="type-quote" value="견적 요청" checked><span>견적 요청</span></label>
          <label><input type="radio" name="type" id="type-spec" value="규격·하중 상담"><span>규격·하중 상담</span></label>
          <label><input type="radio" name="type" id="type-etc" value="기타 문의"><span>기타 문의</span></label>
        </div>
      </div>
      <div class="row2">
        <div class="field"><label for="f-company">회사명<span class="req">*</span></label><input id="f-company" name="company" required autocomplete="organization"></div>
        <div class="field"><label for="f-name">담당자<span class="req">*</span></label><input id="f-name" name="name" required autocomplete="name"></div>
      </div>
      <div class="row2">
        <div class="field"><label for="f-phone">연락처<span class="req">*</span></label><input id="f-phone" name="phone" type="tel" required autocomplete="tel" placeholder="010-0000-0000"></div>
        <div class="field"><label for="f-email">이메일</label><input id="f-email" name="email" type="email" autocomplete="email"></div>
      </div>
      <div class="field"><label for="f-project">현장·프로젝트명</label><input id="f-project" name="project" placeholder="예: OO 플랜트 증설 2단계"></div>
      <div class="row2">
        <div class="field"><label for="f-spec">규격·수량</label><input id="f-spec" name="spec" placeholder="예: I-32 피치 30, 약 40톤"></div>
        <div class="field"><label for="f-due">납기 희망일</label><input id="f-due" name="due" type="date"></div>
      </div>
      <div class="field"><label for="f-message">문의 내용<span class="req">*</span></label><textarea id="f-message" name="message" required placeholder="스팬, 하중 조건, 끝 마감(엔드바형·컷엔드형), 계단 발판 여부 등을 적어 주세요."></textarea>
        <span class="hint">도면 파일은 {EMAIL} 로 보내 주세요.</span></div>
      <label class="agree"><input type="checkbox" id="f-agree" name="agree" required>
        <span>개인정보 수집·이용에 동의합니다. (필수)
          <details><summary>내용 보기</summary>수집 항목: 회사명, 담당자, 연락처, 이메일 · 목적: 견적 및 문의 응대 · 보관 기간: 문의 처리 후 1년</details>
        </span></label>
      <div><button class="btn btn-red" type="submit">문의 보내기</button></div>
      <div class="form-status" id="form-status" role="status" hidden></div>
    </form>
    <aside style="display:grid;gap:36px">
      <div><h2 style="font-size:20px;margin-bottom:14px">연락처</h2>
        <dl class="info-list">
          <div><dt>전화</dt><dd><a class="big" href="tel:{TEL.replace('-', '')}">{TEL}</a></dd></div>
          <div><dt>팩스</dt><dd class="big">{FAX}</dd></div>
          <div><dt>이메일</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd></div>
          <div><dt>주소</dt><dd style="font-weight:500">{ADDR_HQ}</dd></div>
        </dl></div>
      <div><h2 style="font-size:20px;margin-bottom:14px">자료실</h2>
        <a class="doc-card" href="assets/docs/junin-grating-spec-2026-10.pdf" target="_blank" rel="noopener"><span class="ext">PDF</span><div><strong>스틸 그레이팅 규격표</strong><span>기본 치수, 베어링 바, 단위중량, 계단 발판 · 2026.10</span></div></a>
        <a class="doc-card" style="margin-top:12px" href="assets/docs/junin-catalog.pdf" download><span class="ext">PDF</span><div><strong>회사 카탈로그 (Steel Grating DATA BOOK)</strong><span>제품 구조, 규격, 제작 공정 · 16쪽 · 3.3MB</span></div></a></div>
    </aside>
  </div>
</section>
'''
page('contact', '견적 문의', '(주)준인산업 견적 문의. TEL 031-351-3142, FAX 031-351-3149, hgkoo@juninmail.com', contact)
print('ok')
