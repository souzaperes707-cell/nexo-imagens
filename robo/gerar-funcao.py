#!/usr/bin/env python3
"""Fase 8 (19/11/2026) — peças por FUNÇÃO: descoberta (vídeo 9h), relacionamento (carrossel 12h), conversão (vídeo 19h).

Uso: python3 robo/gerar-funcao.py <spec.json> <pasta-saida> [trecho.m4a]
spec = {"tipo":"video"|"carrossel", "funcao":"descoberta|relacionamento|conversao",
        "telas":[{"txt":"...","peq":"linha pequena opcional","citacao":true|false,"capa":false}], "rodape":"..."}
Vídeo: 1080x1920, ~2,4 s por tela, transição curta, música do autor a -20 LUFS.
Carrossel: telas 1080x1350 (tela-1.jpg …).
"""
import os, sys, json, subprocess, tempfile, glob
from PIL import Image, ImageDraw, ImageFont, ImageFilter

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = "/usr/share/fonts/truetype/dejavu/"
COR = {"descoberta": (56, 189, 255), "relacionamento": (242, 163, 58), "conversao": (242, 163, 58)}
spec = json.load(open(sys.argv[1])); out = sys.argv[2]; os.makedirs(out, exist_ok=True)
trecho = sys.argv[3] if len(sys.argv) > 3 else sorted(glob.glob(os.path.join(RAIZ, "robo/musicas/*.m4a")))[0]
cor = COR.get(spec.get("funcao"), (56, 189, 255))

def quebra(d, txt, f, larg):
    linhas = []
    for par in txt.split("\n"):
        atual = ""
        for w in par.split():
            t = (atual + " " + w).strip()
            if d.textlength(t, font=f) <= larg: atual = t
            else: linhas.append(atual); atual = w
        linhas.append(atual)
    return linhas

def tela(t, W, H, saida, i, n):
    img = Image.new("RGB", (W, H), (6, 8, 13)); g = Image.new("RGB", (W, H), (6, 8, 13))
    ImageDraw.Draw(g).ellipse((-300, H * .28, W + 300, H * .78), fill=(16, 52, 84))
    img = Image.blend(img, g.filter(ImageFilter.GaussianBlur(170)), .95); d = ImageDraw.Draw(img)
    topo = ImageFont.truetype(F + "DejaVuSansCondensed-Bold.ttf", 34)
    s = "N E X O" if spec.get("funcao") != "descoberta" else ""
    d.text(((W - d.textlength(s, font=topo)) / 2, H * .085), s, font=topo, fill=cor)
    if t.get("capa"):
        capa = Image.open(os.path.join(RAIZ, "..", "nexo-site", "capa.jpg")) if os.path.exists(os.path.join(RAIZ, "..", "nexo-site", "capa.jpg")) else None
        if capa:
            capa.thumbnail((int(W * .46), int(H * .42))); img.paste(capa, ((W - capa.width) // 2, int(H * .17)))
            y0 = int(H * .17) + capa.height + 50
        else: y0 = int(H * .3)
    else: y0 = None
    serif = t.get("citacao")
    fonte = (F + "DejaVuSerifCondensed-Italic.ttf") if serif else (F + "DejaVuSansCondensed-Bold.ttf")
    txt = t["txt"] if serif else t["txt"].upper()
    maxl = 7 if serif else 5
    for tam in range(132 if not serif else 92, 44, -4):
        f = ImageFont.truetype(fonte, tam); linhas = quebra(d, txt, f, W - 150)
        if len(linhas) <= maxl: break
    lh = int(tam * (1.28 if serif else 1.1)); bloco = lh * len(linhas)
    y = y0 if y0 else (H - bloco) // 2 - 30
    for k, l in enumerate(linhas):
        x = (W - d.textlength(l, font=f)) / 2
        d.text((x + 3, y + k * lh + 4), l, font=f, fill=(0, 0, 0)); d.text((x, y + k * lh), l, font=f, fill=(255, 255, 255))
    yb = y + bloco + 26
    if t.get("peq"):
        fp = ImageFont.truetype(F + "DejaVuSansCondensed.ttf", 40)
        for k, l in enumerate(quebra(d, t["peq"], fp, W - 180)):
            d.text(((W - d.textlength(l, font=fp)) / 2, yb + 10 + k * 52), l, font=fp, fill=(170, 182, 196))
    if not serif:
        d.rectangle(((W - 180) // 2, y - 34, (W + 180) // 2, y - 26), fill=cor)
    rod = spec.get("rodape", "")
    if rod:
        fr = ImageFont.truetype(F + "DejaVuSansCondensed-Bold.ttf", 30)
        d.text(((W - d.textlength(rod, font=fr)) / 2, H * .9), rod, font=fr, fill=(120, 130, 145))
    if spec["tipo"] == "carrossel":
        fr = ImageFont.truetype(F + "DejaVuSansCondensed.ttf", 28); s = f"{i}/{n}"
        d.text((W - 90, H - 70), s, font=fr, fill=(110, 120, 135))
    img.save(saida, quality=90)

n = len(spec["telas"])
if spec["tipo"] == "carrossel":
    for i, t in enumerate(spec["telas"], 1): tela(t, 1080, 1350, os.path.join(out, f"tela-{i}.jpg"), i, n)
    sys.exit(0)

SEG = [t.get("dur", 2.4) for t in spec["telas"]]; XF = .3; DUR = sum(SEG) - XF * (n - 1)
with tempfile.TemporaryDirectory() as tmp:
    ins, filt = [], []
    for i, t in enumerate(spec["telas"]):
        p = os.path.join(tmp, f"t{i}.jpg"); tela(t, 1080, 1920, p, i + 1, n)
        ins += ["-loop", "1", "-t", str(SEG[i] + .1), "-i", p]
        filt.append(f"[{i}:v]scale=1080:1920,zoompan=z='min(zoom+0.0009,1.06)':d={int((SEG[i]+.1)*30)}:s=1080x1920:fps=30,format=yuv420p[v{i}]")
    acc, off = "v0", 0
    for i in range(1, n):
        off += SEG[i - 1] - XF
        filt.append(f"[{acc}][v{i}]xfade=transition=fade:duration={XF}:offset={off:.2f}[x{i}]"); acc = f"x{i}"
    ins += ["-i", trecho]
    filt.append(f"[{n}:a]atrim=0:{DUR:.2f},afade=t=in:d=0.4,afade=t=out:st={DUR-1:.2f}:d=1,loudnorm=I=-20:TP=-2:LRA=11[a]")
    cmd = ["ffmpeg", "-y", "-loglevel", "error"] + ins + ["-filter_complex", ";".join(filt), "-map", f"[{acc}]", "-map", "[a]",
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "23", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k", "-t", f"{DUR:.2f}", "-movflags", "+faststart", os.path.join(out, "video.mp4")]
    subprocess.run(cmd, check=True)
    Image.open(os.path.join(tmp, "t0.jpg")).save(os.path.join(out, "capa.jpg"), quality=85)
print("ok", out)
