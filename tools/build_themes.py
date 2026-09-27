from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import zipfile, shutil, math, random
ROOT=Path(__file__).resolve().parents[1]; BUILD=ROOT/'build'; DIST=ROOT/'dist'; BUILD.mkdir(exist_ok=True); DIST.mkdir(exist_ok=True)
THEMES=[
('amoled-purple-neon','AMOLED Purple Neon','#A855F7'),('amoled-purple-clean','AMOLED Purple Clean','#9333EA'),('amoled-purple-cyberpunk','AMOLED Purple Cyberpunk','#C084FC'),('midnight-aurora','Midnight Aurora','#55E8E0'),('obsidian-gold','Obsidian Gold','#EBC467'),('ancient-arcane','Ancient Arcane','#D8AA5B'),('rose-quartz','Rose Quartz','#F3A6C8'),
('crystal-sakura','Crystal Sakura','#FF9FC5'),('emerald-glass','Emerald Glass','#4DE6A8'),('ocean-glass','Ocean Glass','#43D9E8'),('pearl-holographic','Pearl Holographic','#D6B8FF'),('midnight-chrome','Midnight Chrome','#C7D0DB'),('matcha-zen','Matcha Zen','#A8C98B'),('cherry-noir','Cherry Noir','#E24467'),('lavender-dream','Lavender Dream','#B89CFF'),('champagne-silk','Champagne Silk','#E9C98B'),('cyber-ice','Cyber Ice','#8CEBFF'),
('paper-ink','Paper Ink','#C94B45'),('retro-terminal-84','Retro Terminal 84','#6CFF78'),('concrete-brutalist','Concrete Brutalist','#FF7139'),('porcelain-blue','Porcelain Blue','#2255A4'),('coffee-atelier','Coffee Atelier','#B97850'),('solar-punk','Solar Punk','#D8E85B'),('memphis-pop','Memphis Pop','#FF695E'),('blueprint-architect','Blueprint Architect','#79C7FF'),('japanese-minimal','Japanese Minimal','#E8493F'),('bauhaus-26','Bauhaus 26','#E84736'),('clay-soft','Clay Soft','#E99675'),('carbon-motorsport','Carbon Motorsport','#F04444'),('nordic-snow','Nordic Snow','#7BAAC7'),('comic-pop','Comic Pop','#FFD83D'),('desert-dune','Desert Dune','#D7834D'),('analog-synth','Analog Synth','#F09A45'),('stained-glass','Stained Glass','#4D7BDB'),('newspaper-noir','Newspaper Noir','#D9D9D9'),('pixel-garden','Pixel Garden','#76C76B'),('origami','Origami','#EE776D')]
NEW={x[0] for x in THEMES[17:]}; GLASS={'crystal-sakura','emerald-glass','ocean-glass','pearl-holographic','lavender-dream','cyber-ice','rose-quartz'}
def rgb(h):h=h.lstrip('#');return tuple(int(h[i:i+2],16) for i in (0,2,4))
def mix(a,b,t):return tuple(int(a[i]*(1-t)+b[i]*t) for i in range(3))
def key_asset(path,accent,variant,slug):
 w,h,S=140,128,4;a=rgb(accent);im=Image.new('RGBA',(w*S,h*S),(0,0,0,0));d=ImageDraw.Draw(im);box=(8*S,8*S,(w-8)*S,(h-8)*S)
 square=slug in {'retro-terminal-84','concrete-brutalist','blueprint-architect','bauhaus-26','comic-pop','analog-synth','pixel-garden'}; light=slug in {'paper-ink','porcelain-blue','nordic-snow','newspaper-noir','japanese-minimal','origami'}
 base=(238,235,225) if light else mix((5,5,7),a,.07); fill=base if variant=='normal' else (mix(base,a,.13) if variant=='functional' else mix(base,a,.48)); rad=(2 if square else (24 if slug in GLASS or slug in {'clay-soft','coffee-atelier'} else 13))*S
 if slug=='carbon-motorsport':
  d.rounded_rectangle(box,8*S,fill=(10,10,11,255),outline=(*a,235),width=3*S)
  for k in range(12,w,18):d.line((k*S,10*S,(k+25)*S,(h-10)*S),fill=(255,255,255,12),width=3*S)
 elif slug=='stained-glass':
  d.rounded_rectangle(box,8*S,fill=(*mix((5,5,10),a,.20),250),outline=(25,25,28,255),width=6*S);d.line((20*S,18*S,(w-18)*S,(h-22)*S),fill=(15,15,18,220),width=3*S)
 elif slug=='clay-soft':
  d.rounded_rectangle((10*S,13*S,(w-6)*S,(h-5)*S),25*S,fill=(60,30,22,90));d.rounded_rectangle(box,25*S,fill=(*fill,255),outline=(*mix(a,(255,255,255),.35),230),width=2*S)
 else:d.rounded_rectangle(box,rad,fill=(*fill,235 if slug in GLASS else 255),outline=(*a,235),width=(2 if slug in GLASS else 3)*S)
 if light:d.line((20*S,16*S,(w-20)*S,16*S),fill=(255,255,255,110),width=2*S)
 im.resize((w,h),Image.Resampling.LANCZOS).save(path)
def background(path,slug,accent):
 W,H=1440,900;a=rgb(accent); light=slug in {'paper-ink','porcelain-blue','nordic-snow','newspaper-noir','japanese-minimal','origami'}; im=Image.new('RGBA',(W,H),(245,242,232,255) if light else (0,0,0,255));l=Image.new('RGBA',(W,H),(0,0,0,0));d=ImageDraw.Draw(l);random.seed(sum(map(ord,slug)))
 if slug=='obsidian-gold':
  for p,c in [([(0,0),(515,0),(420,230),(95,390),(0,300)],(244,239,222,250)), ([(95,390),(420,230),(625,340),(510,610),(175,650)],(255,253,243,255)), ([(510,610),(905,625),(780,900),(430,900)],(12,10,8,255))]:d.polygon(p,fill=c)
 elif slug in {'crystal-sakura','rose-quartz','champagne-silk'}:
  for j in range(3):d.line([(x,200+j*230+80*math.sin(x*.004+j)) for x in range(-100,W+100,18)],fill=(*a,35),width=120)
 elif slug in {'emerald-glass','ocean-glass','lavender-dream','cyber-ice','midnight-aurora'}:
  for j in range(3):d.line([(x,180+j*220+75*math.sin(x*.003+j)) for x in range(-100,W+100,18)],fill=(*mix(a,(100+50*j,220,255),.35),45),width=110)
  l=l.filter(ImageFilter.GaussianBlur(20))
 elif slug=='pearl-holographic':
  for x,y,c in [(280,260,(255,160,210)),(720,510,(145,220,255)),(1160,260,(205,165,255))]:d.ellipse((x-300,y-300,x+300,y+300),fill=(*c,35));l=l.filter(ImageFilter.GaussianBlur(50))
 elif slug=='paper-ink':
  for y in range(90,H,54):d.line((60,y,W-60,y),fill=(55,45,40,18),width=1)
  d.rectangle((90,110,105,790),fill=(*a,190))
 elif slug=='retro-terminal-84':
  for y in range(0,H,6):d.line((0,y,W,y),fill=(80,255,95,18),width=1)
  d.rectangle((55,55,W-55,H-55),outline=(*a,70),width=2)
 elif slug=='concrete-brutalist':
  for _ in range(900):x=random.randrange(W);y=random.randrange(H);v=random.randrange(20,65);d.point((x,y),fill=(v,v,v,90))
  d.rectangle((0,650,W,665),fill=(*a,160))
 elif slug=='porcelain-blue':
  for cx,cy in [(250,220),(1120,650)]:
   for r in range(60,240,45):d.arc((cx-r,cy-r,cx+r,cy+r),10,310,fill=(*a,95),width=3)
 elif slug=='coffee-atelier':
  for r in (120,170,225):d.ellipse((180-r,180-r,180+r,180+r),outline=(150,90,55,35),width=8)
  d.arc((750,120,1450,820),80,280,fill=(*a,50),width=35)
 elif slug=='solar-punk':
  for x,y,r in [(180,170,95),(1180,650,140),(760,300,75)]:
   d.ellipse((x-r,y-r,x+r,y+r),outline=(105,190,80,75),width=10);d.line((x,y+r,x+60,y+r+100),fill=(*a,80),width=5)
 elif slug=='memphis-pop':
  cols=[(255,105,94),(72,160,220),(255,215,70),(245,245,220)]
  for _ in range(40):x=random.randrange(W);y=random.randrange(H);s=random.randrange(12,45);c=random.choice(cols);d.rectangle((x,y,x+s,y+s),fill=(*c,80))
 elif slug=='blueprint-architect':
  for x in range(0,W,60):d.line((x,0,x,H),fill=(110,200,255,30));
  for y in range(0,H,60):d.line((0,y,W,y),fill=(110,200,255,30));d.line((80,760,1320,180),fill=(*a,100),width=3)
 elif slug=='japanese-minimal':
  d.ellipse((930,120,1320,510),fill=(*a,210));d.line((110,650,750,650),fill=(20,20,20,100),width=3);d.line((110,690,560,690),fill=(20,20,20,70),width=2)
 elif slug=='bauhaus-26':
  d.ellipse((100,90,430,420),fill=(230,65,50,180));d.rectangle((960,100,1320,430),fill=(50,95,190,170));d.polygon([(520,760),(760,280),(940,760)],fill=(245,205,50,170))
 elif slug=='clay-soft':
  for x,y,r,c in [(250,240,240,(225,130,95)),(1050,620,330,(245,180,145)),(920,100,170,(190,100,80))]:d.ellipse((x-r,y-r,x+r,y+r),fill=(*c,45));l=l.filter(ImageFilter.GaussianBlur(25))
 elif slug=='carbon-motorsport':
  for x in range(-H,W,32):d.line((x,0,x+H,H),fill=(255,255,255,16),width=10);d.line((x+16,0,x+H+16,H),fill=(0,0,0,100),width=10)
  d.line((0,700,W,420),fill=(*a,120),width=8)
 elif slug=='nordic-snow':
  d.polygon([(0,700),(350,300),(600,650),(900,180),(1440,720),(1440,900),(0,900)],fill=(120,165,190,40));d.line((0,700,350,300,600,650,900,180,1440,720),fill=(*a,80),width=3)
 elif slug=='comic-pop':
  for x in range(40,W,35):
   for y in range(40,H,35):d.ellipse((x,y,x+5,y+5),fill=(*a,40))
  d.polygon([(1040,100),(1110,270),(1320,210),(1170,360),(1370,470),(1130,430),(1080,650),(1010,450),(800,520),(950,340),(800,210),(1010,270)],fill=(*a,70))
 elif slug=='desert-dune':
  for j,c in enumerate([(210,135,80),(170,95,55),(235,180,115)]):d.line([(x,420+j*120+70*math.sin(x*.002+j)) for x in range(-100,W+100,18)],fill=(*c,70),width=180)
 elif slug=='analog-synth':
  for x in range(100,W,180):d.ellipse((x-30,130,x+30,190),outline=(*a,150),width=6);d.line((x,160,x+22,125),fill=(240,240,220,160),width=4)
  for y in (300,520,740):d.line((80,y,W-80,y),fill=(255,255,255,30),width=2)
 elif slug=='stained-glass':
  pts=[(0,0),(360,0),(220,330),(0,500),(0,0),(360,0),(700,260),(220,330),(700,260),(1100,0),(1440,0),(1440,450),(1050,620),(700,260),(1050,620),(650,900),(0,900),(220,330)]
  d.line(pts,fill=(20,20,25,230),width=14,joint='curve')
  for x,y,c in [(200,160,(180,40,65)),(620,180,(45,90,190)),(1130,220,(230,170,45)),(880,650,(65,160,110))]:d.ellipse((x-190,y-190,x+190,y+190),fill=(*c,65))
 elif slug=='newspaper-noir':
  for y in range(100,800,85):d.line((80,y,1360,y),fill=(25,25,25,45),width=2)
  for x in (480,960):d.line((x,80,x,820),fill=(25,25,25,35),width=2)
 elif slug=='pixel-garden':
  for x in range(0,W,32):
   h=random.randrange(20,170,20);d.rectangle((x,H-h,x+28,H),fill=(70,145+random.randrange(50),75,100));
  for _ in range(28):x=random.randrange(0,W,32);y=random.randrange(420,800,32);d.rectangle((x,y,x+16,y+16),fill=(*a,110))
 elif slug=='origami':
  for p,c in [([(0,0),(600,0),(360,480)],(255,255,255,90)), ([(600,0),(1440,0),(980,430)],(180,205,220,80)), ([(360,480),(980,430),(700,900)],(*a,55))]:d.polygon(p,fill=c)
 else:
  for k in range(-900,1600,120):d.line((k,H,k+900,0),fill=(*a,18),width=2)
 Image.alpha_composite(im,l).convert('RGB').save(path,'WEBP',quality=95)
def theme_text(name,slug,accent):
 a=rgb(accent);light=slug in {'paper-ink','porcelain-blue','nordic-snow','newspaper-noir','japanese-minimal','origami'};bg='#F4F1E8' if light else '#000000';fg='#171717' if light else '#FFFFFF'; pc='#%02X%02X%02X'%mix((0,0,0),a,.34);kc='#EEEAE0' if light else '#%02X%02X%02X'%mix((3,3,5),a,.06);pressed='#%02X%02X%02X'%mix((0,0,0),a,.50)
 return f'''# FUTO Keyboard Theme Configuration\nname = "{name}"\nauthor = "Latan Villegas"\nid = "com.latanvillegas.{slug.replace('-','')}"\nversion = 5\ndescription = "Original custom FUTO Keyboard theme by Latan Villegas."\n\n[options]\nauto_borders = true\ncenter_hints = false\nroundedness = 1\nscale_text = 1\nscale_hints = 1\nweight_text = 400\nweight_hints = 500\n\n[colors]\nprimary = "{accent}"\non_primary = "#FFFFFF"\nprimary_container = "{pc}"\non_primary_container = "#FFFFFF"\ninverse_primary = "{accent}"\nsecondary = "{accent}"\non_secondary = "#FFFFFF"\nsecondary_container = "{pc}"\non_secondary_container = "#FFFFFF"\ntertiary = "{accent}"\non_tertiary = "#FFFFFF"\ntertiary_container = "{pc}"\non_tertiary_container = "#FFFFFF"\nbackground = "{bg}"\non_background = "{fg}"\nsurface = "{bg}"\non_surface = "{fg}"\nsurface_variant = "{kc}"\non_surface_variant = "{fg}"\nsurface_tint = "{accent}"\ninverse_surface = "{fg}"\ninverse_on_surface = "{bg}"\nerror = "#FF5252"\non_error = "#000000"\nerror_container = "#5C1010"\non_error_container = "#FFDAD6"\noutline = "{accent}"\noutline_variant = "{pc}"\nscrim = "#000000"\nsurface_bright = "{kc}"\nsurface_dim = "{bg}"\nsurface_container = "{kc}"\nsurface_container_high = "{kc}"\nsurface_container_highest = "{kc}"\nsurface_container_low = "{bg}"\nsurface_container_lowest = "{bg}"\nkeyboard_surface = "{bg}"\nkeyboard_surface_dim = "{bg}"\nkeyboard_container = "{kc}"\nkeyboard_container_variant = "{kc}"\non_keyboard_container = "{fg}"\nkeyboard_press = "{accent}"\nkeyboard_container_pressed = "{pressed}"\non_keyboard_container_pressed = "#FFFFFF"\n\n[options.background]\nimage = "background.webp"\nopacity = 1\naction_bar_opacity = 0.82\ncropping = [0,0,1,1]\n\n[[matchrules.border]]\nselector = "pressed"\nasset = "pressed.png"\n[[matchrules.border]]\nselector = "normal"\nasset = "normal.png"\n[[matchrules.border]]\nselector = "spacebar"\nasset = "normal.png"\n[[matchrules.border]]\nselector = "action"\nasset = "action.png"\n[[matchrules.border]]\nselector = "functional"\nasset = "functional.png"\n\n[[asset.border]]\nname = "normal.png"\nbackground_tint = "#FFFFFF"\nforeground_tint = "#FFFFFF"\npadding = [0,0,0,0]\nslicing = [0.28,0.28,0.72,0.72]\ngap = [1,1,1,1]\ntarget_density = 320\n[[asset.border]]\nname = "functional.png"\nbackground_tint = "#FFFFFF"\nforeground_tint = "#FFFFFF"\npadding = [0,0,0,0]\nslicing = [0.28,0.28,0.72,0.72]\ngap = [1,1,1,1]\ntarget_density = 320\n[[asset.border]]\nname = "pressed.png"\nbackground_tint = "#FFFFFF"\nforeground_tint = "#FFFFFF"\npadding = [0,0,0,0]\nslicing = [0.28,0.28,0.72,0.72]\ngap = [1,1,1,1]\ntarget_density = 320\n[[asset.border]]\nname = "action.png"\nbackground_tint = "#FFFFFF"\nforeground_tint = "#FFFFFF"\npadding = [0,0,0,0]\nslicing = [0.28,0.28,0.72,0.72]\ngap = [1,1,1,1]\ntarget_density = 320\n'''
def build(slug,name,accent):
 out=BUILD/slug
 if out.exists():shutil.rmtree(out)
 out.mkdir(parents=True);background(out/'background.webp',slug,accent)
 for fn,v in [('normal.png','normal'),('functional.png','functional'),('pressed.png','pressed'),('action.png','pressed')]:key_asset(out/fn,accent,v,slug)
 (out/'theme.txt').write_text(theme_text(name,slug,accent),encoding='utf-8');(out/'LICENSE.txt').write_text('Copyright (c) 2026 Latan Villegas. Personal non-commercial use permitted. Third-party components retain their original licenses.\n',encoding='utf-8');(out/'CREDITS.txt').write_text(f'{name} theme design and original visual assets: Latan Villegas.\nTypography: FUTO/system font in this build. Any future third-party font will retain its original license and attribution.\n',encoding='utf-8')
 z=DIST/f'{slug}-FUTO.zip'
 with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as q:
  for p in out.rglob('*'):
   if p.is_file():q.write(p,p.relative_to(out).as_posix())
 print(z)
for item in THEMES:build(*item)
