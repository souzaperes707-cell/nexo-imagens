#!/usr/bin/env python3
"""Vídeo do NEXO - V1 (15/11/2026): transforma as 4 telas de um carrossel em vídeo vertical 9:16
com zoom lento, transições e trilha original (robo/trilhas.py).

Uso: python3 robo/gerar-video.py AAAA-MM/<id> [estilo]
  estilo: suspense | acao | tensao | misterio  (sem estilo: rodízio pelo dia do ano)
Saída: AAAA-MM/<id>/video.mp4  (link raw no GitHub serve para Metricool e Buffer)
"""
import os, subprocess, sys, datetime, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import trilhas

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = "https://raw.githubusercontent.com/souzaperes707-cell/nexo-imagens/main"
pasta_rel = sys.argv[1].strip("/")
estilos = list(trilhas.ESTILOS)
estilo = sys.argv[2] if len(sys.argv) > 2 else estilos[datetime.date.today().timetuple().tm_yday % len(estilos)]
pasta = os.path.join(RAIZ, pasta_rel)
telas = [os.path.join(pasta, f"tela-{n}.jpg") for n in range(1, 5)]
DUR = 14.2

with tempfile.TemporaryDirectory() as tmp:
    wav = os.path.join(tmp, "trilha.wav")
    trilhas.gerar(estilo, DUR, wav, abs(hash(pasta_rel)) % 10**6)
    Z = ("scale=2160:2700,zoompan=z='min(zoom+0.0006,1.06)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
         ":d=120:s=1080x1350:fps=30,pad=1080:1920:0:285:color=0x0E0E10,setsar=1")
    fc = (f"[0]{Z}[v0];[1]{Z}[v1];[2]{Z}[v2];[3]{Z},tpad=stop_mode=clone:stop_duration=1[v3];"
          "[v0][v1]xfade=transition=fade:duration=0.6:offset=3.4[a];"
          "[a][v2]xfade=transition=fade:duration=0.6:offset=6.8[b];"
          "[b][v3]xfade=transition=fade:duration=0.6:offset=10.2,format=yuv420p[out]")
    cmd = ["ffmpeg", "-y", "-loglevel", "error"]
    for tl in telas:
        cmd += ["-i", tl]
    cmd += ["-i", wav, "-filter_complex", fc, "-map", "[out]", "-map", "4:a",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "23", "-r", "30",
            "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart",
            os.path.join(pasta, "video.mp4")]
    subprocess.run(cmd, check=True, timeout=280)

print(f"{RAW}/{pasta_rel}/video.mp4  (estilo: {estilo})")
