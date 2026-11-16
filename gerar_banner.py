"""Gera banner.svg: visual de ciência de dados animado para o README do GitHub.
Rede de nós com pulsos de dados, gráfico de linha se desenhando, barras e dispersão.
Só usa CSS/SMIL dentro do SVG, que o GitHub renderiza quando o SVG é exibido como imagem."""
import math
import random
from pathlib import Path

random.seed(11)
W, H = 1000, 280
CY, MG, GR = "#22d3ee", "#a78bfa", "#22c55e"
parts = []

# Grade de fundo (papel milimetrado de gráfico)
for x in range(0, W, 40):
    parts.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{H}" class="grid"/>')
for y in range(0, H, 40):
    parts.append(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" class="grid"/>')

# Rede de nós à esquerda (grafo / pipeline de dados)
layers = [[(60, 70), (60, 140), (60, 210)],
          [(130, 50), (130, 110), (130, 170), (130, 230)],
          [(200, 90), (200, 190)]]
edges = []
for a, b in zip(layers, layers[1:]):
    for p in a:
        for q in b:
            edges.append((p, q))
for i, (p, q) in enumerate(edges):
    parts.append(f'<line x1="{p[0]}" y1="{p[1]}" x2="{q[0]}" y2="{q[1]}" class="edge"/>')
    if i % 2 == 0:
        dur = random.uniform(1.6, 3.2)
        parts.append(
            f'<circle r="2.5" fill="{CY}"><animateMotion dur="{dur:.1f}s" begin="-{random.uniform(0, dur):.1f}s" '
            f'repeatCount="indefinite" path="M{p[0]},{p[1]} L{q[0]},{q[1]}"/></circle>')
for layer in layers:
    for (x, y) in layer:
        parts.append(f'<circle cx="{x}" cy="{y}" r="7" class="node" style="animation-delay:-{random.uniform(0, 3):.1f}s"/>')

# Gráfico de linha à direita, desenhando-se
pts = []
v = 200
for i in range(16):
    v = max(70, min(230, v - random.uniform(-8, 22)))
    pts.append((790 + i * 12.5, v))
d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
area = d + f" L{pts[-1][0]:.1f},240 L{pts[0][0]:.1f},240 Z"
parts.append(f'<path d="{area}" fill="url(#area)" class="fadein"/>')
parts.append(f'<path d="{d}" class="line" pathLength="1"/>')
parts.append('<line x1="785" y1="240" x2="990" y2="240" class="axis"/><line x1="785" y1="60" x2="785" y2="240" class="axis"/>')

# Barras pulsando (histograma) embaixo da linha
for i in range(8):
    h = random.uniform(15, 45)
    parts.append(
        f'<rect x="{800 + i * 23}" y="{250 - h:.1f}" width="14" height="{h:.1f}" fill="{MG}" opacity=".0" class="bar" '
        f'style="animation-delay:-{i * 0.35:.2f}s; transform-origin:{807 + i * 23}px 250px"/>')

# Pontos de dispersão espalhados
for _ in range(26):
    x = random.choice([random.uniform(240, 330), random.uniform(680, 770)])
    y = random.uniform(30, 250)
    parts.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{random.choice([1.5, 2, 2.5])}" fill="{random.choice([CY, MG])}" '
                 f'class="dot" style="animation-delay:-{random.uniform(0, 4):.1f}s"/>')

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#05080f"/><stop offset="1" stop-color="#0b1424"/></linearGradient>
  <linearGradient id="area" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{CY}" stop-opacity=".35"/><stop offset="1" stop-color="{CY}" stop-opacity="0"/></linearGradient>
  <radialGradient id="glow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#05080f" stop-opacity=".9"/><stop offset="1" stop-color="#05080f" stop-opacity="0"/></radialGradient>
  <clipPath id="type"><rect x="0" y="0" height="{H}" width="0"><animate attributeName="width" values="0;{W};{W}" keyTimes="0;.35;1" dur="6s" repeatCount="indefinite"/></rect></clipPath>
</defs>
<style>
  .grid {{ stroke: #1e293b; stroke-width: 1; opacity: .55; }}
  .edge {{ stroke: {CY}; stroke-opacity: .18; }}
  .node {{ fill: #0b1424; stroke: {CY}; stroke-width: 2; animation: pulse 3s ease-in-out infinite; }}
  .axis {{ stroke: #475569; }}
  .line {{ fill: none; stroke: {CY}; stroke-width: 2.5; stroke-dasharray: 1; stroke-dashoffset: 1; animation: draw 6s ease-in-out infinite; }}
  @keyframes draw {{ 0% {{ stroke-dashoffset: 1; }} 45%, 85% {{ stroke-dashoffset: 0; }} 100% {{ stroke-dashoffset: 0; opacity: 0; }} }}
  .fadein {{ animation: fade 6s ease-in-out infinite; }}
  @keyframes fade {{ 0%, 30% {{ opacity: 0; }} 50%, 85% {{ opacity: 1; }} 100% {{ opacity: 0; }} }}
  .bar {{ animation: bar 2.8s ease-in-out infinite; }}
  @keyframes bar {{ 0%, 100% {{ transform: scaleY(.4); opacity: .25; }} 50% {{ transform: scaleY(1); opacity: .6; }} }}
  .dot {{ animation: pulse 4s ease-in-out infinite; }}
  @keyframes pulse {{ 50% {{ opacity: .25; }} }}
  .name {{ font: 700 44px Consolas, 'Courier New', monospace; fill: #e6f6ff; letter-spacing: 8px; }}
  .sub {{ font: 18px Consolas, 'Courier New', monospace; fill: {CY}; }}
  .tag {{ font: 13px Consolas, 'Courier New', monospace; fill: #94a3b8; letter-spacing: 2px; }}
  .blink {{ animation: blink 1s steps(1) infinite; }}
  @keyframes blink {{ 50% {{ opacity: 0; }} }}
</style>
<rect width="{W}" height="{H}" rx="14" fill="url(#bg)"/>
{"".join(parts)}
<ellipse cx="{W/2}" cy="{H/2}" rx="330" ry="100" fill="url(#glow)"/>
<text class="name" x="{W/2}" y="125" text-anchor="middle">SIDNEI RODRIGUES</text>
<g clip-path="url(#type)"><text class="sub" x="{W/2}" y="165" text-anchor="middle">&gt; designer gráfico → desenvolvedor de soluções_</text></g>
<text class="tag" x="{W/2}" y="205" text-anchor="middle">AUTOMAÇÃO  ·  IA LOCAL  ·  CIÊNCIA DE DADOS</text>
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="none" stroke="{CY}" stroke-opacity=".35"/>
<circle class="blink" cx="30" cy="30" r="5" fill="{GR}"/>
<text class="tag" x="44" y="34">ONLINE</text>
</svg>'''
Path(__file__).with_name("banner.svg").write_text(svg, encoding="utf-8")
print("ok", len(svg))
