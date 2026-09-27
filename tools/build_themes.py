from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import zipfile, shutil, math, random

ROOT=Path(__file__).resolve().parents[1]; BUILD=ROOT/'build'; DIST=ROOT/'dist'; BUILD.mkdir(exist_ok=True); DIST.mkdir(exist_ok=True)
THEMES=[
('amoled-purple-neon','AMOLED Purple Neon','#A855F7'),('amoled-purple-clean','AMOLED Purple Clean','#9333EA'),('amoled-purple-cyberpunk','AMOLED Purple Cyberpunk','#C084FC'),('midnight-aurora','Midnight Aurora','#55E8E0'),('obsidian-gold','Obsidian Gold','#EBC467'),('ancient-arcane','Ancient Arcane','#D8AA5B'),('rose-quartz','Rose Quartz','#F3A6C8'),
('crystal-sakura','Crystal Sakura','#FF9FC5'),('emerald-glass','Emerald Glass','#4DE6A8'),('ocean-glass','Ocean Glass','#43D9E8'),('pearl-holographic','Pearl Holographic','#D6B8FF'),('midnight-chrome','Midnight Chrome','#C7D0DB'),('matcha-zen','Matcha Zen','#A8C98B'),('cherry-noir','Cherry Noir','#E24467'),('lavender-dream','Lavender Dream','#B89CFF'),('champagne-silk','Champagne Silk','#E9C98B'),('cyber-ice','Cyber Ice','#8CEBFF')]
MODERN={x[0] for x in THEMES[7:]}

def rgb(h): h=h.lstrip('#'); return tuple(int(h[i:i+2],16) for i in (0,2,4))
def mix(a,b,t): return tuple(int(a[i]*(1-t)+b[i]*t) for i in range(3))

def key_asset(path,accent,variant,slug):
    w,h,S=140,128,4; a=rgb(accent); im=Image.new('RGBA',(w*S,h*S),(0,0,0,0)); box=(8*S,8*S,(w-8)*S,(h-8)*S)
    glass=slug in {'crystal-sakura','emerald-glass','ocean-glass','pearl-holographic','lavender-dream','cyber-ice','rose-quartz'}
    warm=slug in {'obsidian-gold','champagne-silk','matcha-zen'}
    base=mix((5,5,7),a,.08 if glass else .04); fill=(*base,225 if glass else 248)
    if variant=='functional': fill=(*mix(base,a,.13),240)
    if variant=='pressed': fill=(*mix(base,a,.52),248)
    glow=Image.new('RGBA',im.size,(0,0,0,0)); gd=ImageDraw.Draw(glow); rad=(23 if glass else 16)*S
    gd.rounded_rectangle(box,rad,outline=(*a,105 if glass else 70),width=(6 if glass else 4)*S); glow=glow.filter(ImageFilter.GaussianBlur((9 if glass else 5)*S)); im=Image.alpha_composite(im,glow)
    d=ImageDraw.Draw(im); d.rounded_rectangle(box,rad,fill=fill,outline=(*mix(a,(255,255,255),.2 if glass else 0),235),width=(2 if glass else 3)*S)
    if glass: d.arc((14*S,12*S,(w-14)*S,(h-18)*S),190,345,fill=(255,255,255,105),width=2*S)
    elif warm: d.line((24*S,15*S,(w-24)*S,15*S),fill=(255,246,220,70),width=2*S)
    im.resize((w,h),Image.Resampling.LANCZOS).save(path)

def background(path,slug,accent):
    W,H=1440,900; a=rgb(accent); im=Image.new('RGBA',(W,H),(0,0,0,255)); l=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(l); random.seed(sum(map(ord,slug)))
    if slug=='obsidian-gold':
        polys=[([(0,0),(515,0),(420,230),(95,390),(0,300)],(244,239,222,250)), ([(410,0),(1020,0),(930,225),(625,340),(420,230)],(210,202,181,210)), ([(95,390),(420,230),(625,340),(510,610),(175,650)],(255,253,243,255)), ([(625,340),(930,225),(1165,400),(905,625),(510,610)],(238,232,214,245)), ([(1165,400),(1440,300),(1440,720),(1135,610),(905,625)],(255,255,249,255)), ([(0,300),(95,390),(175,650),(0,820)],(12,11,10,255)), ([(175,650),(510,610),(430,900),(0,900),(0,820)],(2,2,2,255)), ([(510,610),(905,625),(780,900),(430,900)],(12,10,8,255)), ([(905,625),(1135,610),(1440,720),(1440,900),(780,900)],(1,1,1,255))]
        for p,c in polys:d.polygon(p,fill=c)
    elif slug in {'crystal-sakura','rose-quartz'}:
        for j,(y,c) in enumerate([(180,(255,142,190)),(470,(205,104,166)),(720,(255,216,230))]): d.line([(x,y+85*math.sin(x*.004+j)) for x in range(-100,W+100,18)],fill=(*c,35),width=120)
        if slug=='crystal-sakura':
            for _ in range(42):
                x=random.randrange(W);y=random.randrange(H);r=random.randrange(3,8);d.ellipse((x-r*2,y-r,x+r*2,y+r),fill=(255,174,207,random.randrange(35,90)))
    elif slug in {'emerald-glass','ocean-glass','lavender-dream','cyber-ice','midnight-aurora'}:
        palettes={'emerald-glass':[(30,210,145),(75,245,190),(10,95,70)],'ocean-glass':[(20,150,255),(45,235,220),(20,80,180)],'lavender-dream':[(178,140,255),(240,145,255),(80,130,255)],'cyber-ice':[(120,235,255),(230,250,255),(40,150,255)],'midnight-aurora':[(50,220,255),(0,235,215),(145,75,255)]}
        for j,c in enumerate(palettes[slug]): d.line([(x,210+j*190+75*math.sin(x*.003+j)) for x in range(-100,W+100,18)],fill=(*c,48),width=115)
        l=l.filter(ImageFilter.GaussianBlur(20))
    elif slug=='pearl-holographic':
        for x,y,r,c in [(280,260,300,(255,160,210)),(720,510,350,(145,220,255)),(1160,260,310,(205,165,255))]: d.ellipse((x-r,y-r,x+r,y+r),fill=(*c,32))
        l=l.filter(ImageFilter.GaussianBlur(55))
    elif slug=='midnight-chrome':
        for k in range(-400,1800,260): d.polygon([(k,0),(k+170,0),(k-180,H),(k-350,H)],fill=(205,220,235,18)); d.line((k,0,k-350,H),fill=(220,235,255,55),width=2)
    elif slug=='matcha-zen':
        for x,y,r in [(180,220,260),(1200,650,340),(750,350,190)]: d.ellipse((x-r,y-r,x+r,y+r),outline=(150,190,125,35),width=24)
        for k in range(0,W,110): d.arc((k-200,180,k+320,820),210,330,fill=(190,215,165,28),width=2)
    elif slug=='cherry-noir':
        for x,y,r in [(220,210,190),(1180,680,280)]: d.ellipse((x-r,y-r,x+r,y+r),fill=(145,10,45,42))
        for _ in range(70): x=random.randrange(W);y=random.randrange(H);d.ellipse((x,y,x+2,y+2),fill=(230,55,90,random.randrange(25,90)))
    elif slug=='champagne-silk':
        for j in range(3): d.line([(x,260+j*210+65*math.sin(x*.0035+j)) for x in range(-100,W+100,16)],fill=(235,202,140,32-j*5),width=100)
        l=l.filter(ImageFilter.GaussianBlur(14))
    elif slug=='ancient-arcane':
        cx,cy=720,460
        for r in (170,230,290):d.ellipse((cx-r,cy-r,cx+r,cy+r),outline=(*a,65),width=2)
    else:
        for k in range(-900,1600,120):d.line((k,H,k+900,0),fill=(*a,16),width=2)
    for _ in range(45 if slug in MODERN else 15):
        x=random.randrange(W);y=random.randrange(H);r=random.choice((1,1,2));d.ellipse((x-r,y-r,x+r,y+r),fill=(*mix(a,(255,255,255),.35),random.randrange(20,75)))
    Image.alpha_composite(im,l).convert('RGB').save(path,'WEBP',quality=95)

def theme_text(name,slug,accent):
    a=rgb(accent); pc='#%02X%02X%02X'%mix((0,0,0),a,.34); sc='#%02X%02X%02X'%mix((0,0,0),a,.24); tc='#%02X%02X%02X'%mix((0,0,0),a,.20); sv='#%02X%02X%02X'%mix((4,4,6),a,.10); out='#%02X%02X%02X'%mix(a,(255,255,255),.10); outv='#%02X%02X%02X'%mix((0,0,0),a,.32); kc='#%02X%02X%02X'%mix((3,3,5),a,.055); kcv='#%02X%02X%02X'%mix((4,4,6),a,.13); pressed='#%02X%02X%02X'%mix((0,0,0),a,.50)
    return f'''# FUTO Keyboard Theme Configuration
name = "{name}"
author = "Latan Villegas"
id = "com.latanvillegas.{slug.replace('-','')}"
version = 4
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
on_primary_container = "#FFFFFF"
inverse_primary = "{accent}"
secondary = "{accent}"
on_secondary = "#FFFFFF"
secondary_container = "{sc}"
on_secondary_container = "#FFFFFF"
tertiary = "{accent}"
on_tertiary = "#FFFFFF"
tertiary_container = "{tc}"
on_tertiary_container = "#FFFFFF"
background = "#000000"
on_background = "#FFFFFF"
surface = "#000000"
on_surface = "#FFFFFF"
surface_variant = "{sv}"
on_surface_variant = "#EEE8EE"
surface_tint = "{accent}"
inverse_surface = "#F5F2F5"
inverse_on_surface = "#171317"
error = "#FF5252"
on_error = "#000000"
error_container = "#5C1010"
on_error_container = "#FFDAD6"
outline = "{out}"
outline_variant = "{outv}"
scrim = "#000000"
surface_bright = "#211D21"
surface_dim = "#000000"
surface_container = "#090709"
surface_container_high = "#100D10"
surface_container_highest = "#181318"
surface_container_low = "#050405"
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
cropping = [0,0,1,1]

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
padding = [0,0,0,0]
slicing = [0.28,0.28,0.72,0.72]
gap = [1,1,1,1]
target_density = 320
[[asset.border]]
name = "functional.png"
background_tint = "#FFFFFF"
foreground_tint = "#FFFFFF"
padding = [0,0,0,0]
slicing = [0.28,0.28,0.72,0.72]
gap = [1,1,1,1]
target_density = 320
[[asset.border]]
name = "pressed.png"
background_tint = "#FFFFFF"
foreground_tint = "#FFFFFF"
padding = [0,0,0,0]
slicing = [0.28,0.28,0.72,0.72]
gap = [1,1,1,1]
target_density = 320
[[asset.border]]
name = "action.png"
background_tint = "#FFFFFF"
foreground_tint = "#FFFFFF"
padding = [0,0,0,0]
slicing = [0.28,0.28,0.72,0.72]
gap = [1,1,1,1]
target_density = 320
'''

def build(slug,name,accent):
    out=BUILD/slug
    if out.exists():shutil.rmtree(out)
    out.mkdir(parents=True);background(out/'background.webp',slug,accent)
    for fn,v in [('normal.png','normal'),('functional.png','functional'),('pressed.png','pressed'),('action.png','pressed')]:key_asset(out/fn,accent,v,slug)
    (out/'theme.txt').write_text(theme_text(name,slug,accent),encoding='utf-8')
    (out/'LICENSE.txt').write_text('Copyright (c) 2026 Latan Villegas. Personal non-commercial use permitted. Third-party components retain their original licenses.\n',encoding='utf-8')
    if slug in MODERN or slug=='rose-quartz':(out/'CREDITS.txt').write_text(f'{name} theme design and original visual assets: Latan Villegas.\nTypography: FUTO/system font in this build. Any future third-party font will retain its original license and attribution.\n',encoding='utf-8')
    z=DIST/f'{slug}-FUTO.zip'
    with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as q:
        for p in out.rglob('*'):
            if p.is_file():q.write(p,p.relative_to(out).as_posix())
    print(z)
for item in THEMES:build(*item)
