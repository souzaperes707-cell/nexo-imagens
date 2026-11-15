#!/usr/bin/env python3
"""PUBLICADOR NA NUVEM do NEXO - V1 (14/11/2026)

Prepara UM carrossel para uma data e deixa as imagens prontas para subir ao GitHub.
Uso:  python3 robo/preparar-post.py AAAA-MM-DD [id-da-pauta]
  - escolhe a proxima pauta livre do capitulo do mes (nov/2026 = cap. 1, dez = cap. 2 ...)
  - escolhe a base pelo dia da semana (rodizio)
  - gera tela-1..4.jpg em AAAA-MM/<id>/
  - marca a pauta como usada em robo/pautas.json
  - imprime um JSON com: id, pasta, media (links raw do GitHub), legenda, tiktok
Depois: git add/commit/push e agendar no Metricool com os links de "media".
"""
import json, os, subprocess, sys, datetime, glob, shutil
from PIL import Image

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROBO = os.path.join(RAIZ, "robo")
PAUTAS = os.path.join(ROBO, "pautas.json")
RAW = "https://raw.githubusercontent.com/souzaperes707-cell/nexo-imagens/main"
RODIZIO = ["branca", "preta", "viva", "branca", "cinema", "viva", "preta"]  # seg..dom (weekday 0=seg)

data = sys.argv[1]
forcar = sys.argv[2] if len(sys.argv) > 2 else None
d = datetime.date.fromisoformat(data)
cap = (d.year - 2026) * 12 + d.month - 10  # nov/2026 = 1

pautas = json.load(open(PAUTAS, encoding="utf8"))
if forcar:
    pauta = next(p for p in pautas if p["id"] == forcar)
else:
    pauta = next((p for p in pautas if not p.get("usada") and int(p.get("capitulo", 1)) == cap), None) \
        or next((p for p in pautas if not p.get("usada")), None)
if not pauta:
    print(json.dumps({"erro": "ESTOQUE VAZIO: escreva pautas novas em robo/pautas.json"}))
    sys.exit(2)
base = RODIZIO[d.weekday()]

tmp = os.path.join("/tmp", "nexo-render")
shutil.rmtree(tmp, ignore_errors=True)
os.makedirs(tmp)
shutil.copy(os.path.join(ROBO, "gerar-carrossel.js"), tmp)
json.dump(pautas, open(os.path.join(tmp, "pautas.json"), "w", encoding="utf8"), ensure_ascii=False)
env = dict(os.environ, ROBO_CHROME="nao")
r = subprocess.run(["node", "gerar-carrossel.js", base, pauta["id"]], cwd=tmp, env=env, capture_output=True, text=True, timeout=180)
saidas = glob.glob(os.path.join(tmp, "saida", "*"))
if not saidas or not os.path.exists(os.path.join(saidas[0], "tela-4.png")):
    print(json.dumps({"erro": "falha ao gerar imagens", "log": (r.stdout + r.stderr)[-800:]}))
    sys.exit(3)

pasta_rel = f"{data[:7]}/{pauta['id']}"
pasta = os.path.join(RAIZ, pasta_rel)
os.makedirs(pasta, exist_ok=True)
for n in range(1, 5):
    Image.open(os.path.join(saidas[0], f"tela-{n}.png")).convert("RGB").save(os.path.join(pasta, f"tela-{n}.jpg"), quality=90)

pauta["usada"] = True
pauta["usadaEm"] = data
json.dump(pautas, open(PAUTAS, "w", encoding="utf8"), ensure_ascii=False, indent=1)

livres = sum(1 for p in pautas if not p.get("usada") and int(p.get("capitulo", 1)) == cap)
print(json.dumps({
    "id": pauta["id"], "base": base, "pasta": pasta_rel,
    "media": [f"{RAW}/{pasta_rel}/tela-{n}.jpg" for n in range(1, 5)],
    "legenda": pauta["legenda"], "tiktok": pauta.get("tiktok", ""),
    "pautas_livres_do_capitulo": livres,
}, ensure_ascii=False, indent=1))
