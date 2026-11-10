import subprocess, os, sys
S, P = sys.argv[1], sys.argv[2]
dur = {l.split()[0]: float(l.split()[2]) for l in open(f"{S}/durs.txt")}
scenes = [("hook","h1 h2"),("maya","m1 m2 m3 m4"),("jake","j1 j2 j3 j4"),("ask","a1 a2 a3"),("race","r1 r2 r3 r4 r5"),("payoff","p1 p2"),("why","w1 w2 w3"),("end","e1 e2 e3")]
INTRA, GAP, LEAD, TAIL = 0.25, 0.45, 0.25, 1.4
t = LEAD; st = {}; sstart = {}; order = []
for i,(sc,ids) in enumerate(scenes):
    ids = ids.split()
    sstart[sc] = 0.0 if i == 0 else round(t - 0.2, 3)
    for k,pid in enumerate(ids):
        st[pid] = t; order.append(pid); t += dur[pid] + (INTRA if k < len(ids)-1 else GAP)
T = round(t - GAP + TAIL, 2)
names = [s for s,_ in scenes]
sdur = {s: round((sstart[names[i+1]] if i+1 < len(names) else T) - sstart[s], 3) for i,s in enumerate(names)}
def L(pid, off=0.0):
    sc = next(s for s,ids in scenes if pid in ids.split())
    return round(st[pid] - sstart[sc] + off, 3)
# voice track
os.makedirs(f"{P}/assets", exist_ok=True)
ins = []; fl = []
for i,pid in enumerate(order):
    ins += ["-i", f"{S}/vt/{pid}.wav"]; fl.append(f"[{i}]adelay={int(st[pid]*1000)}[a{i}]")
fc = ";".join(fl) + ";" + "".join(f"[a{i}]" for i in range(len(order))) + f"amix=inputs={len(order)}:normalize=0,apad=whole_dur={T},loudnorm=I=-15:TP=-1.5:LRA=11[o]"
subprocess.run(["ffmpeg","-v","error","-y",*ins,"-filter_complex",fc,"-map","[o]","-ar","48000","-ac","1",f"{P}/assets/voice.wav"],check=True)

FONT = '"Archivo Black", sans-serif'; INTER = '"Inter", sans-serif'
W = 'data-width="1080" data-height="1920"'
def clip(d): return f'class="clip" data-start="0" data-duration="{d}"'
def wipe(sel, at, d=0.3): return f'tl.fromTo("{sel}", {{ clipPath: "inset(0% 100% 0% 0%)" }}, {{ clipPath: "inset(0% 0% 0% 0%)", duration: {d}, ease: "power3.out" }}, {at});'
def wipeR(sel, at, d=0.3): return f'tl.fromTo("{sel}", {{ clipPath: "inset(0% 0% 0% 100%)" }}, {{ clipPath: "inset(0% 0% 0% 0%)", duration: {d}, ease: "power3.out" }}, {at});'
def scene(name, css, html, js):
    d = sdur[name]
    open(f"{P}/compositions/{name}.html","w",encoding="utf-8").write(f'''<template>
  <style>
    #root {{ position: absolute; inset: 0; background: #ffd21f; font-family: {FONT}; color: #121212; }}
{css}
  </style>
  <div id="root" data-composition-id="{name}" {W}>
{html}
  </div>
  <script>
    {{
      const tl = gsap.timeline({{ paused: true }});
{js}
      tl.to({{}}, {{ duration: 0.01 }}, {round(d-0.02,3)});
      window.__timelines["{name}"] = tl;
    }}
  </script>
</template>
''')

# hook
d = sdur["hook"]; c = clip(d)
scene("hook", f'''    #hook-title {{ position: absolute; left: 90px; top: 250px; width: 900px; font-size: 150px; line-height: 0.96; letter-spacing: -0.02em; }}
    #hook-title span {{ display: block; }}
    #hook-bar {{ position: absolute; left: 90px; top: 730px; width: 820px; height: 26px; background: #121212; }}
    .hook-tag {{ position: absolute; top: 860px; width: 430px; height: 330px; color: #fff; }}
    .hook-tag b {{ font-size: 104px; font-weight: 400; line-height: 1; }}
    .hook-tag i {{ font-family: {INTER}; font-style: normal; font-weight: 700; font-size: 44px; margin-top: 16px; }}
    #hook-maya {{ left: 90px; }} #hook-jake {{ left: 550px; }}
    .hook-in {{ position: absolute; inset: 0; display: flex; flex-direction: column; justify-content: center; padding-left: 40px; }}
    #hook-maya-in {{ background: #0b7a3e; }} #hook-jake-in {{ background: #e8452c; }}''',
f'''    <h1 id="hook-title" {c}><span>WER GEHT</span><span>REICHER</span><span>IN RENTE?</span></h1>
    <div id="hook-barclip" {c}><div id="hook-bar"></div></div>
    <div id="hook-maya" {c.replace('class="clip"','class="clip hook-tag"')}><div id="hook-maya-in" class="hook-in"><b>LENA</b><i>spart 10 Jahre</i></div></div>
    <div id="hook-jake" {c.replace('class="clip"','class="clip hook-tag"')}><div id="hook-jake-in" class="hook-in"><b>TOM</b><i>spart 30 Jahre</i></div></div>''',
f'''      tl.fromTo("#hook-bar", {{ scaleX: 0.12, transformOrigin: "0 50%" }}, {{ scaleX: 1, duration: 0.5, ease: "power4.out" }}, 0.05);
      tl.fromTo("#hook-maya-in", {{ scale: 1.5, rotation: -8, opacity: 0 }}, {{ scale: 1, rotation: -2, opacity: 1, duration: 0.28, ease: "back.out(2)" }}, {L("h2",0.7)});
      tl.fromTo("#hook-jake-in", {{ scale: 1.5, rotation: 8, opacity: 0 }}, {{ scale: 1, rotation: 2, opacity: 1, duration: 0.28, ease: "back.out(2)" }}, {L("h2",1.15)});''')

def person(n, color, align, NAME, origin, l1c, l2, l3, total, r0, r1, t1, t2, t3, ts, wp):
    d = sdur[n]; c = lambda extra="": clip(d).replace('class="clip"', f'class="clip {extra}"'.replace(' "','"'))
    scene(n, f'''    #{n}-field {{ position: absolute; inset: 0; background: {color}; }}
    .{n}-l {{ position: absolute; left: 90px; width: 900px; text-align: {align}; color: #fff; }}
    #{n}-name {{ top: 220px; font-size: 250px; line-height: 1; letter-spacing: -0.02em; }}
    #{n}-l1 {{ top: 525px; font-size: 90px; color: {l1c}; }}
    #{n}-l2 {{ top: 670px; font-family: {INTER}; font-weight: 900; font-size: 78px; }}
    #{n}-l3 {{ top: 780px; font-family: {INTER}; font-weight: 900; font-size: 78px; }}
    #{n}-stamp {{ position: absolute; left: 90px; top: 990px; width: 800px; height: 250px; }}
    #{n}-stamp-in {{ position: absolute; inset: 0; background: #ffd21f; color: #121212; display: flex; flex-direction: column; justify-content: center; padding-left: 44px; }}
    #{n}-stamp-in i {{ font-family: {INTER}; font-style: normal; font-weight: 900; font-size: 48px; }}
    #{n}-stamp-in b {{ font-weight: 400; font-size: 124px; line-height: 1.05; }}''',
f'''    <div id="{n}-fieldclip" {clip(d)}><div id="{n}-field"></div></div>
    <div id="{n}-name" {c(n+"-l")}><div id="{n}-name-in">{NAME}</div></div>
    <div id="{n}-l1" {c(n+"-l")}><div id="{n}-l1-in">200 € im Monat</div></div>
    <div id="{n}-l2" {c(n+"-l")}><div id="{n}-l2-in">{l2}</div></div>
    <div id="{n}-l3" {c(n+"-l")}><div id="{n}-l3-in">{l3}</div></div>
    <div id="{n}-stamp" {clip(d)}><div id="{n}-stamp-in"><i>INSGESAMT EINGEZAHLT</i><b>{total}</b></div></div>''',
f'''      tl.fromTo("#{n}-field", {{ scaleY: 0, transformOrigin: "{origin}" }}, {{ scaleY: 1, duration: 0.32, ease: "power4.out" }}, 0);
      tl.fromTo("#{n}-name-in", {{ scale: 1.35, opacity: 0, transformOrigin: "{align} 50%" }}, {{ scale: 1, opacity: 1, duration: 0.24, ease: "power4.out" }}, 0.14);
      {wp(f"#{n}-l1-in", t1)}
      {wp(f"#{n}-l2-in", t2)}
      {wp(f"#{n}-l3-in", t3)}
      tl.fromTo("#{n}-stamp-in", {{ scale: 1.6, rotation: {r0}, opacity: 0 }}, {{ scale: 1, rotation: {r1}, opacity: 1, duration: 0.22, ease: "back.out(1.6)" }}, {ts});''')
person("maya","#0b7a3e","left","LENA","50% 0%","#ffd21f","von 25 bis 35","dann Schluss.","24.000 €",-9,-3,L("m2",0.5),L("m2",1.6),L("m3",0.45),L("m4",0.15),wipe)
person("jake","#e8452c","right","TOM","50% 100%","#121212","von 35 bis 65","ohne Pause.","72.000 €",9,3,L("j2",2.6),L("j2",0.6),L("j3",1.0),L("j4",0.1),wipeR)

# ask
d = sdur["ask"]; c = clip(d).replace('class="clip"','class="clip ask-l"')
scene("ask", f'''    .ask-l {{ position: absolute; left: 90px; width: 900px; }}
    #ask-a {{ top: 230px; font-size: 96px; }}
    #ask-b {{ top: 330px; font-size: 300px; line-height: 1; letter-spacing: -0.03em; color: #e8452c; }}
    #ask-c {{ top: 630px; font-size: 80px; }}
    #ask-q {{ top: 840px; height: 330px; width: 860px; }}
    #ask-q-in {{ position: absolute; inset: 0; background: #121212; color: #fff; display: flex; flex-direction: column; justify-content: center; padding-left: 44px; font-size: 80px; line-height: 1.1; }}
    #ask-q-in span {{ color: #ffd21f; }}
    #ask-g {{ top: 1215px; font-size: 60px; }}''',
f'''    <div id="ask-a" {c}><div id="ask-a-in">TOM HAT</div></div>
    <div id="ask-b" {c}><div id="ask-b-in">3×</div></div>
    <div id="ask-c" {c}><div id="ask-c-in">MEHR EINGEZAHLT</div></div>
    <div id="ask-q" {c}><div id="ask-q-in"><div>TOM GEWINNT…</div><span>ODER?</span></div></div>
    <div id="ask-g" {c}><div id="ask-g-in">SCHREIB DEINEN TIPP</div></div>''',
f'''      {wipe("#ask-a-in", L("a1",0.1), 0.25)}
      tl.fromTo("#ask-b-in", {{ scale: 2.2, opacity: 0, transformOrigin: "0% 50%" }}, {{ scale: 1, opacity: 1, duration: 0.26, ease: "power4.out" }}, {L("a1",0.95)});
      {wipe("#ask-c-in", L("a1",1.35), 0.25)}
      tl.fromTo("#ask-q-in", {{ scaleX: 0, transformOrigin: "0% 50%" }}, {{ scaleX: 1, duration: 0.3, ease: "power4.out" }}, {L("a2",-0.05)});
      tl.fromTo("#ask-q-in span", {{ opacity: 0, scale: 1.4, transformOrigin: "0% 50%" }}, {{ opacity: 1, scale: 1, duration: 0.2, ease: "back.out(2)" }}, {L("a2",0.75)});
      {wipe("#ask-g-in", L("a3",0.35), 0.3)}''')

# race
d = sdur["race"]; c = clip(d)
g1s, g1d = L("r2"), round(dur["r2"]+0.3,3)
g2s = L("r3",1.7); g2e = L("r5", dur["r5"]-0.2); g2d = round(g2e-g2s,3)
open(f"{P}/compositions/race.html","w",encoding="utf-8").write(f'''<template>
  <style>
    #root {{ position: absolute; inset: 0; background: #ffd21f; font-family: {FONT}; color: #121212; }}
    #race-age {{ position: absolute; left: 90px; top: 200px; width: 900px; font-size: 190px; line-height: 1; letter-spacing: -0.02em; }}
    #race-age small {{ font-size: 80px; margin-right: 24px; }}
    #race-base {{ position: absolute; left: 60px; top: 1160px; width: 960px; height: 12px; background: #121212; }}
    .race-col {{ position: absolute; top: 540px; width: 400px; height: 620px; }}
    #race-mcol {{ left: 110px; }} #race-jcol {{ left: 570px; }}
    .race-fill {{ position: absolute; inset: 0; }}
    #race-mfill {{ background: #0b7a3e; }} #race-jfill {{ background: #e8452c; }}
    .race-val {{ position: absolute; left: -20px; width: 440px; top: 540px; text-align: center; font-size: 74px; line-height: 1; }}
    .race-name {{ position: absolute; top: 1184px; width: 400px; text-align: center; font-size: 64px; line-height: 1; }}
    #race-mname {{ left: 110px; }} #race-jname {{ left: 570px; }}
    .race-note {{ position: absolute; top: 1264px; width: 400px; text-align: center; font-family: {INTER}; font-weight: 900; font-size: 34px; }}
    #race-mnote {{ left: 110px; }} #race-jnote {{ left: 570px; }}
    #race-fine {{ position: absolute; left: 90px; top: 392px; width: 900px; font-family: {INTER}; font-weight: 700; font-size: 32px; }}
  </style>
  <div id="root" data-composition-id="race" {W}>
    <div id="race-age" {c}><small>ALTER</small><span id="race-age-n">25</span></div>
    <div id="race-fine" {c}>Beispiel: beide 7 % Rendite pro Jahr</div>
    <div id="race-mcol" {c.replace('class="clip"','class="clip race-col"')} data-layout-allow-overflow>
      <div id="race-mfill" class="race-fill"></div>
      <div id="race-mval" class="race-val">0 €</div>
    </div>
    <div id="race-jcol" {c.replace('class="clip"','class="clip race-col"')} data-layout-allow-overflow>
      <div id="race-jfill" class="race-fill"></div>
      <div id="race-jval" class="race-val">0 €</div>
    </div>
    <div id="race-mname" {c.replace('class="clip"','class="clip race-name"')}>LENA</div>
    <div id="race-jname" {c.replace('class="clip"','class="clip race-name"')}>TOM</div>
    <div id="race-baseclip" {c}><div id="race-base"></div></div>
    <div id="race-mnote" {c.replace('class="clip"','class="clip race-note"')}><div id="race-mnote-in">STOPP MIT 35</div></div>
    <div id="race-jnote" {c.replace('class="clip"','class="clip race-note"')}><div id="race-jnote-in">START MIT 35</div></div>
  </div>
  <script>
    {{
      const r = 0.07 / 12, H = 620, MAX = 281000;
      const maya = (m) => ((200 * (Math.pow(1 + r, Math.min(m, 120)) - 1)) / r) * Math.pow(1 + r, Math.max(0, m - 120));
      const jake = (m) => (200 * (Math.pow(1 + r, Math.max(0, m - 120)) - 1)) / r;
      const fmt = (v) => String(Math.round(v)).replace(/\\B(?=(\\d{{3}})+(?!\\d))/g, ".") + " €";
      const q = (s) => document.querySelector(s);
      const p = {{ m: 0 }};
      const draw = () => {{
        const mv = maya(p.m), jv = jake(p.m);
        const ms = Math.max(0.004, mv / MAX), js = Math.max(0.004, jv / MAX);
        gsap.set("#race-mfill", {{ scaleY: ms, transformOrigin: "50% 100%" }});
        gsap.set("#race-jfill", {{ scaleY: js, transformOrigin: "50% 100%" }});
        gsap.set("#race-mval", {{ y: -H * ms - 4 }});
        gsap.set("#race-jval", {{ y: -H * js - 4 }});
        const done = p.m >= 479.5;
        q("#race-mval").textContent = fmt(done ? mv : Math.round(mv / 100) * 100);
        q("#race-jval").textContent = fmt(done ? jv : Math.round(jv / 100) * 100);
        q("#race-age-n").textContent = String(Math.floor(25 + p.m / 12 + 1e-6));
      }};
      const tl = gsap.timeline({{ paused: true }});
      tl.fromTo("#race-base", {{ scaleX: 0, transformOrigin: "0% 50%" }}, {{ scaleX: 1, duration: 0.3, ease: "power4.out" }}, 0);
      tl.fromTo(p, {{ m: 0 }}, {{ m: 120, duration: {g1d}, ease: "none", onUpdate: draw }}, {g1s});
      tl.fromTo(p, {{ m: 120 }}, {{ m: 480, duration: {g2d}, ease: "power1.in", onUpdate: draw, immediateRender: false }}, {g2s});
      tl.fromTo("#race-mnote-in", {{ opacity: 0, scale: 1.5 }}, {{ opacity: 1, scale: 1, duration: 0.2, ease: "back.out(2)" }}, {L("r3",0.5)});
      tl.fromTo("#race-jnote-in", {{ opacity: 0, scale: 1.5 }}, {{ opacity: 1, scale: 1, duration: 0.2, ease: "back.out(2)" }}, {L("r3",1.5)});
      tl.fromTo("#race-mval", {{ scale: 1 }}, {{ scale: 1.18, duration: 0.16, ease: "power2.out", yoyo: true, repeat: 1, transformOrigin: "50% 100%" }}, {round(g2e+0.05,3)});
      tl.to({{}}, {{ duration: 0.01 }}, {round(d-0.02,3)});
      draw();
      window.__timelines["race"] = tl;
    }}
  </script>
</template>
''')

# payoff
d = sdur["payoff"]; c = clip(d).replace('class="clip"','class="clip pay-l"')
scene("payoff", f'''    #pay-field {{ position: absolute; inset: 0; background: #0b7a3e; }}
    .pay-l {{ position: absolute; left: 90px; width: 900px; color: #fff; }}
    #pay-win {{ top: 220px; font-size: 170px; line-height: 0.95; letter-spacing: -0.02em; }}
    #pay-m {{ top: 620px; font-family: {INTER}; font-weight: 900; font-size: 60px; line-height: 1.25; }}
    #pay-m b {{ font-family: {FONT}; font-weight: 400; font-size: 136px; color: #ffd21f; display: block; line-height: 1.05; }}
    #pay-j {{ top: 960px; font-family: {INTER}; font-weight: 700; font-size: 46px; line-height: 1.3; }}''',
f'''    <div id="pay-fieldclip" {clip(d)}><div id="pay-field"></div></div>
    <div id="pay-win" {c}><div id="pay-win-in">LENA<br />GEWINNT</div></div>
    <div id="pay-m" {c}><div id="pay-m-in">Aus 24.000 € wurden<b>280.968 €</b></div></div>
    <div id="pay-j" {c}><div id="pay-j-in">Tom: aus 72.000 € wurden 243.994 €</div></div>''',
f'''      tl.fromTo("#pay-field", {{ scaleY: 0, transformOrigin: "50% 100%" }}, {{ scaleY: 1, duration: 0.3, ease: "power4.out" }}, 0);
      tl.fromTo("#pay-win-in", {{ scale: 1.6, opacity: 0, transformOrigin: "0% 50%" }}, {{ scale: 1, opacity: 1, duration: 0.26, ease: "power4.out" }}, 0.15);
      {wipe("#pay-m-in", L("p1",1.1), 0.35)}
      {wipe("#pay-j-in", L("p2",0.1), 0.35)}''')

# why
d = sdur["why"]; c = clip(d).replace('class="clip"','class="clip why-l"')
scene("why", f'''    .why-l {{ position: absolute; left: 90px; width: 900px; }}
    #why-q {{ top: 220px; font-size: 172px; line-height: 1; letter-spacing: -0.03em; color: #e8452c; }}
    #why-y {{ top: 470px; font-size: 140px; line-height: 0.95; letter-spacing: -0.02em; color: #0b7a3e; }}
    #why-y small {{ display: block; font-size: 84px; color: #121212; margin-top: 14px; letter-spacing: 0; }}
    #why-b {{ top: 980px; width: 860px; height: 280px; }}
    #why-b-in {{ position: absolute; inset: 0; background: #121212; color: #ffd21f; display: flex; flex-direction: column; justify-content: center; padding-left: 44px; font-family: {INTER}; font-weight: 900; font-size: 54px; line-height: 1.15; }}
    #why-b-in b {{ font-family: {FONT}; font-weight: 400; font-size: 124px; color: #fff; line-height: 1.05; }}''',
f'''    <div id="why-q" {c}><div id="why-q-in">WARUM?</div></div>
    <div id="why-y" {c}><div id="why-y-in">10 JAHRE<br />MEHR ZEIT<small>ZUM WACHSEN</small></div></div>
    <div id="why-b" {c}><div id="why-b-in"><div>mehr wert als Toms extra</div><b>48.000 €</b></div></div>''',
f'''      tl.fromTo("#why-q-in", {{ scale: 1.5, opacity: 0, transformOrigin: "0% 50%" }}, {{ scale: 1, opacity: 1, duration: 0.24, ease: "back.out(1.8)" }}, {L("w1",-0.05)});
      {wipe("#why-y-in", L("w2",0.55), 0.4)}
      tl.fromTo("#why-b-in", {{ scaleX: 0, transformOrigin: "0% 50%" }}, {{ scaleX: 1, duration: 0.3, ease: "power4.out" }}, {L("w3",1.3)});
      tl.fromTo("#why-b-in b", {{ scale: 1, transformOrigin: "0% 50%" }}, {{ scale: 1.12, duration: 0.18, ease: "power2.out", yoyo: true, repeat: 1 }}, {L("w3",3.3)});''')

# end
d = sdur["end"]; c = clip(d).replace('class="clip"','class="clip end-l"')
scene("end", f'''    .end-l {{ position: absolute; left: 90px; width: 900px; }}
    #end-claim {{ top: 220px; font-size: 170px; line-height: 0.95; letter-spacing: -0.02em; }}
    #end-claim span {{ display: block; }}
    #end-cta {{ top: 800px; width: 840px; height: 250px; }}
    #end-cta-in {{ position: absolute; inset: 0; background: #121212; color: #fff; display: flex; flex-direction: column; justify-content: center; padding-left: 44px; font-size: 74px; line-height: 1.15; }}
    #end-cta-in span {{ color: #ffd21f; font-size: 46px; }}
    #end-fine {{ top: 1100px; width: 820px; font-family: {INTER}; font-weight: 700; font-size: 30px; line-height: 1.35; }}''',
f'''    <div id="end-claim" {c}><span id="end-c1">ZEIT</span><span id="end-c2">SCHLÄGT</span><span id="end-c3">GELD</span></div>
    <div id="end-cta" {c}><div id="end-cta-in"><div>FRÜH ANFANGEN</div><span>Folge für mehr Geldwissen</span></div></div>
    <div id="end-fine" {c}><div id="end-fine-in">Nur ein Beispiel: 7 % Rendite pro Jahr angenommen. Keine Anlageberatung.</div></div>''',
f'''      tl.fromTo("#end-c1", {{ opacity: 0, x: -120 }}, {{ opacity: 1, x: 0, duration: 0.2, ease: "power4.out" }}, {L("e1",-0.05)});
      tl.fromTo("#end-c2", {{ opacity: 0, x: -120 }}, {{ opacity: 1, x: 0, duration: 0.2, ease: "power4.out" }}, {L("e1",0.3)});
      tl.fromTo("#end-c3", {{ opacity: 0, x: -120 }}, {{ opacity: 1, x: 0, duration: 0.2, ease: "power4.out" }}, {L("e1",0.6)});
      tl.fromTo("#end-cta-in", {{ scaleX: 0, transformOrigin: "0% 50%" }}, {{ scaleX: 1, duration: 0.3, ease: "power4.out" }}, {L("e2",0.1)});
      tl.fromTo("#end-cta-in span", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2, ease: "power2.out" }}, {L("e3")});
      tl.fromTo("#end-fine-in", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.25, ease: "power2.out" }}, {L("e2",0.4)});''')

hosts = "\n".join(f'      <div id="{s}" data-composition-id="{s}" data-composition-src="compositions/{s}.html" data-start="{sstart[s]}" data-duration="{sdur[s]}" data-track-index="1" data-track-kind="graphics" {W}></div>' for s in names)
idx = open(f"{P}/index.html").read()
head = idx[:idx.index('    <div id="root"')]
open(f"{P}/index.html","w",encoding="utf-8").write(head + f'''    <div id="root" data-composition-id="main" data-start="0" data-duration="{T}" {W}>
{hosts}
      <audio id="vo" class="clip" src="assets/voice.wav" data-start="0" data-duration="{T}" data-track-index="2" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
''')
print("T", T); [print(s, sstart[s], sdur[s]) for s in names]
