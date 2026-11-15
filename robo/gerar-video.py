#!/usr/bin/env python3
"""Vídeo do NEXO - V2 (15/11/2026): transforma as 4 telas de um carrossel em vídeo vertical 9:16
com zoom lento, transições e trilha.

V2: a trilha principal são os trechos das músicas do próprio autor (robo/musicas/*.m4a),
em rodízio por dia, sem repetir a mesma música em dias seguidos.
Reserva: trilhas geradas por código (robo/trilhas.py), se não houver trechos.

Uso: python3 robo/gerar-video.py AAAA-MM/<id> [AAAA-MM-DD | trecho.m4a | suspense|acao|tensao|misterio]
  AAAA-MM-DD = data em que o vídeo vai ao ar (define o trecho do rodízio; sem data, usa hoje)
Saída: AAAA-MM/<id>/video.mp4  (link raw no GitHub serve para Metricool e Buffer)
"""
import os, subprocess, sys, datetime, tempfile, glob, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import trilhas

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = "https://raw.githubusercontent.com/souzaperes707-cell/nexo-imagens/main"
MUSICAS = os.path.join(RAIZ, "robo", "musicas")
pasta_rel = sys.argv[1].strip("/")
escolha = sys.argv[2] if len(sys.argv) > 2 else ""
pasta = os.path.join(RAIZ, pasta_rel)
telas = [os.path.join(pasta, f"tela-{n}.jpg") for n in range(1, 5)]
DUR = 14.2


def fila_de_trechos():
    """Intercala as músicas: trecho 1 de cada, depois trecho 2 de cada... (nunca a mesma música em dias seguidos)."""
    por_musica = {}
    for f in sorted(glob.glob(os.path.join(MUSICAS, "*.m4a"))):
        nome = re.sub(r"-\d+\.m4a$", "", os.path.basename(f))
        por_musica.setdefault(nome, []).append(f)
    fila, i = [], 0
    while any(i < len(v) for v in por_musica.values()):
        for v in por_musica.values():
            if i < len(v):
                fila.append(v[i])
        i += 1
    return fila


with tempfile.TemporaryDirectory() as tmp:
    fila = fila_de_trechos()
    data_post = None
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", escolha):
        data_post, escolha = datetime.date.fromisoformat(escolha), ""
    if escolha in trilhas.ESTILOS or not fila:
        estilo = escolha if escolha in trilhas.ESTILOS else list(trilhas.ESTILOS)[datetime.date.today().timetuple().tm_yday % len(trilhas.ESTILOS)]
        audio = os.path.join(tmp, "trilha.wav")
        trilhas.gerar(estilo, DUR, audio, abs(hash(pasta_rel)) % 10**6)
        rotulo = f"trilha de código: {estilo}"
    else:
        if escolha:
            audio = escolha if os.path.isabs(escolha) else os.path.join(MUSICAS, escolha)
        else:
            dia = (data_post or datetime.date.today()).toordinal()
            audio = fila[dia % len(fila)]
        rotulo = f"música do autor: {os.path.basename(audio)}"
    Z = ("scale=2160:2700,zoompan=z='min(zoom+0.0006,1.06)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
         ":d=120:s=1080x1350:fps=30,pad=1080:1920:0:285:color=0x0E0E10,setsar=1")
    fc = (f"[0]{Z}[v0];[1]{Z}[v1];[2]{Z}[v2];[3]{Z},tpad=stop_mode=clone:stop_duration=1[v3];"
          "[v0][v1]xfade=transition=fade:duration=0.6:offset=3.4[a];"
          "[a][v2]xfade=transition=fade:duration=0.6:offset=6.8[b];"
          "[b][v3]xfade=transition=fade:duration=0.6:offset=10.2,format=yuv420p[out];"
          f"[4:a]afade=t=out:st={DUR-1.4}:d=1.4[au]")
    cmd = ["ffmpeg", "-y", "-loglevel", "error"]
    for tl in telas:
        cmd += ["-i", tl]
    cmd += ["-i", audio, "-filter_complex", fc, "-map", "[out]", "-map", "[au]",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "23", "-r", "30",
            "-c:a", "aac", "-b:a", "128k", "-shortest", "-movflags", "+faststart",
            os.path.join(pasta, "video.mp4")]
    subprocess.run(cmd, check=True, timeout=280)

print(f"{RAW}/{pasta_rel}/video.mp4  ({rotulo})")
