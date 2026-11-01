"""Mute-Buzzer Gehäuse (CadQuery) – alle Maße in mm.

Teile:
  gehaeuse  – Unterteil mit Board-Führung, USB-C-Öffnung, Akkufach, JST-Tasche,
              Schiebeschalter-Tasche + Schlitz, Büroklammer-Reset, Gummifuß-Mulden
  deckel    – Steckdeckel mit MX-Ausschnitt (Plattenstärke 1,5) und Führungsring
  kappe     – Knopfkappe Ø50 mit MX-Kreuz, flache Oberseite (supportfrei kopfüber druckbar)
"""
import math
import cadquery as cq

# ---------------- Parameter ----------------
R_OUT = 40.0          # Außenradius
WALL = 2.5
R_IN = R_OUT - WALL   # 37.5
FLOOR = 2.0
H_BASE = 18.0

# Board (Pro Micro nRF52840): 18 x 33, USB-C zeigt nach +Y
BOARD_W, BOARD_L = 18.0, 33.0
BOARD_Y0 = 2.8        # Board-Anfang (Anschlag)

# Akku 30 x 20 x 6 (liegt quer)
BAT_X, BAT_Y = 32.6, 22.6   # Innenmaß Fach
BAT_CY = -19.3

# JST-PH-Buchse 5.9 x 4.5 x 5.9
JST_IN = (6.3, 4.9)
JST_C = (-24.0, -12.0)

# Schiebeschalter: Körper 10 x 5.5 x 5, Hebel 3 dick, Schlitz 7 x 3.6
SW_L, SW_W, SW_H = 10.0, 5.5, 5.0
SLOT_L, SLOT_H = 7.0, 3.6

# Reset-Taster 6x6x5, kopfüber auf dem Boden
RST_C = (-24.0, 12.0)

# MX
MX_CUT = 14.1
PLATE_T = 1.5

# Deckel
LID_Z = H_BASE                  # 18
LID_T = 3.0                     # Deckelplatte 18..21
LIP_CLEAR = 0.2
LIP_H = 4.0
RING_R_IN, RING_R_OUT, RING_TOP = 25.4, 27.4, 29.0

# Kappe
STEM_TOP = LID_Z + LID_T + 9.0   # gemessen: Kreuz-Oberkante 9 mm, Gehäuse 4.5 mm über Platte
CAP_R = 25.0
CAP_SKIRT_IN = 23.0
CAP_TOP_T = 3.0
CROSS_L, CROSS_W, CROSS_DEPTH = 4.15, 1.3, 3.6
BOSS_R = 2.75


def box(x0, x1, y0, y1, z0, z1):
    return (cq.Workplane("XY")
            .box(x1 - x0, y1 - y0, z1 - z0, centered=False)
            .translate((x0, y0, z0)))


def cyl(r, z0, z1, x=0.0, y=0.0):
    return cq.Workplane("XY").circle(r).extrude(z1 - z0).translate((x, y, z0))


# ================= GEHÄUSE =================
base = cyl(R_OUT, 0, H_BASE).cut(cyl(R_IN, FLOOR, H_BASE + 1))
base = base.faces("<Z").edges().chamfer(1.0)

# Board-Schienen + Anschlag
bx = BOARD_W / 2 + 0.2
rails = (box(bx, bx + 1.5, BOARD_Y0 + 1.2, BOARD_Y0 + BOARD_L - 2, FLOOR, FLOOR + 3)
         .union(box(-bx - 1.5, -bx, BOARD_Y0 + 1.2, BOARD_Y0 + BOARD_L - 2, FLOOR, FLOOR + 3))
         .union(box(-bx - 1.5, bx + 1.5, BOARD_Y0 - 1.5, BOARD_Y0, FLOOR, FLOOR + 3)))
base = base.union(rails)

# USB-C Öffnung
base = base.cut(box(-6, 6, 33, 42, FLOOR, FLOOR + 7))

# Akkufach (Rahmen)
bat_outer = box(-BAT_X / 2 - 1.2, BAT_X / 2 + 1.2, BAT_CY - BAT_Y / 2 - 1.2, BAT_CY + BAT_Y / 2 + 1.2, FLOOR, FLOOR + 4)
bat_inner = box(-BAT_X / 2, BAT_X / 2, BAT_CY - BAT_Y / 2, BAT_CY + BAT_Y / 2, FLOOR, FLOOR + 5)
base = base.union(bat_outer.cut(bat_inner))

# JST-Tasche (Seite Richtung Akku offen)
jx, jy = JST_C
jw, jd = JST_IN
jst = box(jx - jw / 2 - 1, jx + jw / 2 + 1, jy - jd / 2 - 1, jy + jd / 2 + 1, FLOOR, FLOOR + 4)
jst = jst.cut(box(jx - jw / 2, jx + jw / 2 + 2, jy - jd / 2, jy + jd / 2, FLOOR, FLOOR + 5))
base = base.union(jst)

# Schiebeschalter an der +X-Wand: Körper liegt mit der Hebelseite an der Wand
sw_zc = FLOOR + SW_W / 2                     # Hebelmitte in Z
gy = SW_L / 2 + 0.2
guides = (box(R_IN - SW_H - 1.0, R_IN + 1.0, gy, gy + 1.2, FLOOR, FLOOR + SW_W + 1)
          .union(box(R_IN - SW_H - 1.0, R_IN + 1.0, -gy - 1.2, -gy, FLOOR, FLOOR + SW_W + 1)))
base = base.union(guides)
base = base.cut(box(R_IN - 3, R_OUT + 2, -SLOT_L / 2, SLOT_L / 2, sw_zc - SLOT_H / 2, sw_zc + SLOT_H / 2))
# kleine Markierungen neben dem Schlitz außen (Kerben), I-Seite = +Y
mark = box(R_OUT - 0.6, R_OUT + 1, SLOT_L / 2 + 1.5, SLOT_L / 2 + 2.3, sw_zc - 1.8, sw_zc + 1.8)
base = base.cut(mark)

# Büroklammer-Reset: Stufenloch + Halterahmen für 6x6-Taster
rx, ry = RST_C
base = base.cut(cyl(2.0, 0.4, FLOOR + 0.1, rx, ry)).cut(cyl(1.0, -1, FLOOR, rx, ry))
rframe = box(rx - 4.2, rx + 4.2, ry - 4.2, ry + 4.2, FLOOR, FLOOR + 2.5).cut(
    box(rx - 3.2, rx + 3.2, ry - 3.2, ry + 3.2, FLOOR, FLOOR + 3))
base = base.union(rframe)

# Gummifuß-Mulden (10 mm Füße)
for a in (45, 135, 225, 315):
    x, y = 28 * math.cos(math.radians(a)), 28 * math.sin(math.radians(a))
    base = base.cut(cyl(5.2, -1, 1.0, x, y))

# ================= DECKEL =================
lid = cyl(R_OUT, LID_Z, LID_Z + LID_T)
lid = lid.faces(">Z").edges().chamfer(0.8)
lip = cyl(R_IN - LIP_CLEAR, LID_Z - LIP_H, LID_Z).cut(cyl(R_IN - LIP_CLEAR - 2.0, LID_Z - LIP_H - 1, LID_Z + 0.1))
lid = lid.union(lip)
lid = lid.union(cyl(RING_R_OUT, LID_Z + LID_T, RING_TOP).cut(cyl(RING_R_IN, LID_Z, RING_TOP + 1)))
# Switch-Freiraum unten (Platte 1.5) + MX-Ausschnitt
lid = lid.cut(box(-10, 10, -10, 10, LID_Z - 1, LID_Z + LID_T - PLATE_T))
lid = lid.cut(box(-MX_CUT / 2, MX_CUT / 2, -MX_CUT / 2, MX_CUT / 2, LID_Z - 1, LID_Z + LID_T + 1))

# ================= KAPPE =================
ceil_z = STEM_TOP + 0.4
skirt_bottom = LID_Z + LID_T + 4.8          # 4.8 mm Luft bei 4 mm Tastenweg
cap = cyl(CAP_R, ceil_z, ceil_z + CAP_TOP_T)
cap = cap.faces(">Z").edges().fillet(1.2)
cap = cap.union(cyl(CAP_R, skirt_bottom, ceil_z).cut(cyl(CAP_SKIRT_IN, skirt_bottom - 1, ceil_z)))
boss_bottom = STEM_TOP - CROSS_DEPTH
cap = cap.union(cyl(BOSS_R, boss_bottom, ceil_z + 0.01))
cross = (box(-CROSS_L / 2, CROSS_L / 2, -CROSS_W / 2, CROSS_W / 2, boss_bottom - 1, STEM_TOP)
         .union(box(-CROSS_W / 2, CROSS_W / 2, -CROSS_L / 2, CROSS_L / 2, boss_bottom - 1, STEM_TOP)))
cap = cap.cut(cross)

# Mute-Symbol 0.6 mm tief in die Oberseite
top = ceil_z + CAP_TOP_T
icon_d = 0.6
spk = (cq.Workplane("XY").workplane(offset=top - icon_d)
       .polyline([(-13, -4), (-7, -4), (-1, -10), (-1, 10), (-7, 4), (-13, 4)]).close()
       .extrude(icon_d + 1))
x1 = (cq.Workplane("XY").workplane(offset=top - icon_d).center(8, 0)
      .rect(16, 2.4).extrude(icon_d + 1).rotate((8, 0, 0), (8, 0, 1), 45))
x2 = (cq.Workplane("XY").workplane(offset=top - icon_d).center(8, 0)
      .rect(16, 2.4).extrude(icon_d + 1).rotate((8, 0, 0), (8, 0, 1), -45))
cap = cap.cut(spk).cut(x1).cut(x2)

if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "."
    for name, part in (("gehaeuse", base), ("deckel", lid), ("kappe", cap)):
        cq.exporters.export(part, f"{out}/{name}.stl", tolerance=0.02, angularTolerance=0.1)
        cq.exporters.export(part, f"{out}/{name}.step")
        bb = part.val().BoundingBox()
        print(name, "ok", part.val().isValid(), round(part.val().Volume() / 1000, 2), "cm3",
              [round(v, 1) for v in (bb.xmin, bb.ymin, bb.zmin, bb.xmax, bb.ymax, bb.zmax)])
    asm = cq.Assembly().add(base, name="gehaeuse").add(lid, name="deckel").add(cap, name="kappe")
    asm.save(f"{out}/mute_buzzer_komplett.step")
