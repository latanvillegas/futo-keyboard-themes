from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import urllib.request, zipfile, shutil

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "build" / "velvet-editorial"
DIST = ROOT / "dist"
shutil.rmtree(OUT, ignore_errors=True)
OUT.mkdir(parents=True, exist_ok=True)
DIST.mkdir(exist_ok=True)

FONT = "CormorantGaramond-Regular.ttf"
FONT_URL = "https://raw.githubusercontent.com/google/fonts/main/ofl/cormorantgaramond/CormorantGaramond%5Bwght%5D.ttf"
OFL_URL = "https://raw.githubusercontent.com/google/fonts/main/ofl/cormorantgaramond/OFL.txt"

# Background: matte black-plum velvet with editorial copper/rose accents.
W, H = 1440, 900
im = Image.new("RGB", (W, H), (10, 3, 9))
ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(ov)
d.ellipse((860, -260, 1600, 480), fill=(122, 39, 78, 78))
d.ellipse((-300, 470, 520, 1250), fill=(72, 18, 48, 82))
for x in range(-400, W + 400, 88):
    d.line((x, 0, x - 430, H), fill=(255, 218, 224, 10), width=2)
d.rectangle((74, 64, 81, H - 64), fill=(201, 138, 166, 135))
d.rectangle((94, 64, 98, H - 64), fill=(229, 185, 145, 90))
ov = ov.filter(ImageFilter.GaussianBlur(3))
im = Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB")
im.save(OUT / "background.webp", "WEBP", quality=94, method=6)

# Low-resolution 9-slice borders, following FUTO editor guidance (~128x140).
def border(name, fill, outline, highlight=True):
    w, h, s = 128, 140, 4
    a = Image.new("RGBA", (w*s, h*s), (0,0,0,0)); q = ImageDraw.Draw(a)
    box = (7*s, 7*s, (w-7)*s, (h-7)*s)
    q.rounded_rectangle(box, 17*s, fill=fill, outline=outline, width=2*s)
    if highlight:
        q.line((21*s, 18*s, (w-21)*s, 18*s), fill=(255,235,228,82), width=2*s)
    a.resize((w,h), Image.Resampling.LANCZOS).save(OUT / name)

border("normal.png", (28,9,21,246), (201,138,166,235))
border("functional.png", (46,14,34,250), (176,106,137,245))
border("action.png", (126,55,87,255), (235,187,155,255))
border("pressed.png", (168,95,128,255), (255,220,196,255))
border("popup.png", (63,20,45,255), (235,187,155,255))

# Google Fonts asset + original OFL license. Variable font bytes are stored under a
# stable theme filename; FUTO consumes the TTF as an Other Asset via [options.font].
try:
    urllib.request.urlretrieve(FONT_URL, OUT / FONT)
    urllib.request.urlretrieve(OFL_URL, OUT / "OFL-CormorantGaramond.txt")
except Exception as e:
    raise SystemExit(f"Could not download licensed Google Font: {e}")

colors = {
"primary":"#C98AA6","on_primary":"#160A10","primary_container":"#70344F","on_primary_container":"#FFE8F0",
"inverse_primary":"#E8A9C4","secondary":"#E5B98F","on_secondary":"#24150B","secondary_container":"#563C29","on_secondary_container":"#FFE9D6",
"tertiary":"#E9D7C9","on_tertiary":"#231A16","tertiary_container":"#4A3830","on_tertiary_container":"#FBEADF",
"background":"#0A0309","on_background":"#FFF1EA","surface":"#0A0309","on_surface":"#FFF1EA","surface_variant":"#2A101F","on_surface_variant":"#F2D9E2",
"surface_tint":"#C98AA6","inverse_surface":"#FFF1EA","inverse_on_surface":"#26151D","error":"#FFB4AB","on_error":"#690005","error_container":"#93000A","on_error_container":"#FFDAD6",
"outline":"#B98A9F","outline_variant":"#5D3D4B","scrim":"#000000","surface_bright":"#35202A","surface_dim":"#0A0309","surface_container":"#190A12",
"surface_container_high":"#24101B","surface_container_highest":"#311725","surface_container_low":"#12070D","surface_container_lowest":"#050103",
"keyboard_surface":"#0A0309","keyboard_surface_dim":"#070206","keyboard_container":"#1C0915","keyboard_container_variant":"#351426","on_keyboard_container":"#FFF1EA",
"keyboard_press":"#D79AB5","keyboard_container_pressed":"#A85F80","on_keyboard_container_pressed":"#FFFFFF"
}

lines = [
'# FUTO Keyboard Theme Configuration',
'name = "Velvet Editorial"',
'author = "Latan Villegas"',
'id = "com.latanvillegas.velveteditorial"',
'version = 1',
'description = "Modern velvet editorial theme with licensed Google Font, custom 9-slice borders and original visual assets."',
'', '[options]', 'auto_borders = true', 'center_hints = false', 'roundedness = 0.82', 'scale_text = 1.03', 'scale_hints = 0.92', 'weight_text = 500', 'weight_hints = 500',
'', '[colors]']
for k,v in colors.items(): lines.append(f'{k} = "{v}"')
lines += ['', '[options.font]', f'font = "{FONT}"', '', '[options.background]', 'image = "background.webp"', 'opacity = 1.0', 'action_bar_opacity = 0.84', 'cropping = [0, 0, 1, 1]']
# Specific rules first; FUTO applies only the first matching rule.
rules = [('pressed','pressed.png'),('popup','popup.png'),('action','action.png'),('functional','functional.png'),('spacebar','normal.png'),('normal','normal.png')]
for sel,asset in rules:
    lines += ['', '[[matchrules.border]]', f'selector = "{sel}"', f'asset = "{asset}"']
for asset in ['normal.png','functional.png','action.png','pressed.png','popup.png']:
    lines += ['', '[[asset.border]]', f'name = "{asset}"', 'background_tint = "#FFFFFFFF"', 'foreground_tint = "#FFFFFFFF"', 'padding = [0.055, 0.05, 0.945, 0.95]', 'slicing = [0.28, 0.28, 0.72, 0.72]', 'gap = [0.02, 0.02, 0.98, 0.98]', 'target_density = 320']
(OUT / 'theme.txt').write_text('\n'.join(lines) + '\n', encoding='utf-8')
(OUT / 'CREDITS.txt').write_text('Velvet Editorial\nTheme design and original visual assets: Latan Villegas\nTypography: Cormorant Garamond from Google Fonts. Original font authors and OFL license are preserved in OFL-CormorantGaramond.txt.\n', encoding='utf-8')
(OUT / 'LICENSE.txt').write_text('Velvet Editorial theme design and original visual assets: Copyright (c) 2026 Latan Villegas. Permission is granted to use, copy, modify and redistribute with attribution. Third-party components retain their original licenses.\n', encoding='utf-8')

z = DIST / 'velvet-editorial-FUTO.zip'
z.unlink(missing_ok=True)
with zipfile.ZipFile(z, 'w', zipfile.ZIP_DEFLATED) as f:
    for p in OUT.iterdir():
        if p.is_file(): f.write(p, p.name)
print(z)
