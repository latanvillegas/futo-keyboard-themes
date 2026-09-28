from pathlib import Path
import base64, io, zipfile, re, shutil
from PIL import Image, ImageEnhance

ROOT=Path(__file__).resolve().parents[1]
DIST=ROOT/'dist'; DIST.mkdir(exist_ok=True)
BASE=Path('/tmp/aurora-candy-26-premium-FUTO.zip.b64')
OUT=DIST/'aurora-night-26-amoled-FUTO.zip'

raw=base64.b64decode(BASE.read_text().strip())
work=ROOT/'build'/'aurora-night-26-amoled'
if work.exists(): shutil.rmtree(work)
work.mkdir(parents=True)
with zipfile.ZipFile(io.BytesIO(raw)) as z: z.extractall(work)

theme=next(work.rglob('theme.txt'))
t=theme.read_text(encoding='utf-8')

# Approved AMOLED V15: true black keyboard, transparent normal key/space
# containers, readable white keyboard text and readable FUTO dialogs/settings.
vals={
'background':'#000000FF','surface':'#000000FF','surface_dim':'#000000FF',
'surface_container_lowest':'#000000FF','surface_container_low':'#000000FF','surface_container':'#000000FF',
'keyboard_surface':'#000000FF','keyboard_surface_dim':'#000000FF',
'keyboard_container':'#00000000','keyboard_container_variant':'#00000000',
'on_keyboard_container':'#FFFFFFFF','keyboard_press':'#17131F66',
'keyboard_container_pressed':'#17131F66','on_keyboard_container_pressed':'#FFFFFFFF',
'primary':'#B8A8F2FF','on_primary':'#171124FF','primary_container':'#29213DFF','on_primary_container':'#F1EBFFFF',
'inverse_primary':'#675A9AFF','secondary':'#AAB3E8FF','on_secondary':'#151A2AFF',
'secondary_container':'#252A3DFF','on_secondary_container':'#EDF0FFFF',
'tertiary':'#C6A4D0FF','on_tertiary':'#241528FF','tertiary_container':'#35233AFF','on_tertiary_container':'#F8EFFFFF',
'on_background':'#F2EFF7FF','on_surface':'#F2EFF7FF','on_surface_variant':'#D1CBD9FF',
'outline':'#77717FFF','outline_variant':'#3B3642FF','surface_tint':'#000000FF'
}
for k,v in vals.items():
    t=re.sub(rf'(?mi)^({re.escape(k)}\s*=\s*)"#[0-9A-Fa-f]{{6,8}}"',rf'\1"{v}"',t)

# Remove inherited border match rules; they caused low-contrast key legends.
t=re.sub(r'\n\[\[matchrules\.border\]\]\n.*?(?=\n\[\[|\Z)','',t,flags=re.S)
t=re.sub(r'(?mi)^(auto_borders\s*=\s*)(true|false)',r'\1false',t)
# No inherited background tint on key assets.
t=re.sub(r'(?mi)^background_tint\s*=\s*"#[0-9A-Fa-f]{6,8}"','background_tint = "#00000000"',t)

t=re.sub(r'(?m)^name\s*=\s*".*?"','name = "Aurora Night 26 AMOLED"',t,count=1)
t=re.sub(r'(?m)^id\s*=\s*".*?"','id = "com.latanvillegas.auroranight26.amoled"',t,count=1)
t=re.sub(r'(?m)^version\s*=\s*\d+','version = 1',t,count=1)
theme.write_text(t,encoding='utf-8')

# AMOLED background: practically pure black while retaining only a trace of texture.
m=re.search(r'(?mi)^\s*image\s*=\s*"([^"]+)"',t)
if m:
    p=work/m.group(1)
    if p.exists():
        im=Image.open(p).convert('RGB')
        im=ImageEnhance.Brightness(im).enhance(0.04)
        black=Image.new('RGB',im.size,(0,0,0))
        im=Image.blend(black,im,0.10)
        im.save(p,'WEBP',quality=96,method=6) if p.suffix.lower()=='.webp' else im.save(p)

with zipfile.ZipFile(OUT,'w',zipfile.ZIP_DEFLATED) as z:
    for p in work.rglob('*'):
        if p.is_file(): z.write(p,p.relative_to(work).as_posix())
print(OUT)
