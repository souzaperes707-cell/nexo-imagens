#!/usr/bin/env python3
"""Sexta do NEXO - V1 (15/11/2026): vídeo vertical com uma PÁGINA REAL do livro + música do autor.

Uso: python3 robo/gerar-pagina.py <numero_da_pagina_do_livro> <parte> <total> <AAAA-MM-DD>
  ex.: python3 robo/gerar-pagina.py 12 1 20 2026-11-20
Entrada: robo/livro/pNNN.jpg (páginas grátis 12 a 31, as mesmas do site)
Saída:   serie/sexta-PP/video.mp4 e serie/sexta-PP/capa.jpg
Áudio:   dois trechos seguidos da mesma música (robo/musicas) com fusão de 3 s = cerca de 27 s
"""
import os, sys, glob, re, datetime, subprocess, tempfile
from PIL import Image, ImageDraw, ImageFont, ImageFilter

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = "https://raw.githubusercontent.com/souzaperes707-cell/nexo-imagens/main"
pag, parte, total, data = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), datetime.date.fromisoformat(sys.argv[4])
F = "/usr/share/fonts/truetype/dejavu/"
W, H = 1080, 1920
AZUL, OURO, PRATA, FUNDO = (56, 189, 255), (242, 163, 58), (217, 221, 227), (8, 11, 17)

def fonte(nome, tam): return ImageFont.truetype(F + nome, tam)
def centro(d, y, txt, f, cor, esp=0):
    if esp:
        larg = sum(d.textlength(c, font=f) for c in txt) + esp * (len(txt) - 1)
        x = (W - larg) / 2
        for c in txt:
            d.text((x, y), c, font=f, fill=cor); x += d.textlength(c, font=f) + esp
    else:
        d.text(((W - d.textlength(txt, font=f)) / 2, y), txt, font=f, fill=cor)

# quadro
img = Image.new("RGB", (W, H), FUNDO)
brilho = Image.new("RGB", (W, H), FUNDO); bd = ImageDraw.Draw(brilho)
bd.ellipse((-200, 500, W + 200, 1500), fill=(14, 40, 62)); brilho = brilho.filter(ImageFilter.GaussianBlur(160))
img = Image.blend(img, brilho, 0.9)
d = ImageDraw.Draw(img)
centro(d, 70, "SEXTA DO NEXO", fonte("DejaVuSansCondensed-Bold.ttf", 54), AZUL, esp=10)
centro(d, 148, f"PÁGINA {parte} DE {total}", fonte("DejaVuSansCondensed-Bold.ttf", 38), OURO, esp=6)
p = Image.open(os.path.join(RAIZ, "robo", "livro", f"p{pag:03d}.jpg")).convert("RGB").resize((960, 1440), Image.LANCZOS)
sombra = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(sombra)
sd.rectangle((60 + 14, 230 + 18, 60 + 960 + 14, 230 + 1440 + 18), fill=(0, 0, 0, 170)); sombra = sombra.filter(ImageFilter.GaussianBlur(18))
img.paste(sombra, (0, 0), sombra); img.paste(p, (60, 230))
d = ImageDraw.Draw(img)
fim = "Continua na próxima sexta" if parte < total else "Fim da leitura grátis"
centro(d, 1712, fim, fonte("DejaVuSerif-Italic.ttf", 40), PRATA)
centro(d, 1780, "OU LEIA AGORA · LINK NA BIO", fonte("DejaVuSansCondensed-Bold.ttf", 40), OURO, esp=4)

pasta = os.path.join(RAIZ, "serie", f"sexta-{parte:02d}"); os.makedirs(pasta, exist_ok=True)
capa = os.path.join(pasta, "capa.jpg"); img.save(capa, quality=90)

# música: dois trechos seguidos da mesma música (rodízio pela data)
por = {}
for f in sorted(glob.glob(os.path.join(RAIZ, "robo", "musicas", "*.m4a"))):
    por.setdefault(re.sub(r"-\d+\.m4a$", "", os.path.basename(f)), []).append(f)
nomes = sorted(n for n in por if len(por[n]) >= 4)
musica = por[nomes[data.toordinal() % len(nomes)]]
k = (data.toordinal() // len(nomes)) % (len(musica) - 1)
a1, a2 = musica[k], musica[k + 1]
DUR = 27.0
fc = (f"[0]scale=1188:2112,zoompan=z='min(zoom+0.0002,1.04)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={int(DUR*30)}:s={W}x{H}:fps=30,"
      f"fade=t=in:st=0:d=0.6,format=yuv420p[v];"
      f"[1:a][2:a]acrossfade=d=3[m];[m]atrim=0:{DUR},afade=t=out:st={DUR-2}:d=2,loudnorm=I=-20:TP=-2:LRA=11[a]")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", capa, "-i", a1, "-i", a2, "-filter_complex", fc,
                "-map", "[v]", "-map", "[a]", "-t", str(DUR), "-c:v", "libx264", "-preset", "veryfast", "-crf", "22",
                "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", os.path.join(pasta, "video.mp4")], check=True, timeout=400)
rel = os.path.relpath(pasta, RAIZ)
print(f"{RAW}/{rel}/video.mp4  (página {pag}, parte {parte}/{total}, música: {os.path.basename(a1)} + {os.path.basename(a2)})")
