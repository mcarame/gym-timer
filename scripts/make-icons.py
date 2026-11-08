#!/usr/bin/env python3
"""Genera le icone di "Ripeti" senza dipendenze esterne.

Perché così: su questo Mac non ci sono Homebrew né Pillow, e installarli per quattro
PNG sarebbe sproporzionato. Questo script disegna le forme geometriche a mano e scrive
i file PNG usando solo la libreria standard (zlib per la compressione).

Disegno: due archi concentrici che si inseguono (l'idea di "ciclo che si ripete") più un
punto centrale. Tre colori = le tre fasi dell'app (preparazione, lavoro, riposo).

Uso:  python3 scripts/make-icons.py
Output in public/icons/.
"""

import math
import os
import struct
import zlib

# --- Palette (identica a src/styles.css) -------------------------------------
BG = (0x0B, 0x0D, 0x0E)
WORK = (0xC6, 0xFF, 0x3D)   # verde acido
REST = (0x4D, 0xA3, 0xFF)   # azzurro
PREP = (0xFF, 0xB0, 0x20)   # ambra

CANVAS = 1024          # lato del disegno maestro
SS = 2                 # supersampling per lato -> 2048x2048 campioni
OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "public", "icons")


def draw_ring(buffer, n, cx, cy, radius, half_thickness, start_deg, end_deg, color):
    """Dipinge una corona circolare (arco con estremità arrotondate) nel buffer RGBA."""
    r_out = radius + half_thickness
    start = math.radians(start_deg)
    end = math.radians(end_deg)
    # estremi dell'arco, per le "punte" tonde
    caps = [
        (cx + radius * math.cos(start), cy + radius * math.sin(start)),
        (cx + radius * math.cos(end), cy + radius * math.sin(end)),
    ]
    span = (end_deg - start_deg) % 360

    for y in range(n):
        dy = y + 0.5 - cy
        for x in range(n):
            dx = x + 0.5 - cx
            dist = math.hypot(dx, dy)
            if dist > r_out + 1.5:
                continue
            hit = False
            if abs(dist - radius) <= half_thickness:
                ang = (math.degrees(math.atan2(dy, dx)) - start_deg) % 360
                if ang <= span:
                    hit = True
            if not hit:
                for cxp, cyp in caps:
                    if math.hypot(x + 0.5 - cxp, y + 0.5 - cyp) <= half_thickness:
                        hit = True
                        break
            if hit:
                i = (y * n + x) * 4
                buffer[i:i + 3] = bytes(color)


def draw_dot(buffer, n, cx, cy, radius, color):
    r2 = radius * radius
    for y in range(n):
        dy = y + 0.5 - cy
        for x in range(n):
            dx = x + 0.5 - cx
            if dx * dx + dy * dy <= r2:
                i = (y * n + x) * 4
                buffer[i:i + 3] = bytes(color)


def downsample(src, n, target):
    """Riduce a `target`x`target` mediando i pixel (box filter): è qui che nasce l'antialiasing."""
    out = bytearray(target * target * 4)
    scale = n / target
    for ty in range(target):
        y0 = ty * scale
        y1 = y0 + scale
        iy0, iy1 = int(y0), max(int(y0) + 1, int(math.ceil(y1)))
        for tx in range(target):
            x0 = tx * scale
            x1 = x0 + scale
            ix0, ix1 = int(x0), max(int(x0) + 1, int(math.ceil(x1)))
            r = g = b = 0
            count = 0
            for y in range(iy0, min(iy1, n)):
                row = y * n
                for x in range(ix0, min(ix1, n)):
                    i = (row + x) * 4
                    r += src[i]
                    g += src[i + 1]
                    b += src[i + 2]
                    count += 1
            o = (ty * target + tx) * 4
            out[o] = r // count
            out[o + 1] = g // count
            out[o + 2] = b // count
            out[o + 3] = 255
    return bytes(out)


def write_png(path, pixels, size):
    raw = bytearray()
    stride = size * 4
    for y in range(size):
        raw.append(0)  # filtro "None" per ogni riga
        raw += pixels[y * stride:(y + 1) * stride]

    def chunk(tag, data):
        return (struct.pack(">I", len(data)) + tag + data +
                struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF))

    header = struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0)
    png = (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header) +
           chunk(b"IDAT", zlib.compress(bytes(raw), 9)) + chunk(b"IEND", b""))
    with open(path, "wb") as fh:
        fh.write(png)
    print(f"  {os.path.basename(path):28} {size}x{size}  {len(png) / 1024:.1f} KB")


def build_master(content_scale=1.0):
    n = CANVAS
    buf = bytearray()
    for _ in range(n * n):
        buf += bytes(BG) + b"\xff"

    cx = cy = n / 2
    s = n / 2 * content_scale          # raggio di riferimento del contenuto

    # Arco esterno (lavoro): quasi mezzo giro, parte dalle ore 13 e chiude verso il basso.
    draw_ring(buf, n, cx, cy, radius=0.70 * s, half_thickness=0.105 * s,
              start_deg=-50, end_deg=130, color=WORK)
    # Arco interno (riposo): il giro successivo, ruotato di 180°.
    draw_ring(buf, n, cx, cy, radius=0.40 * s, half_thickness=0.085 * s,
              start_deg=130, end_deg=310, color=REST)
    # Punto centrale (preparazione).
    draw_dot(buf, n, cx, cy, radius=0.105 * s, color=PREP)
    return buf


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    print("Disegno le icone di Ripeti...")

    master = build_master(content_scale=1.0)
    for size, name in ((512, "icon-512.png"), (192, "icon-192.png"),
                       (180, "apple-touch-icon-180.png")):
        write_png(os.path.join(OUT_DIR, name), downsample(master, CANVAS, size), size)

    # Maskable: il sistema può ritagliare fino al 20% per lato, quindi il contenuto
    # va rimpicciolito dentro la zona sicura, mentre lo sfondo resta a tutto campo.
    maskable = build_master(content_scale=0.78)
    write_png(os.path.join(OUT_DIR, "icon-512-maskable.png"),
              downsample(maskable, CANVAS, 512), 512)
    print("Fatto.")


if __name__ == "__main__":
    main()
