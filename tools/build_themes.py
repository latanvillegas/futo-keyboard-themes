from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import zipfile, shutil, math, random

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "build"
DIST = ROOT / "dist"
BUILD.mkdir(exist_ok=True)
DIST.mkdir(exist_ok=True)

THEMES = [
    ("amoled-purple-neon", "AMOLED Purple Neon", "#A855F7", "#000000"),
    ("amoled-purple-clean", "AMOLED Purple Clean", "#9333EA", "#000000"),
    ("amoled-purple-cyberpunk", "AMOLED Purple Cyberpunk", "#C084FC", "#000000"),
    ("midnight-aurora", "Midnight Aurora", "#55E8E0", "#000000"),
    ("obsidian-gold", "Obsidian Gold", "#EBC467", "#000000"),
    ("ancient-arcane", "Ancient Arcane", "#D8AA5B", "#000000"),
]

def rgb(hexv):
    hexv=hexv.lstrip('#')
    return tuple(int(hexv[i:i+2],16) for i in (0,2,4))

def key_asset(path, accent, variant="normal", slug=""):
    w,h,S=140,128,4
    im=Image.new("RGBA",(w*S,h*S),(0,0,0,0)); box=(8*S,8*S,(w-8)*S,(h-8)*S); a=rgb(accent)
    if slug == "obsidian-gold":
        fill=(4,4,5,252) if variant=="normal" else ((10,8,7,252) if variant=="functional" else ((112,78,18,245) if variant=="pressed" else (4,4,5,252)))
        glow=Image.new("RGBA",im.size,(0,0,0,0)); gd=ImageDraw.Draw(glow)
        gd.rounded_rectangle(box,16*S,outline=(220,174,80,75),width=5*S); glow=glow.filter(ImageFilter.GaussianBlur(6*S)); im=Image.alpha_composite(im,glow)
        d=ImageDraw.Draw(im); d.rounded_rectangle(box,16*S,fill=fill,outline=(206,165,78,245),width=3*S)
        d.arc((14*S,12*S,(w-14)*S,(h-16)*S),5,175,fill=(255,231,169,115),width=2*S)
        d.line((22*S,(h-18)*S,(w-22)*S,(h-18)*S),fill=(110,73,14,150),width=2*S)
    else:
        fill=(8,8,11,248) if variant=="normal" else ((20,14,26,252) if variant=="functional" else (*a,210))
        glow=Image.new("RGBA",im.size,(0,0,0,0)); gd=ImageDraw.Draw(glow)
        gd.rounded_rectangle(box,20*S,outline=(*a,115),width=6*S); glow=glow.filter(ImageFilter.GaussianBlur(8*S)); im=Image.alpha_composite(im,glow)
        d=ImageDraw.Draw(im); d.rounded_rectangle(box,20*S,fill=fill,outline=(*a,245),width=3*S)
        d.line((28*S,14*S,(w-28)*S,14*S),fill=(255,255,255,45),width=2*S)
    im.resize((w,h),Image.Resampling.LANCZOS).save(path)

def background(path, slug, accent):
    W,H=1440,900; a=rgb(accent); im=Image.new("RGBA",(W,H),(0,0,0,255)); layer=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(layer)
    if slug=="midnight-aurora":
        for j,c in enumerate([(50,220,255),(0,235,215),(145,75,255)]):
            pts=[(x,240+j*120+70*math.sin(x*.003+j)) for x in range(-100,W+100,18)]; d.line(pts,fill=(*c,55),width=100)
    elif slug=="ancient-arcane":
        cx,cy=720,460
        for r in (170,230,290): d.ellipse((cx-r,cy-r,cx+r,cy+r),outline=(*a,65),width=2)
        for ang in range(0,360,30):
            q=math.radians(ang); d.line((cx+170*math.cos(q),cy+170*math.sin(q),cx+290*math.cos(q),cy+290*math.sin(q)),fill=(150,70,210,45),width=1)
    elif slug=="obsidian-gold":
        # Original-style fractured obsidian: bright ivory/gold facets, black shards,
        # diagonal gold seams and fine gold dust. Deterministic for reproducible builds.
        random.seed(2077)
        d.polygon([(0,0),(515,0),(420,230),(95,390),(0,300)],fill=(244,239,222,250))
        d.polygon([(410,0),(1020,0),(930,225),(625,340),(420,230)],fill=(210,202,181,210))
        d.polygon([(95,390),(420,230),(625,340),(510,610),(175,650)],fill=(255,253,243,255))
        d.polygon([(625,340),(930,225),(1165,400),(905,625),(510,610)],fill=(238,232,214,245))
        d.polygon([(1165,400),(1440,300),(1440,720),(1135,610),(905,625)],fill=(255,255,249,255))
        d.polygon([(0,300),(95,390),(175,650),(0,820)],fill=(12,11,10,255))
        d.polygon([(175,650),(510,610),(430,900),(0,900),(0,820)],fill=(2,2,2,255))
        d.polygon([(510,610),(905,625),(780,900),(430,900)],fill=(12,10,8,255))
        d.polygon([(905,625),(1135,610),(1440,720),(1440,900),(780,900)],fill=(1,1,1,255))
        seams=[((0,300),(420,230)),((95,390),(510,610)),((420,230),(625,340)),((625,340),(930,225)),((625,340),(905,625)),((930,225),(1165,400)),((905,625),(1135,610)),((1165,400),(1440,300)),((1135,610),(1440,720)),((175,650),(430,900)),((510,610),(780,900))]
        for p1,p2 in seams:
            d.line((*p1,*p2),fill=(208,166,76,150),width=2)
            d.line((p1[0]+3,p1[1]+3,p2[0]+3,p2[1]+3),fill=(94,62,15,75),width=1)
        for _ in range(95):
            x=random.randrange(W); y=random.randrange(H); r=random.choice((1,1,1,2))
            d.ellipse((x-r,y-r,x+r,y+r),fill=(226,183,84,random.randrange(35,120)))
    else:
        for k in range(-900,1600,120): d.line((k,H,k+900,0),fill=(*a,16),width=2)
    if slug=="midnight-aurora": layer=layer.filter(ImageFilter.GaussianBlur(18))
    Image.alpha_composite(im,layer).convert("RGB").save(path,"WEBP",quality=95)

def theme_text(name, slug, accent):
    gold = slug == "obsidian-gold"
    pc = "#4A3510" if gold else "#32104A"
    opc = "#FFF0C2" if gold else "#F3E8FF"
    sec = "#C9A24D" if gold else accent
    sc = "#392A10" if gold else "#281033"
    tc = "#33250C" if gold else "#25112E"
    sv = "#16130D" if gold else "#17111D"
    osv = "#E9DFC6" if gold else "#E7DBEF"
    outline = "#9D7A35" if gold else "#79548C"
    outlinev = "#51401E" if gold else "#402A4B"
    kc = "#080807" if gold else "#121216"
    kcv = "#171208" if gold else "#1A1022"
    pressed = "#725019" if gold else "#54236C"
    return f'''# FUTO Keyboard Theme Configuration
name = "{name}"
author = "Latan Villegas"
id = "com.latanvillegas.{slug.replace('-', '')}"
version = 3
description = "Original custom FUTO Keyboard theme by Latan Villegas."

[options]
auto_borders = true
center_hints = false
roundedness = 1
scale_text = 1
scale_hints = 1
weight_text = 400
weight_hints = 500

[colors]
primary = "{accent}"
on_primary = "#FFFFFF"
primary_container = "{pc}"
on_primary_container = "{opc}"
inverse_primary = "{sec}"
secondary = "{sec}"
on_secondary = "#FFFFFF"
secondary_container = "{sc}"
on_secondary_container = "#F7E8C3"
tertiary = "{accent}"
on_tertiary = "#FFFFFF"
tertiary_container = "{tc}"
on_tertiary_container = "#FFF1C8"
background = "#000000"
on_background = "#FFFFFF"
surface = "#000000"
on_surface = "#FFFFFF"
surface_variant = "{sv}"
on_surface_variant = "{osv}"
surface_tint = "{accent}"
inverse_surface = "#F5F0E6"
inverse_on_surface = "#17130C"
error = "#FF5252"
on_error = "#000000"
error_container = "#5C1010"
on_error_container = "#FFDAD6"
outline = "{outline}"
outline_variant = "{outlinev}"
scrim = "#000000"
surface_bright = "#211D15"
surface_dim = "#000000"
surface_container = "#090806"
surface_container_high = "#100E0A"
surface_container_highest = "#17140E"
surface_container_low = "#050403"
surface_container_lowest = "#000000"
keyboard_surface = "#000000"
keyboard_surface_dim = "#000000"
keyboard_container = "{kc}"
keyboard_container_variant = "{kcv}"
on_keyboard_container = "#FFFFFF"
keyboard_press = "{accent}"
keyboard_container_pressed = "{pressed}"
on_keyboard_container_pressed = "#FFFFFF"

[options.background]
image = "background.webp"
opacity = 1
action_bar_opacity = 0.82
cropping = [0, 0, 1, 1]

[[matchrules.border]]
selector = "pressed"
asset = "pressed.png"
[[matchrules.border]]
selector = "normal"
asset = "normal.png"
[[matchrules.border]]
selector = "spacebar"
asset = "normal.png"
[[matchrules.border]]
selector = "action"
asset = "action.png"
[[matchrules.border]]
selector = "functional"
asset = "functional.png"

[[asset.border]]
name = "normal.png"
background_tint = "#FFFFFF"
foreground_tint = "#FFFFFF"
padding = [0, 0, 0, 0]
slicing = [0.28, 0.28, 0.72, 0.72]
gap = [1, 1, 1, 1]
target_density = 320
[[asset.border]]
name = "functional.png"
background_tint = "#FFFFFF"
foreground_tint = "#FFFFFF"
padding = [0, 0, 0, 0]
slicing = [0.28, 0.28, 0.72, 0.72]
gap = [1, 1, 1, 1]
target_density = 320
[[asset.border]]
name = "pressed.png"
background_tint = "#FFFFFF"
foreground_tint = "#FFFFFF"
padding = [0, 0, 0, 0]
slicing = [0.28, 0.28, 0.72, 0.72]
gap = [1, 1, 1, 1]
target_density = 320
[[asset.border]]
name = "action.png"
background_tint = "#FFFFFF"
foreground_tint = "#FFFFFF"
padding = [0, 0, 0, 0]
slicing = [0.28, 0.28, 0.72, 0.72]
gap = [1, 1, 1, 1]
target_density = 320
'''

def build(slug,name,accent,bg):
    out=BUILD/slug
    if out.exists(): shutil.rmtree(out)
    out.mkdir(parents=True); background(out/"background.webp",slug,accent)
    key_asset(out/"normal.png",accent,"normal",slug); key_asset(out/"functional.png",accent,"functional",slug); key_asset(out/"pressed.png",accent,"pressed",slug); key_asset(out/"action.png",accent,"pressed",slug)
    (out/"theme.txt").write_text(theme_text(name,slug,accent),encoding="utf-8")
    (out/"LICENSE.txt").write_text("Copyright (c) 2026 Latan Villegas. Personal non-commercial use permitted. Third-party components retain their original licenses.\n",encoding="utf-8")
    zpath=DIST/f"{slug}-FUTO.zip"
    with zipfile.ZipFile(zpath,"w",zipfile.ZIP_DEFLATED) as z:
        for p in out.rglob("*"):
            if p.is_file(): z.write(p,p.relative_to(out).as_posix())
    print(zpath)

for item in THEMES: build(*item)
