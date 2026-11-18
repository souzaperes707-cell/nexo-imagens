#!/usr/bin/env python3
"""Vídeo do NEXO - V3 (17/11/2026): GANCHO NO 1º SEGUNDO + vídeo curto (cerca de 9,5 s) + volume -20 LUFS.

Por quê: em 16-17/11 o público assistiu ~2 s de vídeos de 14 s. A V3 abre com uma frase grande
(título da pauta) entrando com impacto, depois as 4 telas em ritmo rápido e a chamada final.

Uso: python3 robo/gerar-video.py AAAA-MM/<id> [AAAA-MM-DD | trecho.m4a | suspense|acao|tensao|misterio]
Saída: AAAA-MM/<id>/video.mp4 (+ gancho.jpg)
"""
import os, subprocess, sys, datetime, tempfile, glob, re, json
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import trilhas

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = "https://raw.githubusercontent.com/souzaperes707-cell/nexo-imagens/main"
MUSICAS = os.path.join(RAIZ, "robo", "musicas")
pasta_rel = sys.argv[1].strip("/")
escolha = sys.argv[2] if len(sys.argv) > 2 else ""
pasta = os.path.join(RAIZ, pasta_rel)
pid = os.path.basename(pasta_rel)
telas = [os.path.join(pasta, f"tela-{n}.jpg") for n in range(1, 5)]
# tempos (s): gancho, tela1..tela4 ; transição curta
SEG = [1.7, 1.9, 1.9, 1.9, 2.6]
XF = 0.25
DUR = sum(SEG) - XF * (len(SEG) - 1)
F = "/usr/share/fonts/truetype/dejavu/"

def fila_de_trechos():
    por = {}
    for f in sorted(glob.glob(os.path.join(MUSICAS, "*.m4a"))):
        por.setdefault(re.sub(r"-\d+\.m4a$", "", os.path.basename(f)), []).append(f)
    fila, i = [], 0
    while any(i < len(v) for v in por.values()):
        for v in por.values():
            if i < len(v): fila.append(v[i])
        i += 1
    return fila

def frase_gancho():
    try:
        for p in json.load(open(os.path.join(RAIZ, "robo", "pautas.json"))):
            if p["id"] == pid: return p.get("tiktok") or p["telas"][0]
    except Exception: pass
    return "O sistema não tem lado."

def quadro_gancho(txt, saida):
    W, H = 1080, 1920
    img = Image.new("RGB", (W, H), (6, 8, 13)); g = Image.new("RGB", (W, H), (6, 8, 13))
    ImageDraw.Draw(g).ellipse((-300, 520, W + 300, 1500), fill=(16, 52, 84)); img = Image.blend(img, g.filter(ImageFilter.GaussianBlur(180)), 0.95)
    d = ImageDraw.Draw(img)
    txt = txt.upper().rstrip(".")
    for tam in range(150, 60, -6):
        f = ImageFont.truetype(F + "DejaVuSansCondensed-Bold.ttf", tam)
        linhas, atual = [], ""
        for w in txt.split():
            t = (atual + " " + w).strip()
            if d.textlength(t, font=f) <= W - 140: atual = t
            else: linhas.append(atual); atual = w
        linhas.append(atual)
        if len(linhas) <= 4: break
    lh = int(tam * 1.12); y = (H - lh * len(linhas)) // 2 - 40
    for i, l in enumerate(linhas):
        x = (W - d.textlength(l, font=f)) / 2
        d.text((x + 4, y + i * lh + 5), l, font=f, fill=(0, 0, 0))
        d.text((x, y + i * lh), l, font=f, fill=(255, 255, 255))
    yb = y + lh * len(linhas) + 30
    d.rectangle(((W - 220) // 2, yb, (W + 220) // 2, yb + 10), fill=(242, 163, 58))
    f2 = ImageFont.truetype(F + "DejaVuSansCondensed-Bold.ttf", 40)
    s = "N E X O  ·  T H R I L L E R  P O L Í T I C O"; d.text(((W - d.textlength(s, font=f2)) / 2, 230), s, font=f2, fill=(56, 189, 255))
    img.save(saida, quality=92)

with tempfile.TemporaryDirectory() as tmp:
    gancho = os.path.join(pasta, "gancho.jpg"); quadro_gancho(frase_gancho(), gancho)
    fila = fila_de_trechos(); data_post = None
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", escolha):
        data_post, escolha = datetime.date.fromisoformat(escolha), ""
    if escolha in trilhas.ESTILOS or not fila:
        estilo = escolha if escolha in trilhas.ESTILOS else list(trilhas.ESTILOS)[datetime.date.today().timetuple().tm_yday % len(trilhas.ESTILOS)]
        audio = os.path.join(tmp, "trilha.wav"); trilhas.gerar(estilo, DUR + 1, audio, abs(hash(pasta_rel)) % 10**6)
        rotulo = f"trilha de código: {estilo}"
    else:
        audio = (escolha if os.path.isabs(escolha) else os.path.join(MUSICAS, escolha)) if escolha else fila[(data_post or datetime.date.today()).toordinal() % len(fila)]
        rotulo = f"música do autor: {os.path.basename(audio)}"
    # gancho: fundo cheio 9:16 com "soco" de zoom (1.18 -> 1.0)
    fz = int(SEG[0] * 30)
    G = (f"scale=1296:2304,zoompan=z='max(1.18-0.18*on/{fz//3},1.0)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={fz}:s=1080x1920:fps=30,setsar=1")
    def T(n, i):
        d = int(SEG[i] * 30)
        return (f"scale=2160:2700,zoompan=z='min(zoom+0.0012,1.08)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={d}:s=1080x1350:fps=30,"
                f"pad=1080:1920:0:285:color=0x0E0E10,setsar=1")
    fc = f"[0]{G}[v0];"
    for i in range(1, 5): fc += f"[{i}]{T(i, i)}[v{i}];"
    off, prev = 0.0, "v0"
    for i in range(1, 5):
        off += SEG[i - 1] - XF
        trans = "fadeblack" if i == 1 else "slideleft"
        fc += f"[{prev}][v{i}]xfade=transition={trans}:duration={XF}:offset={off:.2f}[x{i}];"; prev = f"x{i}"
    fc += f"[{prev}]format=yuv420p[out];[5:a]atrim=0:{DUR:.2f},afade=t=in:d=0.05,afade=t=out:st={DUR-0.8:.2f}:d=0.8,loudnorm=I=-20:TP=-2:LRA=11[au]"
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", gancho] + sum([["-i", t] for t in telas], []) + ["-i", audio,
           "-filter_complex", fc, "-map", "[out]", "-map", "[au]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "22", "-r", "30",
           "-c:a", "aac", "-b:a", "128k", "-t", f"{DUR:.2f}", "-movflags", "+faststart", os.path.join(pasta, "video.mp4")]
    subprocess.run(cmd, check=True, timeout=280)
print(f"{RAW}/{pasta_rel}/video.mp4  ({rotulo})")
