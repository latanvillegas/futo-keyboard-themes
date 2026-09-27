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

def key_asset(path, accent, variant="normal"):
    w,h,S=140,128,4
    im=Image.new("RGBA",(w*S,h*S),(0,0,0,0))
    box=(8*S,8*S,(w-8)*S,(h-8)*S)
    a=rgb(accent)
    fill=(8,8,11,248) if variant=="normal" else ((20,14,26,252) if variant=="functional" else (*a,210))
    glow=Image.new("RGBA",im.size,(0,0,0,0)); gd=ImageDraw.Draw(glow)
    gd.rounded_rectangle(box,20*S,outline=(*a,115),width=6*S)
    glow=glow.filter(ImageFilter.GaussianBlur(8*S)); im=Image.alpha_composite(im,glow)
    d=ImageDraw.Draw(im)
    d.rounded_rectangle(box,20*S,fill=fill,outline=(*a,245),width=3*S)
    d.line((28*S,14*S,(w-28)*S,14*S),fill=(255,255,255,45),width=2*S)
    im.resize((w,h),Image.Resampling.LANCZOS).save(path)

def background(path, slug, accent):
    W,H=1440,900; a=rgb(accent)
    im=Image.new("RGBA",(W,H),(0,0,0,255)); layer=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(layer)
    if slug=="midnight-aurora":
        colors=[(50,220,255),(0,235,215),(145,75,255)]
        for j,c in enumerate(colors):
            pts=[]
            for x in range(-100,W+100,18): pts.append((x,240+j*120+70*math.sin(x*.003+j)))
            d.line(pts,fill=(*c,55),width=100)
    elif slug=="ancient-arcane":
        cx,cy=720,460
        for r in (170,230,290): d.ellipse((cx-r,cy-r,cx+r,cy+r),outline=(*a,65),width=2)
        for ang in range(0,360,30):
            q=math.radians(ang); d.line((cx+170*math.cos(q),cy+170*math.sin(q),cx+290*math.cos(q),cy+290*math.sin(q)),fill=(150,70,210,45),width=1)
    elif slug=="obsidian-gold":
        d.polygon([(0,250),(480,80),(750,430),(180,610)],fill=(255,255,255,13))
        d.line((0,720,520,210),fill=(*a,50),width=2)
    else:
        for k in range(-900,1600,120): d.line((k,H,k+900,0),fill=(*a,16),width=2)
    layer=layer.filter(ImageFilter.GaussianBlur(18 if slug=="midnight-aurora" else 1))
    im=Image.alpha_composite(im,layer); im.convert("RGB").save(path,"WEBP",quality=94)

def theme_text(name, slug, accent):
    return f'''# FUTO Keyboard Theme Configuration\nname = "{name}"\nauthor = "Latan Villegas"\nid = "com.latanvillegas.{slug.replace('-', '')}"\nversion = 1\ndescription = "Custom FUTO Keyboard theme by Latan Villegas."\n\n[options]\nauto_borders = true\ncenter_hints = false\nroundedness = 1\nscale_text = 1\nscale_hints = 1\nweight_text = 400\nweight_hints = 500\n\n[colors]\nprimary = "{accent}"\non_primary = "#FFFFFF"\nbackground = "#000000"\non_background = "#FFFFFF"\nsurface = "#000000"\non_surface = "#FFFFFF"\nkeyboard_surface = "#000000"\nkeyboard_container = "#0A0A0D"\non_keyboard_container = "#FFFFFF"\nkeyboard_press = "{accent}"\nkeyboard_container_pressed = "{accent}"\non_keyboard_container_pressed = "#FFFFFF"\n\n[options.background]\nimage = "background.webp"\nopacity = 1\naction_bar_opacity = 0.82\ncropping = [0, 0, 1, 1]\n\n[[matchrules.border]]\nselector = "pressed"\nasset = "pressed.png"\n[[matchrules.border]]\nselector = "normal"\nasset = "normal.png"\n[[matchrules.border]]\nselector = "spacebar"\nasset = "normal.png"\n[[matchrules.border]]\nselector = "action"\nasset = "action.png"\n[[matchrules.border]]\nselector = "functional"\nasset = "functional.png"\n\n[[asset.border]]\nname = "normal.png"\nslicing = [0.28, 0.28, 0.72, 0.72]\ntarget_density = 320\n[[asset.border]]\nname = "functional.png"\nslicing = [0.28, 0.28, 0.72, 0.72]\ntarget_density = 320\n[[asset.border]]\nname = "pressed.png"\nslicing = [0.28, 0.28, 0.72, 0.72]\ntarget_density = 320\n[[asset.border]]\nname = "action.png"\nslicing = [0.28, 0.28, 0.72, 0.72]\ntarget_density = 320\n'''

def build(slug,name,accent,bg):
    out=BUILD/slug
    if out.exists(): shutil.rmtree(out)
    out.mkdir(parents=True)
    background(out/"background.webp",slug,accent)
    key_asset(out/"normal.png",accent,"normal")
    key_asset(out/"functional.png",accent,"functional")
    key_asset(out/"pressed.png",accent,"pressed")
    key_asset(out/"action.png",accent,"pressed")
    (out/"theme.txt").write_text(theme_text(name,slug,accent),encoding="utf-8")
    (out/"LICENSE.txt").write_text("Copyright (c) 2026 Latan Villegas. Personal non-commercial use permitted. Third-party components retain their original licenses.\n",encoding="utf-8")
    zpath=DIST/f"{slug}-FUTO.zip"
    with zipfile.ZipFile(zpath,"w",zipfile.ZIP_DEFLATED) as z:
        for p in out.rglob("*"):
            if p.is_file(): z.write(p,p.relative_to(out).as_posix())
    print(zpath)

for item in THEMES: build(*item)
