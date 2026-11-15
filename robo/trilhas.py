#!/usr/bin/env python3
"""Trilhas do NEXO - V1 (15/11/2026). Música original gerada por código (sem direito autoral de terceiros).

Estilos: suspense, acao, tensao, misterio. Cada chamada varia tom e notas pela "semente".
Uso: python3 robo/trilhas.py <estilo> <segundos> <saida.wav> [semente]
"""
import sys, wave, random
import numpy as np

SR = 44100

def nota(m):
    return 440 * 2 ** ((m - 69) / 12)

def env_ar(tt, a, r, total):
    return np.clip(tt / a, 0, 1) * np.clip((total - tt) / r, 0, 1)

def tom(rng):
    return rng.choice([-3, -2, 0, 2, 3])  # transposição

def batida(t, out, inicio, passo, vol=0.35, freq=52, dupla=True):
    for b in np.arange(inicio, t[-1], passo):
        for off, a in ((0, 1), (0.22, 0.7)) if dupla else ((0, 1),):
            m = (t >= b + off) & (t < b + off + 0.18)
            tt = t[m] - (b + off)
            out[m] += vol * a * np.exp(-tt * 25) * np.sin(2 * np.pi * freq * tt)

def suspense(t, rng, dur):
    out = np.zeros_like(t); k = tom(rng)
    prog = [[57, 60, 64], [53, 57, 60], [50, 53, 57], [52, 56, 59]]
    rng.shuffle(prog[1:3])
    seg = dur / 4
    for i, c in enumerate(prog):
        m = (t >= i * seg) & (t < (i + 1) * seg + 0.6); tt = t[m] - i * seg
        e = env_ar(tt, 1.2, 0.9, seg + 0.6)
        out[m] += 0.06 * e * sum(np.sin(2*np.pi*nota(n+k)*tt) + 0.5*np.sin(2*np.pi*nota(n+k)*1.003*tt) for n in c)
        out[m] += 0.18 * e * np.sin(2*np.pi*nota(c[0]-24+k)*tt)
    for ti in np.arange(0.5, dur - 1, 1.6):
        n = rng.choice([69, 71, 72, 74, 76, 77]) + k
        m = (t >= ti) & (t < ti + 2.5); tt = t[m] - ti
        out[m] += 0.12 * np.exp(-tt * 2.2) * (np.sin(2*np.pi*nota(n)*tt) + 0.3*np.sin(4*np.pi*nota(n)*tt))
    batida(t, out, 0.3, 1.15)
    return out

def acao(t, rng, dur):
    out = np.zeros_like(t); k = tom(rng)
    bpm = rng.choice([128, 136, 144]); b = 60 / bpm
    raiz = [45, 45, 41, 43] if rng.random() < 0.5 else [45, 48, 43, 41]
    # baixo em semicolcheias (cordas staccato)
    for i, ti in enumerate(np.arange(0, dur, b / 2)):
        n = raiz[int(ti // (dur / 4)) % 4] + k
        m = (t >= ti) & (t < ti + b / 2 * 0.8); tt = t[m] - ti
        saw = sum(np.sin(2*np.pi*nota(n)*h*tt) / h for h in range(1, 6))
        out[m] += 0.10 * np.exp(-tt * 9) * saw * (1.3 if i % 4 == 0 else 1)
    # bumbo e caixa
    for i, ti in enumerate(np.arange(0, dur, b)):
        m = (t >= ti) & (t < ti + 0.25); tt = t[m] - ti
        out[m] += 0.55 * np.exp(-tt * 18) * np.sin(2*np.pi*(55 + 60*np.exp(-tt*40))*tt)
        if i % 2 == 1:
            m2 = (t >= ti) & (t < ti + 0.15); tt2 = t[m2] - ti
            out[m2] += 0.18 * np.exp(-tt2 * 30) * rng.standard_normal(m2.sum())
    # metais graves (acordes longos)
    seg = dur / 4
    for i in range(4):
        m = (t >= i * seg) & (t < (i + 1) * seg); tt = t[m] - i * seg
        n = raiz[i] + 12 + k
        out[m] += 0.05 * env_ar(tt, 0.05, 0.4, seg) * sum(np.sin(2*np.pi*nota(n+x)*tt) for x in (0, 7, 12))
    # riser no fim
    m = t > dur - 2.5; tt = t[m] - (dur - 2.5)
    out[m] += 0.06 * (tt / 2.5) * rng.standard_normal(m.sum())
    return out

def tensao(t, rng, dur):
    out = np.zeros_like(t); k = tom(rng)
    b = 60 / rng.choice([100, 110, 120])
    seq = [57, 57, 60, 57, 55, 57, 52, 57]
    for i, ti in enumerate(np.arange(0, dur, b / 2)):
        n = seq[i % len(seq)] + k - 12
        m = (t >= ti) & (t < ti + b / 2 * 0.9); tt = t[m] - ti
        corte = 1 + 3 * (ti / dur)  # abre o filtro aos poucos
        sq = np.sign(np.sin(2*np.pi*nota(n)*tt)) * 0.4 + np.sin(2*np.pi*nota(n)*tt)
        out[m] += 0.07 * np.exp(-tt * (12 / corte)) * sq
    m = t >= 0; out += 0.05 * np.sin(2*np.pi*nota(33+k)*t) * np.clip(t / 3, 0, 1)
    batida(t, out, 0.0, b * 2, vol=0.45, freq=48, dupla=False)
    return out

def misterio(t, rng, dur):
    out = np.zeros_like(t); k = tom(rng)
    escala = [69, 72, 74, 75, 76, 79, 81]
    for ti in np.arange(0.2, dur - 1, 0.45):
        n = rng.choice(escala) + 12 + k
        m = (t >= ti) & (t < ti + 1.5); tt = t[m] - ti
        out[m] += 0.09 * np.exp(-tt * 3.5) * (np.sin(2*np.pi*nota(n)*tt) + 0.5*np.sin(2*np.pi*nota(n)*3*tt))
    out += 0.05 * np.sin(2*np.pi*nota(45+k)*t) * (0.6 + 0.4*np.sin(2*np.pi*0.2*t))
    out += 0.03 * np.sin(2*np.pi*nota(52+k)*t)
    return out

ESTILOS = {"suspense": suspense, "acao": acao, "tensao": tensao, "misterio": misterio}

def gerar(estilo, dur, saida, semente=None):
    rng = np.random.default_rng(semente)
    t = np.arange(int(SR * dur)) / SR
    out = ESTILOS[estilo](t, rng, dur)
    out *= np.clip(t / 0.8, 0, 1) * np.clip((dur - t) / 1.5, 0, 1)
    out = out / (np.max(np.abs(out)) + 1e-9) * 0.85
    with wave.open(saida, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((out * 32767).astype(np.int16).tobytes())

if __name__ == "__main__":
    est, dur, saida = sys.argv[1], float(sys.argv[2]), sys.argv[3]
    sem = int(sys.argv[4]) if len(sys.argv) > 4 else random.randint(0, 10**6)
    gerar(est, dur, saida, sem)
    print(saida)
