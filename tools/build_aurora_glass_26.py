from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import zipfile, shutil, urllib.request, time

ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'build'/'aurora-glass-26'; DIST=ROOT/'dist'; DIST.mkdir(exist_ok=True)
shutil.rmtree(OUT,ignore_errors=True); OUT.mkdir(parents=True)

def download(url,dest):
    for n in range(5):
        try:
            req=urllib.request.Request(url,headers={'User-Agent':'futo-keyboard-themes/1.0'})
            with urllib.request.urlopen(req,timeout=45) as r, open(dest,'wb') as f: shutil.copyfileobj(r,f)
            return
        except Exception:
            if n==4: raise
            time.sleep(2**(n+1))

# Premium aurora background, 1440x900, deliberately abstract/original.
W,H=1440,900
base=Image.new('RGBA',(W,H),(3,7,18,255)); glow=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(glow)
for pts,col,width in [
    ([(x,280+100*((x//90)%3)) for x in range(-100,W+200,90)],(55,255,210,80),190),
    ([(x,410+85*((x//120+1)%4)) for x in range(-100,W+200,100)],(80,150,255,78),210),
    ([(x,520+65*((x//140+2)%3)) for x in range(-100,W+200,100)],(185,85,255,58),180)]:
    d.line(pts,fill=col,width=width,joint='curve')
for x,y,r,c in [(210,180,180,(80,255,220,38)),(1120,210,240,(95,130,255,38)),(850,690,260,(180,80,255,30))]: d.ellipse((x-r,y-r,x+r,y+r),fill=c)
glow=glow.filter(ImageFilter.GaussianBlur(80)); Image.alpha_composite(base,glow).convert('RGB').save(OUT/'aurora-background.webp','WEBP',quality=95,method=6)

# 128x140 glass borders. Each state is visibly distinct and 9-slice friendly.
def glass(name,fill,edge,shine=True,pressed=False):
    w,h,s=128,140,4; im=Image.new('RGBA',(w*s,h*s),(0,0,0,0)); dr=ImageDraw.Draw(im); box=(7*s,7*s,(w-7)*s,(h-7)*s)
    if pressed: dr.rounded_rectangle((9*s,11*s,(w-5)*s,(h-3)*s),24*s,fill=(30,255,220,38))
    dr.rounded_rectangle(box,24*s,fill=fill,outline=edge,width=2*s)
    dr.rounded_rectangle((11*s,11*s,(w-11)*s,(h-11)*s),20*s,outline=(255,255,255,34),width=s)
    if shine: dr.line((24*s,18*s,(w-24)*s,18*s),fill=(255,255,255,118),width=2*s)
    im.resize((w,h),Image.Resampling.LANCZOS).save(OUT/name)

glass('glass-normal.png',(12,24,44,196),(105,225,255,205))
glass('glass-functional.png',(18,29,55,220),(151,116,255,225))
glass('glass-action.png',(25,115,130,225),(102,255,222,255))
glass('glass-pressed.png',(25,104,126,238),(145,255,236,255),pressed=True)
glass('glass-popup.png',(31,38,72,242),(185,147,255,255))

# Modern rounded font + its upstream OFL license.
download('https://raw.githubusercontent.com/google/fonts/main/ofl/manrope/Manrope%5Bwght%5D.ttf',OUT/'Manrope.ttf')
download('https://raw.githubusercontent.com/google/fonts/main/ofl/manrope/OFL.txt',OUT/'OFL-Manrope.txt')

colors={
'primary':'#63F4D1','on_primary':'#04120F','primary_container':'#124A50','on_primary_container':'#D7FFF7','inverse_primary':'#006B5C',
'secondary':'#8FCBFF','on_secondary':'#061522','secondary_container':'#173A5A','on_secondary_container':'#E0F1FF',
'tertiary':'#C69BFF','on_tertiary':'#1D0B33','tertiary_container':'#472A68','on_tertiary_container':'#F1E3FF',
'error':'#FFB4AB','on_error':'#690005','error_container':'#93000A','on_error_container':'#FFDAD6',
'background':'#030712','on_background':'#E7F5FF','surface':'#050A16','on_surface':'#E7F5FF','surface_variant':'#15243A','on_surface_variant':'#C9D8E8',
'outline':'#73DDEA','outline_variant':'#334E68','scrim':'#000000','inverse_surface':'#E7F5FF','inverse_on_surface':'#12202D','surface_tint':'#63F4D1',
'surface_dim':'#02050D','surface_bright':'#26364B','surface_container_lowest':'#01030A','surface_container_low':'#08101F','surface_container':'#0C1728','surface_container_high':'#122137','surface_container_highest':'#192B44',
'keyboard_surface':'#030712','keyboard_surface_dim':'#02050D','keyboard_container':'#0C182B','keyboard_container_variant':'#162942','on_keyboard_container':'#F1FAFF','keyboard_press':'#63F4D1','keyboard_container_pressed':'#176C78','on_keyboard_container_pressed':'#FFFFFF'}

lines=['# Aurora Glass 26 — advanced FUTO Keyboard theme','name = "Aurora Glass 26"','author = "Latan Villegas"','id = "com.latanvillegas.auroraglass26"','version = 1','description = "Premium aurora glass theme with custom typography, original background, glass 9-slice assets and interaction states."','','[options]','auto_borders = true','center_hints = false','roundedness = 1.0','scale_text = 1.01','scale_hints = 0.90','weight_text = 520','weight_hints = 480','','[colors]']
lines += [f'{k} = "{v}"' for k,v in colors.items()]
lines += ['','[options.font]','font = "Manrope.ttf"','','[options.background]','image = "aurora-background.webp"','opacity = 0.96','action_bar_opacity = 0.76','cropping = [0, 0, 1, 1]']
# Specific interaction rules first, broad rules last.
for selector,asset in [('pressed','glass-pressed.png'),('popup','glass-popup.png'),('action','glass-action.png'),('functional','glass-functional.png'),('spacebar','glass-normal.png'),('normal','glass-normal.png')]:
    lines += ['','[[matchrules.border]]',f'selector = "{selector}"',f'asset = "{asset}"']
for asset in ['glass-normal.png','glass-functional.png','glass-action.png','glass-pressed.png','glass-popup.png']:
    lines += ['','[[asset.border]]',f'name = "{asset}"','background_tint = "#FFFFFFFF"','foreground_tint = "#FFFFFFFF"','padding = [0.055, 0.05, 0.945, 0.95]','slicing = [0.30, 0.28, 0.70, 0.72]','gap = [0.025, 0.02, 0.975, 0.98]','target_density = 320']
(OUT/'theme.txt').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(OUT/'CREDITS.txt').write_text('Aurora Glass 26\nOriginal theme concept, background and glass key assets: Latan Villegas\nTypography: Manrope from Google Fonts. Its OFL license is included as OFL-Manrope.txt.\n',encoding='utf-8')
(OUT/'LICENSE.txt').write_text('Copyright (c) 2026 Latan Villegas. Original Aurora Glass 26 visual assets may be used, modified and redistributed with attribution. Manrope remains under its included SIL Open Font License.\n',encoding='utf-8')

# Fail build if the complete FUTO color schema regresses.
required=['inverse_primary','surface_dim','surface_bright','surface_container','surface_container_high','surface_container_highest','surface_container_low','surface_container_lowest','inverse_surface','inverse_on_surface','surface_tint']
missing=[x for x in required if x not in colors]
if missing: raise SystemExit('Missing required FUTO colors: '+', '.join(missing))

z=DIST/'aurora-glass-26-FUTO.zip'; z.unlink(missing_ok=True)
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as f:
    for p in OUT.iterdir():
        if p.is_file(): f.write(p,p.name)
print('Built',z)
