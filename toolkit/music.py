"""Soundtrack + SFX synthesizer for code-made videos. Original audio, no samples, no API key.

    python music.py spec.json out.wav

Everything is placed on the picture's clock (seconds), so hits land on the cuts.
Deterministic: same spec → same file. Needs numpy and scipy.

spec.json
{
  "duration": 15,            seconds
  "bpm": 120,                beat grid for drums / bass / arp (a bar is 4 beats)
  "transpose": 0,            semitones from D major
  "progression": "uplift",   uplift | bright | minor   (one chord per bar)
  "seed": 7,
  "fade_out": 1.4,
  "sections": [              what the band plays between two times
    {"from": 0,   "to": 2,  "type": "rumble"},   low drone, no pulse
    {"from": 2,   "to": 6,  "type": "pad"},      chords + slow arpeggio, no drums
    {"from": 6,   "to": 10, "type": "full"},     four-on-the-floor, clap, bass, fast arpeggio
    {"from": 10,  "to": 12, "type": "half"},     kick on 1 and 3
    {"from": 0,   "to": 4,  "type": "dark"},     minor drone + bass pulse, tense
    {"from": 12,  "to": 15, "type": "final"}     big held chord with sparkle
  ],
  "lead": [[6, 10]],         spans where a bell melody plays over the groove
  "hits": [                  one-shots, at exact picture times
    {"t": 2.0, "fx": "impact"},                  impact | tick | pop | buzz | whoosh | riser | down | bell | chime | roll
    {"t": 1.0, "fx": "riser", "len": 1.0, "gain": 0.5, "pan": 0.2},
    {"t": 5.0, "fx": "bell", "note": 81}
  ]
}
"""
import json
import sys
import numpy as np
from scipy import signal
from scipy.io import wavfile

spec = json.load(open(sys.argv[1], encoding='utf8'))
OUT = sys.argv[2] if len(sys.argv) > 2 else 'soundtrack.wav'
SR = 48000
DUR = float(spec['duration'])
N = int(SR * DUR)
BEAT = 60.0 / float(spec.get('bpm', 120))
BAR = BEAT * 4
TR = int(spec.get('transpose', 0))
rng = np.random.default_rng(int(spec.get('seed', 7)))


def hz(n):
    return 440.0 * 2 ** ((n + TR - 69) / 12)


def env(n, a, d, curve=4.0):
    t = np.arange(n) / SR
    e = np.exp(-curve * np.maximum(t - a, 0) / max(d, 1e-4))
    if a > 0:
        e *= np.minimum(t / a, 1.0)
    return e


def lp(x, fc, order=2):
    return signal.sosfilt(signal.butter(order, fc, 'low', fs=SR, output='sos'), x, axis=0)


def hp(x, fc, order=2):
    return signal.sosfilt(signal.butter(order, fc, 'high', fs=SR, output='sos'), x, axis=0)


def bp(x, lo, hi, order=2):
    return signal.sosfilt(signal.butter(order, [lo, hi], 'band', fs=SR, output='sos'), x, axis=0)


def saw(f, n, detune=0.0, phase=0.0):
    t = np.arange(n) / SR
    return 2 * (((f * (1 + detune)) * t + phase) % 1.0) - 1


def put(track, x, at, gain=1.0, pan=0.0):
    i = int(round(at * SR))
    if i >= N or i < 0:
        return
    x = x[: N - i]
    l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    track[i:i + len(x), 0] += x * gain * l
    track[i:i + len(x), 1] += x * gain * r


# ── instruments ────────────────────────────────────────────────────────────
def kick():
    n = int(0.42 * SR)
    t = np.arange(n) / SR
    body = np.sin(2 * np.pi * np.cumsum(46 + 110 * np.exp(-t / 0.035)) / SR) * np.exp(-t / 0.16)
    click = hp(rng.standard_normal(n), 3000) * np.exp(-t / 0.004) * 0.25
    return np.tanh(1.6 * body) + click


def clap():
    n = int(0.3 * SR)
    t = np.arange(n) / SR
    burst = sum(np.exp(-np.maximum(t - d, 0) / 0.012) * (t >= d) for d in (0, 0.011, 0.023))
    return bp(rng.standard_normal(n), 900, 5200) * (burst * 0.5 + np.exp(-t / 0.09) * 0.5)


def hat(decay=0.03):
    n = int(0.12 * SR)
    return hp(rng.standard_normal(n), 7500, 4) * np.exp(-np.arange(n) / SR / decay)


def pluck(note, length=0.32, bright=3400):
    n = int(length * SR)
    f = hz(note)
    x = saw(f, n) * 0.6 + saw(f, n, 0.004, 0.3) * 0.4 + np.sin(2 * np.pi * f * 2 * np.arange(n) / SR) * 0.15
    return lp(x, bright) * env(n, 0.003, length * 0.45)


def bass_note(note, length):
    n = int(length * SR)
    f = hz(note)
    t = np.arange(n) / SR
    x = np.sin(2 * np.pi * f * t) * 0.9 + lp(saw(f, n), 420) * 0.55
    return x * env(n, 0.006, length, curve=2.2) * np.minimum((n - np.arange(n)) / (0.012 * SR), 1)


def pad_chord(notes, length, bright=1500):
    n = int(length * SR)
    x = np.zeros(n)
    for k, note in enumerate(notes):
        f = hz(note)
        for det in (-0.006, 0.0, 0.007):
            x += saw(f, n, det, phase=0.13 * k + det * 40)
    t = np.arange(n) / SR
    a = np.minimum(t / 0.35, 1) * np.minimum((length - t) / 0.45, 1).clip(0)
    return lp(x, bright, 2) * a / (3 * len(notes))


def bell(note, length=1.2):
    n = int(length * SR)
    t = np.arange(n) / SR
    f = hz(note)
    x = np.sin(2 * np.pi * f * t) + 0.45 * np.sin(2 * np.pi * f * 2.01 * t) * np.exp(-t / 0.2) + 0.2 * np.sin(2 * np.pi * f * 3.02 * t) * np.exp(-t / 0.08)
    return x * env(n, 0.004, length * 0.55, curve=3.2)


def noise_sweep(length, lo, hi, shape='up'):
    n = int(length * SR)
    x = bp(rng.standard_normal(n), lo, hi)
    p = np.linspace(0, 1, n)
    return x * {'up': p ** 2.4, 'down': (1 - p) ** 2.0, 'bell': np.sin(np.pi * p) ** 2}[shape]


def impact():
    n = int(1.6 * SR)
    t = np.arange(n) / SR
    boom = np.sin(2 * np.pi * np.cumsum(38 + 60 * np.exp(-t / 0.05)) / SR) * np.exp(-t / 0.45)
    return np.tanh(1.4 * boom) + lp(rng.standard_normal(n), 2600) * np.exp(-t / 0.09) * 0.5


def tick():
    n = int(0.03 * SR)
    t = np.arange(n) / SR
    return np.sin(2 * np.pi * 2300 * t) * np.exp(-t / 0.004) + hp(rng.standard_normal(n), 5000) * np.exp(-t / 0.002) * 0.4


def pop(f0=820, f1=1500):
    n = int(0.09 * SR)
    t = np.arange(n) / SR
    return np.sin(2 * np.pi * np.cumsum(np.linspace(f0, f1, n)) / SR) * np.exp(-t / 0.03)


def buzz():
    n = int(0.2 * SR)
    t = np.arange(n) / SR
    return lp(np.sign(np.sin(2 * np.pi * 92 * t)) + 0.6 * np.sign(np.sin(2 * np.pi * 97.5 * t)), 900) * np.exp(-t / 0.11)


# ── harmony (written in D; "transpose" moves everything) ───────────────────
D = dict(bass=38, pad=[50, 54, 57, 64], arp=[62, 66, 69, 74, 76], lead=[(0, 78, 1.0), (1.5, 81, 0.5), (2, 76, 1.6)])
A = dict(bass=37, pad=[49, 52, 57, 64], arp=[61, 64, 69, 73, 76], lead=[(0, 76, 1.0), (1.5, 73, 0.5), (2, 69, 1.6)])
Bm = dict(bass=35, pad=[47, 54, 57, 62], arp=[59, 62, 66, 71, 74], lead=[(0, 74, 1.0), (1.5, 78, 0.5), (2, 71, 1.6)])
G = dict(bass=31, pad=[43, 50, 55, 59], arp=[62, 67, 71, 74, 79], lead=[(0, 71, 1.0), (1.5, 74, 0.5), (2.5, 76, 0.5), (3, 81, 1.0)])
PROGRESSIONS = {'uplift': [D, A, Bm, G], 'bright': [G, D, A, Bm], 'minor': [Bm, G, D, A]}
CHORDS = PROGRESSIONS[spec.get('progression', 'uplift')]
ARP = [0, 2, 1, 3, 2, 4, 3, 1]


def spans(kind):
    return [(s['from'], s['to']) for s in spec.get('sections', []) if s['type'] == kind]


def inside(t, ss):
    return any(a - 1e-6 <= t < b - 1e-6 for a, b in ss)


FULL, HALF, PAD, DARK, FINAL, RUMBLE = (spans(k) for k in ('full', 'half', 'pad', 'dark', 'final', 'rumble'))
LEAD = [tuple(x) for x in spec.get('lead', [])]
drums, bassT, padT, arpT, leadT, fx = (np.zeros((N, 2)) for _ in range(6))
K, C, H, HO = kick(), clap(), hat(0.025), hat(0.07)
kick_times = []

for b in range(int(DUR / BEAT) + 1):
    t = b * BEAT
    beat = b % 4
    ch = CHORDS[(b // 4) % 4]
    full, half = inside(t, FULL), inside(t, HALF)
    if full or (half and beat in (0, 2)):
        put(drums, K, t, 0.95); kick_times.append(t)
    if full and beat in (1, 3):
        put(drums, C, t, 0.5)
    if full or half:
        put(drums, HO, t + BEAT / 2, 0.16, 0.25)
        for s in (0, 0.25, 0.75):
            put(drums, H, t + s * BEAT, 0.07 if s else 0.1, -0.2)
        put(bassT, bass_note(ch['bass'], BEAT * 0.44), t + BEAT / 2, 0.55)
        if full and beat == 3:
            put(bassT, bass_note(ch['bass'] + 12, BEAT * 0.22), t + BEAT * 0.75, 0.35)
    if full or half or inside(t, PAD):
        steps = 4 if full else 2
        for k in range(steps):
            idx = ARP[((b * steps) + k) % len(ARP)]
            put(arpT, pluck(ch['arp'][idx], 0.3, 4200 if full else 3000), t + k * BEAT / steps,
                (0.2 if full else 0.24) * (1.0 if k % 2 == 0 else 0.7), 0.5 if k % 2 else -0.5)
    if inside(t, DARK):
        put(bassT, bass_note(35, BEAT * 0.6), t, 0.42)
        put(drums, H, t + BEAT / 2, 0.07, 0.2)

for bar in range(int(DUR / BAR) + 1):
    t = bar * BAR
    ch = CHORDS[bar % 4]
    if inside(t, FULL) or inside(t, HALF) or inside(t, PAD):
        put(padT, pad_chord(ch['pad'], BAR + 0.15, 1900 if inside(t, FULL) else 1300), t, 0.5)
    if inside(t, LEAD):
        for off, note, ln in ch['lead']:
            put(leadT, bell(note, ln * BEAT + 0.5), t + off * BEAT, 0.16, 0.15)

for a, b in DARK:
    put(padT, pad_chord([35, 42, 47, 54], b - a + 0.2, 700), a, 0.75)
for a, b in RUMBLE:
    n = int((b - a + 0.2) * SR)
    put(fx, lp(rng.standard_normal(n), 180) * np.linspace(0.3, 1, n), a, 0.5)
    put(bassT, bass_note(26, b - a), a + 0.05, 0.4)
for a, b in FINAL:
    put(padT, pad_chord([38, 50, 54, 57, 62, 66], b - a + 0.1, 2000), a, 0.9)
    put(bassT, bass_note(26, min(3.5, b - a)), a, 0.55)
    for k, note in enumerate([74, 78, 81, 86, 90]):
        put(leadT, bell(note, 2.4), a + min(2.5, (b - a) * 0.55) + k * 0.09, 0.14, -0.4 + 0.2 * k)

# ── one-shots ──────────────────────────────────────────────────────────────
for h in spec.get('hits', []):
    t, kind, g, pan, ln = h['t'], h['fx'], h.get('gain'), h.get('pan', 0.0), h.get('len', 0.6)
    if kind == 'impact':
        put(fx, impact(), t, g or 0.85, pan)
    elif kind == 'tick':
        put(fx, tick(), t, g or 0.6, pan)
    elif kind == 'pop':
        f0 = h.get('pitch', 820)
        put(fx, pop(f0, f0 * 1.8), t, g or 0.35, pan)
    elif kind == 'buzz':
        put(fx, buzz(), t, g or 0.75, pan); put(fx, buzz(), t + 0.23, (g or 0.75) * 0.8, pan)
    elif kind == 'whoosh':
        put(fx, noise_sweep(ln, 700, 7000, 'bell'), t, g or 0.35, pan)
    elif kind == 'riser':
        put(fx, noise_sweep(ln, 400, 9500, 'up'), t, g or 0.5, pan)
    elif kind == 'down':
        put(fx, noise_sweep(ln, 250, 5000, 'down'), t, g or 0.5, pan)
    elif kind == 'bell':
        put(leadT, bell(h.get('note', 81), h.get('len', 1.3)), t, g or 0.2, pan)
    elif kind == 'chime':
        n0 = h.get('note', 81)
        put(leadT, bell(n0, 1.2), t, g or 0.22, -0.1); put(leadT, bell(n0 + 5, 1.6), t + 0.14, g or 0.22, 0.3)
    elif kind == 'roll':
        steps = max(2, int(ln / (BEAT / 4)))
        for i in range(steps):
            put(drums, C, t + i * BEAT / 4, (g or 0.14) + 0.05 * i * 8 / steps)
    else:
        raise SystemExit(f'fx desconocido: {kind}')


# ── mix ────────────────────────────────────────────────────────────────────
def delay(x, time, fb, mix):
    d = int(time * SR)
    out, tap = x.copy(), x.copy()
    for _ in range(5):
        tap = np.roll(tap, d, axis=0)[:, ::-1] * fb
        tap[:d] = 0
        out += tap * mix
    return out


def reverb(x, length=2.2, mix=0.25):
    n = int(length * SR)
    t = np.arange(n) / SR
    ir = np.stack([rng.standard_normal(n), rng.standard_normal(n)], 1) * np.exp(-t / (length / 5))[:, None]
    ir = hp(lp(ir, 6500), 250)
    ir /= np.sqrt((ir ** 2).sum(0)).max()
    return x + np.stack([signal.fftconvolve(x[:, c], ir[:, c])[:N] for c in (0, 1)], 1) * mix


duck = np.ones(N)
for t in kick_times:
    i = int(t * SR)
    n = min(int(0.3 * SR), N - i)
    if n > 0:
        duck[i:i + n] = np.minimum(duck[i:i + n], 1 - 0.62 * np.exp(-np.arange(n) / SR / 0.11))
duck = duck[:, None]

arpT = reverb(delay(arpT, BEAT * 0.75, 0.42, 0.55), 2.0, 0.22)
leadT = reverb(delay(leadT, BEAT * 0.75, 0.4, 0.4), 2.8, 0.4)
padT = reverb(padT, 3.0, 0.35)
fx = reverb(fx, 2.4, 0.3)
mix = hp(drums * 0.9 + (bassT * 0.8 + padT + arpT * 0.9 + leadT * 0.9) * duck + fx * 0.8, 28)

k = int(float(spec.get('fade_out', 1.4)) * SR)
if k > 0:
    mix[-k:] *= (np.cos(np.linspace(0, np.pi / 2, k)) ** 2)[:, None]
mix = np.tanh(mix * 0.7 / np.percentile(np.abs(mix), 99.7))   # glue + soft limit, lands near -14 LUFS
mix *= 10 ** (-1.5 / 20) / np.abs(mix).max()
wavfile.write(OUT, SR, (mix * 32767).astype(np.int16))
print('wrote', OUT, f'{DUR:.2f}s')
