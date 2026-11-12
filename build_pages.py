#!/usr/bin/env python3
"""Build herabio.tech sub-pages (strands + about) from index.html's shared head/style/defs/footer.
Run from repo root: python3 build_pages.py
"""
import re, pathlib
ROOT = pathlib.Path(__file__).parent / 'herabio.tech'
idx = (ROOT / 'index.html').read_text()

head_links = re.search(r'(<link rel="icon".*?</style>)', idx, re.S).group(1)
fonts = re.search(r'(<link rel="preconnect".*?rel="stylesheet">)', idx, re.S).group(1)
defs = re.search(r'(<svg width="0".*?</defs></svg>)', idx, re.S).group(1)
footer = re.search(r'(<footer>.*?</footer>)', idx, re.S).group(1)
import re as _re
footer_sub = _re.sub(r'Photos via Unsplash:.*?Midjourney\.', 'Sketches, prints and objects rendered with Midjourney.', footer, flags=_re.S)
footer_about = _re.sub(r'Photos via Unsplash:.*?Midjourney\.', 'Founder photo courtesy of Olivia Payne Anders.', footer, flags=_re.S)

NAV = [('index.html','HERA'),('saku.html','SAKU'),('hath.html','HATH'),('khandi.html','KHANDI'),('about.html','ABOUT')]

def topbar(current):
    links=''.join(f'<a href="{h}"{" aria-current=\"page\"" if h==current else ""}>{t}</a>' for h,t in NAV)
    return (f'<div class="topbar"><button class="burger" type="button" aria-label="Menu" aria-expanded="false" aria-controls="sitenav"><span></span><span></span><span></span></button><nav id="sitenav" aria-label="Site">{links}</nav>'
            '<a href="index.html" aria-label="Hera home"><svg class="lockup-of" viewBox="153 -459 8636 1893" role="img" aria-label="HERA"><use href="#heraLockupOF"/></svg></a></div>')

EXTRA_CSS = '''
/* sub-pages */
.topbar nav{display:flex;gap:22px;flex-wrap:wrap}
.topbar nav a{text-decoration:none;color:var(--paper-dim)}
.topbar nav a:hover,.topbar nav a[aria-current]{color:var(--paper)}
@media (max-width:640px){.topbar nav{gap:14px;font-size:11px}}
.shero{display:grid;grid-template-columns:minmax(0,6fr) minmax(0,6fr);gap:40px;align-items:center;min-height:min(70vh,700px)}
.shero .copy{display:flex;flex-direction:column;gap:14px}
.shero .kicker{font-weight:800;letter-spacing:4px;font-size:11px;color:var(--paper-dim)}
.shero h1{margin:0;font-family:var(--display);font-weight:400;font-size:clamp(48px,8vw,96px);letter-spacing:6px;line-height:1}
.shero .deity{display:flex;align-items:baseline;gap:12px;font-size:11px;letter-spacing:2px;color:var(--paper-dim)}
.shero .deity .glyph{font-size:22px;line-height:1;letter-spacing:0;color:var(--paper)}
.shero .deity .glyph.jp{font-family:var(--jp);font-weight:700}
.shero .deity .glyph.eg{font-family:'Noto Sans Egyptian Hieroglyphs',serif;font-size:26px}
.shero .deity .glyph.dv{font-family:'Noto Sans Devanagari',sans-serif;font-weight:600}
.shero .lore{font-style:italic;color:var(--paper-dim);max-width:60ch;margin:4px 0 0;border-top:1px solid rgba(238,237,232,.2);padding-top:12px}
.shero .desc{color:var(--paper);max-width:58ch;margin:0}
.shero .status{display:flex;align-items:center;gap:8px;font-size:11px;letter-spacing:2px;color:var(--paper-dim)}
.shero .status .dot{width:7px;height:7px;border-radius:50%;background:var(--acc);display:inline-block}
.sart{position:relative;aspect-ratio:1/1;width:clamp(380px,calc(100vh - 220px),100%);max-width:100%;margin-left:auto}
.sbar{height:150px;margin-top:-24px;background:var(--arch) center/cover;border:1px solid var(--paper)}
.sbar.in{display:none}
/* desktop: bar sits in the copy column, right above the strand name (Olli's bar-lab values: 47.6% wide ≈ column, 79px tall) */
@media (min-width:1025px){.sbar.top{display:none}.sbar.in{display:block;height:79px;margin:0 0 10px;width:100%}}
@media (prefers-reduced-motion:reduce){.sbar{background-image:var(--archs)}}
@media (min-width:641px) and (max-width:1024px){.sbar{height:120px;margin-top:-16px}}
@media (max-width:640px){.sbar{height:96px;margin-top:-12px}}
.sart .pr{position:absolute;right:0;top:0;width:52%;aspect-ratio:4/5;background:var(--print) center/cover;box-shadow:0 18px 40px rgba(0,0,0,.6);transform:rotate(2.5deg);z-index:1;border:6px solid var(--paper);border-bottom-width:28px}
.sart .obj{position:absolute;left:var(--ox);top:var(--oy);width:var(--ow);z-index:0;transform:rotate(var(--orot));transform-origin:50% 50%;filter:drop-shadow(0 14px 18px rgba(0,0,0,.7))}
.sart .obj img{display:block;width:100%;height:auto}
.sart .char{position:absolute;left:2%;bottom:2%;width:42%;z-index:2;background:var(--paper);padding:8px 8px 26px;box-shadow:0 22px 50px rgba(0,0,0,.75);transform:rotate(-3deg)}
.sart .char img{display:block;width:100%;height:auto;mix-blend-mode:multiply}
.sart .char .cap{position:absolute;left:10px;bottom:7px;font-size:9px;letter-spacing:2px;color:#555;white-space:nowrap}
.sart .tape{position:absolute;width:74px;height:20px;background:rgba(238,237,232,.85);box-shadow:0 1px 2px rgba(0,0,0,.4);z-index:3}
.sart .tape.k{background:#101010;opacity:.92;outline:1px solid rgba(238,237,232,.25)}
.roster{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px}
.roster .item{border:1px solid var(--paper);padding:22px 22px 20px;display:flex;flex-direction:column;gap:10px;background:var(--ink);min-width:0}
.roster .item.soon{border-style:dashed;color:var(--paper-dim)}
.roster .item .k{font-size:11px;letter-spacing:2.5px;font-weight:800;color:var(--paper-dim)}
.roster .item h3{margin:0;font-family:var(--display);font-weight:400;font-size:20px;letter-spacing:1px}
.roster .item p{margin:0;color:var(--paper-dim)}
.roster .item .status{display:flex;align-items:center;gap:8px;font-size:11px;letter-spacing:2px;color:var(--paper-dim);margin-top:auto}
.roster .item .status .dot{width:7px;height:7px;border-radius:50%;background:var(--acc);display:inline-block}
.roster .item a{color:var(--paper)}
.sec-head{display:flex;flex-direction:column;gap:8px;margin-bottom:-56px}
.sec-head h2{margin:0;font-family:var(--display);font-weight:400;font-size:clamp(22px,3vw,30px);letter-spacing:1px}
.sec-head p{margin:0;color:var(--paper-dim);max-width:62ch}
.cta{border:1px solid var(--paper);padding:26px 28px;display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:16px}
.cta p{margin:0;max-width:60ch;color:var(--paper-dim)}
.cta a.btn{display:inline-block;background:var(--paper);color:var(--ink);text-decoration:none;font-weight:800;letter-spacing:3px;font-size:12px;padding:12px 18px}
.about .founder{grid-template-columns:minmax(0,3fr) minmax(0,2fr);gap:40px;align-items:center}
.about .founder .fprint{max-width:190px;width:100%;margin:0 auto;justify-self:center;background:none;padding:0;box-shadow:0 22px 50px rgba(0,0,0,.75)}
.about .founder .fprint .cap{display:none}
.about .founder .txt p{max-width:72ch}
.about .founder{margin-top:48px}
.about .founder .txt{order:-1}
@media (min-width:641px) and (max-width:1024px){.shero{gap:28px;min-height:0}.sart{width:100%}.roster{grid-template-columns:repeat(2,minmax(0,1fr))}.about .founder{grid-template-columns:minmax(0,3fr) minmax(0,1fr)}}
@media (max-width:640px){.shero{grid-template-columns:1fr;min-height:0;margin-top:-20px}.sart{width:100%}.roster{grid-template-columns:1fr}.sec-head{margin-bottom:-40px}.about .founder{grid-template-columns:1fr}.about .founder .fprint{margin:8px auto 0;max-width:190px}}
'''

STRANDS = {
 'saku': dict(
   title='SAKU — Hera Biotech', kicker='PRENATAL STRAND', name='SAKU', glyph='木花咲耶姫', gcls='jp', lang='ja', full='KONOHANASAKUYA-HIME',
   acc='#A84F78', arch='img/strand_sakuya.gif', print='img/print_fuji.jpg', obj='img/obj_sprig.png', objw=643, objh=1100, ox='2%', oy='-10%', ow='40%', orot='-22deg', char='img/char_sakuya.jpg', cap='SAKUYA · SUBJECT 01', charw=552, charh=870,
   lore="Konohanasakuya-hime, goddess of Mount Fuji and the cherry blossom. Accused of carrying another man's children, she walked into fire to prove them true, and walked out holding them. The SAKU strand is nutrition for conception and pregnancy.",
   desc="Nutrition for conception and pregnancy: what the body needs before, and what it needs for the forty weeks. Every formula is built for absorption first, tested lot by lot, and published.",
   status='SAKUYA MATCHA · IN FORMULATION',
   items=[('PRODUCT · 01','Sakuya Matcha','A complete prenatal that works as a matcha latte. One scoop, frothed into warm or cold milk, every nutrient in a form that absorbs even in milk. <a href="shop.html">Pre-orders open soon.</a>','IN FORMULATION',False),
          ('DEVICES · 01','Fetal well-being at home','Ultrasound, non-stress tests and movement monitoring you can run yourself, between appointments and on your own schedule.','PLANNED',False),
          ('DEVICE · 02','Cholestasis home test','A bile-acid test you can take at home when the itching starts, with an answer in minutes rather than a week.','PLANNED',False)],
   research=[('Nutrient absorption.','How XX bodies take up iron, folate and choline, and which everyday foods block them.'),
             ('The placenta.','The least understood human organ. We want a way to read its function in a living pregnancy.'),
             ('Hyperemesis gravidarum prevention.','Now that GDF15 is on the table, stopping severe pregnancy sickness before it starts rather than managing it after.'),
             ('Fetal well-being monitoring.','What home ultrasound, NST and movement data can and cannot tell us, validated against the clinic.'),
             ('Intrahepatic cholestasis of pregnancy.','Fast bile-acid measurement outside the lab, and what it changes for stillbirth risk.')],
 ),
 'hath': dict(
   title='HATH — Hera Biotech', kicker='POSTPARTUM STRAND', name='HATH', glyph='𓉡', gcls='eg', lang='egy', full='HATHOR · ḤWT-ḤR',
   acc='#17746F', arch='img/strand_hathor.gif', print='img/print_dendera.jpg', obj='img/obj_sistrum.png', objw=411, objh=1100, ox='12%', oy='-14%', ow='28%', orot='14deg', char='img/char_hathor.jpg', cap='HATHOR · SUBJECT 02', charw=896, charh=1344,
   lore="Hathor, goddess of mothers, music and joy, horns around the sun. She nursed Horus and every king after him; at Dendera a birth house stands beside her temple. The HATH strand is recovery, feeding and the first year.",
   desc="Birth onward: recovery, feeding and the first year. A free tracker, a postnatal made for after (not a prenatal continued), and the hormone work nobody has done.",
   status='TRACKER IN BUILD',
   items=[('TOOL · 01','Tracker','A free app for the first year: feeds, sleep, recovery, the things you will be asked about and will not remember. Name to come.','IN BUILD',False),
          ('PRODUCT · 01','Postnatal','Made for after birth, measured directly rather than extrapolated from pregnancy.','PLANNING',False),
          ('RESEARCH','Hormones','Prolactin testing, hormone tracking and regulation, and D-MER support.','AGENDA',True)],
   research=[('Postnatal nutrition.','What the body needs after birth, measured directly rather than extrapolated from pregnancy.'),
             ('Lactation hormones.','Prolactin testing, hormone tracking and regulation, and D-MER (dysphoric milk ejection reflex), which almost no one has studied.')],
 ),
 'khandi': dict(
   title='KHANDI — Hera Biotech', kicker='XX MEN STRAND', name='KHANDI', glyph='शिखण्डी', gcls='dv', lang='sa', full='SHIKHANDI',
   acc='#2D327F', arch='img/strand_shikhandi.gif', print='img/print_forest.jpg', obj='img/obj_arrowhead.png', objw=332, objh=1000, ox='10%', oy='-8%', ow='26%', orot='-30deg', char='img/char_shikhandi.jpg', cap='SHIKHANDI · SUBJECT 03', charw=896, charh=1344,
   lore="Shikhandi, born a daughter of Panchala and raised a prince. When his bride's father learned the truth and marched on Panchala, Shikhandi went into the forest to die; there the yaksha Sthuna gave him his own male body in exchange for Shikhandi's. At Kurukshetra he led an army and brought down the unkillable Bhishma. The KHANDI strand is for XX men.",
   desc="Products and tools for XX men. Opens with a free tracker, then clinical products built around life on testosterone.",
   status='PLANNING',
   items=[('TOOL · 01','Tracker','A free app for life on T: doses, cycles, bloodwork, mood, the long record a clinic never keeps for you.','PLANNING',False),
          ('PRODUCT · 01','—','Clinical products built around life on testosterone. To be announced.','TBA',True),
          ('RESEARCH','Life on T','What changes, what needs care, what the data says once someone collects it.','AGENDA',True)],
   research=[('Life on testosterone.','The XX body on T: what changes, what needs care, what the data says once someone collects it.')],
 ),
}

def page(title, current, body, extra_style='', desc='', foot=None):
    foot = foot or footer_sub
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="https://herabio.tech/{current}">
{fonts}
{head_links}
<style>{EXTRA_CSS}{extra_style}</style>
</head>
<body>
{defs}

<div class="wrap" id="top">
  <span class="reg" style="left:-34px;top:30px"></span><span class="reg" style="right:-34px;top:30px"></span>
  {topbar(current)}
{body}
  {foot}
</div>
<script>(function(){{const b=document.querySelector('.burger');if(!b)return;b.addEventListener('click',()=>{{const o=b.closest('.topbar').classList.toggle('open');b.setAttribute('aria-expanded',o)}})}})();</script>
</body>
</html>
'''

for key, d in STRANDS.items():
    items=''.join(f'''    <div class="item{' soon' if soon else ''}"><div class="k">{k}</div><h3>{n}</h3><p>{t}</p><div class="status"><span class="dot"></span>{st}</div></div>\n''' for k,n,t,st,soon in d['items'])
    research=''.join(f'<li><b>{a}</b> {b}</li>' for a,b in d['research'])
    body=f'''
  <div class="sbar top" aria-hidden="true"></div>
  <section class="shero">
    <div class="copy">
      <div class="sbar in" aria-hidden="true"></div>
      <div class="kicker">{d['kicker']}</div>
      <h1>{d['name']}</h1>
      <div class="deity"><span class="glyph {d['gcls']}" lang="{d['lang']}">{d['glyph']}</span><span>{d['full']}</span></div>
      <p class="desc">{d['desc']}</p>
      <div class="status"><span class="dot"></span>{d['status']}</div>
      <p class="lore">{d['lore']}</p>
    </div>
    <div class="sart" aria-hidden="true">
      <div class="obj"><img src="{d['obj']}" alt="" width="{d['objw']}" height="{d['objh']}"></div>
      <div class="pr"></div>
      <div class="char"><span class="tape k" style="left:50%;top:-9px;transform:translateX(-50%) rotate(-3deg)"></span><img src="{d['char']}" alt="" width="{d['charw']}" height="{d['charh']}"><span class="cap">{d['cap']}</span></div>
    </div>
  </section>

  <div class="sec-head"><h2>In the strand</h2></div>
  <section class="roster">
{items}  </section>

  <section class="research" id="research">
    <div class="rfig c3" style="background-image:url(img/columns.jpg)"></div>
    <div class="rbody">
      <div class="kicker">RESEARCH · THIS STRAND</div>
      <h2>Open questions</h2>
      <ul>{research}</ul>
      <p class="partner">If you run a lab, clinic or cohort and want to work on any of these, write to <a href="mailto:olli@herabio.tech">olli@herabio.tech</a>.</p>
      <div class="status"><span class="dot"></span>AGENDA · SEEKING PARTNERS</div>
    </div>
  </section>

  <section class="cta">
    <p>Occasional email on formulation, launches and studies. No more than one or two a month.</p>
    <a class="btn" href="index.html#signup">FOLLOW THE BUILD</a>
  </section>
'''
    style=f':root{{--acc:{d["acc"]};--arch:url("{d["arch"]}");--archs:url("{d["arch"].replace(".gif",".jpg")}");--print:url("{d["print"]}")}} .sart .obj{{--ox:{d["ox"]};--oy:{d["oy"]};--ow:{d["ow"]};--orot:{d["orot"]}}} .cell .dot,.research .dot{{background:var(--acc)}}'
    (ROOT/f'{key}.html').write_text(page(d['title'], f'{key}.html', body, style, desc=d['desc']))

# ---------- about ----------
story = pathlib.Path('/tmp/claude-0/-home-claude/192c6e56-ae49-5ab3-a2ab-526c5a81bd6a/scratchpad/story.html').read_text()
founder = pathlib.Path('/tmp/claude-0/-home-claude/192c6e56-ae49-5ab3-a2ab-526c5a81bd6a/scratchpad/founder.html').read_text()
about_body = f'''
  <div class="about">
  <div class="sec-head" style="margin-bottom:0;margin-top:-40px"><h1 class="kicker" style="margin:0;font-family:var(--mono);font-weight:800;letter-spacing:4px;font-size:11px;color:var(--paper-dim)">ABOUT</h1></div>
  {story}
  {founder}
  </div>
  <section class="cta">
    <p>Occasional email on formulation, launches and studies. No more than one or two a month.</p>
    <a class="btn" href="index.html#signup">FOLLOW THE BUILD</a>
  </section>
'''
(ROOT/'about.html').write_text(page('About — Hera Biotech','about.html',about_body,desc='Why Hera Biotech exists, how we work, and the founder, Olivia Payne Anders. XX biosciences from Brooklyn.',foot=footer_about))
print('built', list(STRANDS)+['about'])
