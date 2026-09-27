from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
import zipfile,math,urllib.request
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'build'/'neon-orchid-studio-26';DIST=ROOT/'dist';OUT.mkdir(parents=True,exist_ok=True);DIST.mkdir(exist_ok=True)
for p in OUT.iterdir():
 if p.is_file():p.unlink()
def dl(url,path):
 req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'});path.write_bytes(urllib.request.urlopen(req,timeout=60).read())
dl('https://raw.githubusercontent.com/google/fonts/main/ofl/notosans/NotoSans%5Bwdth,wght%5D.ttf',OUT/'NotoSans.ttf');dl('https://raw.githubusercontent.com/google/fonts/main/ofl/notosans/OFL.txt',OUT/'OFL-NotoSans.txt')
W,H=1440,900;base=Image.new('RGBA',(W,H),(5,7,17,255));mesh=Image.new('RGBA',(W,H),(0,0,0,0));d=ImageDraw.Draw(mesh)
for box,col in [((-260,-230,640,660),(48,224,255,62)),((770,-260,1600,560),(164,75,255,72)),((820,420,1570,1160),(255,66,164,55)),((-250,520,600,1160),(60,255,196,35))]:d.ellipse(box,fill=col)
for j in range(5):d.line([(x,165+j*125+55*math.sin(x/175+j*.9)) for x in range(-100,W+100,18)],fill=(190,225,255,18+j*5),width=10-j)
mesh=mesh.filter(ImageFilter.GaussianBlur(48));bg=Image.alpha_composite(base,mesh);detail=Image.new('RGBA',(W,H),(0,0,0,0));dd=ImageDraw.Draw(detail);dd.arc((950,60,1380,490),195,515,fill=(154,239,255,105),width=4);dd.arc((1000,110,1330,440),195,515,fill=(255,145,220,90),width=2)
for r in [90,150,220]:dd.arc((180-r,690-r,180+r,690+r),280,70,fill=(116,255,214,55),width=3)
Image.alpha_composite(bg,detail).convert('RGB').save(OUT/'neon-orchid-background.webp','WEBP',quality=96,method=6)
def border(name,fill,edge,inner,pressed=False,action=False):
 w,h,s=128,140,4;im=Image.new('RGBA',(w*s,h*s),(0,0,0,0));dr=ImageDraw.Draw(im)
 if pressed:dr.rounded_rectangle((3*s,5*s,(w-3)*s,(h-2)*s),31*s,fill=(91,245,255,45))
 dr.rounded_rectangle((7*s,8*s,(w-7)*s,(h-7)*s),27*s,fill=fill,outline=edge,width=2*s);dr.rounded_rectangle((11*s,12*s,(w-11)*s,(h-11)*s),23*s,outline=inner,width=s);dr.arc((16*s,14*s,(w-16)*s,72*s),195,340,fill=(255,255,255,115),width=2*s)
 if action:dr.rounded_rectangle((25*s,(h-29)*s,(w-25)*s,(h-21)*s),4*s,fill=(218,255,250,190))
 im.resize((w,h),Image.Resampling.LANCZOS).save(OUT/name)
border('border-normal.png',(13,18,38,235),(91,191,226,220),(255,255,255,30));border('border-functional.png',(26,22,52,245),(163,109,255,235),(255,255,255,38));border('border-action.png',(83,40,128,250),(242,130,255,255),(255,228,255,55),action=True);border('border-pressed.png',(25,111,137,252),(111,255,236,255),(255,255,255,70),pressed=True);border('border-popup.png',(62,31,89,252),(255,119,207,255),(255,240,250,60))
def canvas():return Image.new('RGBA',(96,96),(0,0,0,0))
im=canvas();dr=ImageDraw.Draw(im);dr.polygon([(48,15),(20,45),(34,45),(34,73),(62,73),(62,45),(76,45)],fill='white');im.save(OUT/'icon-shift.png')
im=canvas();dr=ImageDraw.Draw(im);dr.polygon([(48,12),(18,43),(33,43),(33,69),(63,69),(63,43),(78,43)],fill='white');dr.rectangle((31,77,65,83),fill='white');im.save(OUT/'icon-shift-shifted.png')
im=canvas();dr=ImageDraw.Draw(im);dr.line((74,22,74,55,34,55),fill='white',width=10,joint='curve');dr.polygon([(36,37),(15,55),(36,73)],fill='white');im.save(OUT/'icon-enter.png')
im=canvas();dr=ImageDraw.Draw(im);dr.ellipse((14,14,82,82),outline='white',width=8);dr.ellipse((31,34,38,41),fill='white');dr.ellipse((58,34,65,41),fill='white');dr.arc((31,42,66,67),10,170,fill='white',width=6);im.save(OUT/'icon-emoji.png')
im=canvas();dr=ImageDraw.Draw(im);dr.polygon([(16,48),(36,26),(80,26),(80,70),(36,70)],outline='white');dr.line((43,38,63,58),fill='white',width=6);dr.line((63,38,43,58),fill='white',width=6);im.save(OUT/'icon-backspace.png')
badge=Image.new('RGBA',(256,256),(0,0,0,0));bd=ImageDraw.Draw(badge);bd.ellipse((30,30,226,226),outline=(145,240,255,220),width=8);bd.ellipse((58,58,198,198),outline=(255,125,218,180),width=4);bd.polygon([(128,65),(146,110),(195,128),(146,146),(128,195),(110,146),(61,128),(110,110)],fill=(255,255,255,210));badge.save(OUT/'orchid-badge.png')
c={'primary':'#9CEFFF','on_primary':'#00363D','primary_container':'#004F58','on_primary_container':'#B8F5FF','inverse_primary':'#006874','secondary':'#D0B6FF','on_secondary':'#35145F','secondary_container':'#4C2D77','on_secondary_container':'#EBDDFF','tertiary':'#FFACDB','on_tertiary':'#5D003C','tertiary_container':'#7E1E59','on_tertiary_container':'#FFD8EB','error':'#FFB4AB','on_error':'#690005','error_container':'#93000A','on_error_container':'#FFDAD6','background':'#050711','on_background':'#F4F5FF','surface':'#090B17','on_surface':'#F4F5FF','surface_variant':'#292B3D','on_surface_variant':'#CAC7D8','outline':'#93909F','outline_variant':'#484654','scrim':'#000000','inverse_surface':'#E5E1ED','inverse_on_surface':'#30303A','surface_tint':'#9CEFFF','surface_dim':'#050711','surface_bright':'#353541','surface_container_lowest':'#03040B','surface_container_low':'#0D0F1B','surface_container':'#111320','surface_container_high':'#1B1D2A','surface_container_highest':'#262835','keyboard_surface':'#050711','keyboard_surface_dim':'#03040B','keyboard_container':'#101427','keyboard_container_variant':'#242341','on_keyboard_container':'#FFFFFF','keyboard_press':'#9CEFFF','keyboard_container_pressed':'#176F82','on_keyboard_container_pressed':'#FFFFFF'}
lines=['# Format version: 1.0','','name = "Neon Orchid Studio 26"','author = "Latan Villegas"','id = "com.latanvillegas.neonorchidstudio26"','version = 1','description = "Designer-grade neon orchid theme with background, font, border assets, icon assets and matchrules."','','[options]','auto_borders = true','center_hints = false','roundedness = 0.95','scale_text = 1.04','scale_hints = 0.91','weight_text = 620','weight_hints = 520','','[colors]']+[f'{k} = "{v}"' for k,v in c.items()]+['','[options.font]','font = "NotoSans.ttf"','','[options.background]','image = "neon-orchid-background.webp"','opacity = 0.98','action_bar_opacity = 0.78','cropping = [0, 0, 1, 1]']
for sel,a in [('pressed','border-pressed.png'),('popup','border-popup.png'),('action','border-action.png'),('functional','border-functional.png'),('spacebar','border-normal.png'),('normal','border-normal.png')]:lines+=['','[[matchrules.border]]',f'selector = "{sel}"',f'asset = "{a}"']
for sel,a in [('icon shift_key_shifted','icon-shift-shifted.png'),('icon shift_key','icon-shift.png'),('icon enter_key','icon-enter.png'),('icon action_emoji','icon-emoji.png'),('icon backspace','icon-backspace.png')]:lines+=['','[[matchrules.icon]]',f'selector = "{sel}"',f'asset = "{a}"']
for a in ['border-normal.png','border-functional.png','border-action.png','border-pressed.png','border-popup.png']:lines+=['','[[asset.border]]',f'name = "{a}"','background_tint = "#FFFFFFFF"','foreground_tint = "#FFFFFFFF"','padding = [0.055, 0.05, 0.945, 0.95]','slicing = [0.30, 0.28, 0.70, 0.72]','gap = [0.025, 0.02, 0.975, 0.98]','target_density = 320']
for a in ['icon-shift.png','icon-shift-shifted.png','icon-enter.png','icon-emoji.png','icon-backspace.png']:lines+=['','[[asset.icon]]',f'name = "{a}"','foreground_tint = "#FFFFFFFF"','target_density = 320']
(OUT/'theme.txt').write_text('\n'.join(lines)+'\n');(OUT/'CREDITS.txt').write_text('Neon Orchid Studio 26\nOriginal concept, background, border assets, icon artwork and decorative assets: Latan Villegas\nNoto Sans: The Noto Project Authors, Google Fonts, SIL OFL 1.1.\n');(OUT/'LICENSE.txt').write_text('Original visual assets Copyright (c) 2026 Latan Villegas. Noto Sans remains under the included SIL Open Font License.\n');z=DIST/'neon-orchid-studio-26-FUTO.zip';z.unlink(missing_ok=True)
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as f:
 for p in OUT.iterdir():
  if p.is_file():f.write(p,p.name)
print('Built',z)
