from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
import zipfile,random
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'build'/'solar-flare-26';DIST=ROOT/'dist';OUT.mkdir(parents=True,exist_ok=True);DIST.mkdir(exist_ok=True)
W,H=1440,900;base=Image.new('RGBA',(W,H),(10,7,12,255));glow=Image.new('RGBA',(W,H),(0,0,0,0));d=ImageDraw.Draw(glow);d.ellipse((390,130,1050,790),fill=(255,111,35,42));d.ellipse((500,240,940,680),fill=(255,202,86,60))
for col,wid,off in [((255,199,83,95),12,0),((255,105,35,75),8,55),((255,61,82,55),6,110)]:d.arc((180+off,80+off//2,1260-off,930-off//2),198,342,fill=col,width=wid)
for y in range(560,850,55):d.line((120,y,1320,y),fill=(255,130,60,max(8,42-(y-560)//10)),width=2)
glow=glow.filter(ImageFilter.GaussianBlur(35));img=Image.alpha_composite(base,glow);stars=Image.new('RGBA',(W,H),(0,0,0,0));sd=ImageDraw.Draw(stars);random.seed(2602)
for _ in range(150):
 x=random.randrange(W);y=random.randrange(H);r=random.choice([1,1,1,2]);sd.ellipse((x-r,y-r,x+r,y+r),fill=(255,220,170,random.randrange(25,80)))
Image.alpha_composite(img,stars).convert('RGB').save(OUT/'solar-flare-background.webp','WEBP',quality=95,method=6)
def key(name,fill,edge,g,pressed=False,action=False):
 w,h,s=128,140,4;im=Image.new('RGBA',(w*s,h*s),(0,0,0,0));dr=ImageDraw.Draw(im)
 if pressed:dr.rounded_rectangle((4*s,6*s,(w-4)*s,(h-3)*s),21*s,fill=(*g,48))
 dr.rounded_rectangle((7*s,7*s,(w-7)*s,(h-7)*s),19*s,fill=fill,outline=edge,width=2*s);dr.rounded_rectangle((11*s,11*s,(w-11)*s,(h-11)*s),15*s,outline=(*g,85),width=s);dr.line((22*s,17*s,(w-22)*s,17*s),fill=(255,230,185,110),width=2*s)
 if action:dr.arc((24*s,(h-42)*s,(w-24)*s,(h-12)*s),190,350,fill=(255,235,170,210),width=3*s)
 im.resize((w,h),Image.Resampling.LANCZOS).save(OUT/name)
key('flare-normal.png',(29,19,24,242),(134,71,51,255),(255,121,55));key('flare-functional.png',(43,23,29,246),(190,76,48,255),(255,112,47));key('flare-action.png',(134,47,24,250),(255,186,76,255),(255,203,96),action=True);key('flare-pressed.png',(164,55,25,252),(255,220,112,255),(255,205,90),pressed=True);key('flare-popup.png',(70,27,37,252),(255,112,86,255),(255,132,74))
c={'primary':'#FFB65C','on_primary':'#321300','primary_container':'#713000','on_primary_container':'#FFDCC0','inverse_primary':'#914100','secondary':'#FF8A67','on_secondary':'#3A0A00','secondary_container':'#7C2D1A','on_secondary_container':'#FFDAD0','tertiary':'#FFD36A','on_tertiary':'#241A00','tertiary_container':'#584400','on_tertiary_container':'#FFEFAF','error':'#FFB4AB','on_error':'#690005','error_container':'#93000A','on_error_container':'#FFDAD6','background':'#0A070C','on_background':'#FFF1E7','surface':'#100A0F','on_surface':'#FFF1E7','surface_variant':'#3B292B','on_surface_variant':'#E8C8C3','outline':'#C99B8D','outline_variant':'#59413E','scrim':'#000000','inverse_surface':'#FFF1E7','inverse_on_surface':'#2A1C1C','surface_tint':'#FFB65C','surface_dim':'#070408','surface_bright':'#432E31','surface_container_lowest':'#050205','surface_container_low':'#130B0E','surface_container':'#1C1115','surface_container_high':'#28191D','surface_container_highest':'#352126','keyboard_surface':'#0A070C','keyboard_surface_dim':'#070408','keyboard_container':'#1B1015','keyboard_container_variant':'#352026','on_keyboard_container':'#FFF3E9','keyboard_press':'#FFC76D','keyboard_container_pressed':'#A33C1C','on_keyboard_container_pressed':'#FFFFFF'}
lines=['name = "Solar Flare 26"','author = "Latan Villegas"','id = "com.latanvillegas.solarflare26"','version = 1','description = "Premium solar-energy theme with warm metallic keys and luminous interaction states."','','[options]','auto_borders = true','center_hints = false','roundedness = 0.72','scale_text = 1.02','scale_hints = 0.90','weight_text = 520','weight_hints = 490','','[colors]']+[f'{k} = "{v}"' for k,v in c.items()]+['','[options.background]','image = "solar-flare-background.webp"','opacity = 0.97','action_bar_opacity = 0.78','cropping = [0, 0, 1, 1]']
for sel,a in [('pressed','flare-pressed.png'),('popup','flare-popup.png'),('action','flare-action.png'),('functional','flare-functional.png'),('spacebar','flare-normal.png'),('normal','flare-normal.png')]:lines+=['','[[matchrules.border]]',f'selector = "{sel}"',f'asset = "{a}"']
for a in ['flare-normal.png','flare-functional.png','flare-action.png','flare-pressed.png','flare-popup.png']:lines+=['','[[asset.border]]',f'name = "{a}"','background_tint = "#FFFFFFFF"','foreground_tint = "#FFFFFFFF"','padding = [0.055, 0.05, 0.945, 0.95]','slicing = [0.28, 0.27, 0.72, 0.73]','gap = [0.025, 0.02, 0.975, 0.98]','target_density = 320']
(OUT/'theme.txt').write_text('\n'.join(lines)+'\n');(OUT/'CREDITS.txt').write_text('Solar Flare 26\nOriginal concept, solar background and key assets: Latan Villegas\n');(OUT/'LICENSE.txt').write_text('Copyright (c) 2026 Latan Villegas. Permission is granted to use, copy, modify and redistribute with attribution.\n');z=DIST/'solar-flare-26-FUTO.zip';z.unlink(missing_ok=True)
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as f:
 for p in OUT.iterdir():
  if p.is_file():f.write(p,p.name)
print('Built',z)
