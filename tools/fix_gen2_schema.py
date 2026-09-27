from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / 'build'
DIST = ROOT / 'dist'
SLUGS = ['luxury-ivory','neo-tokyo-2026','botanical-atelier','liquid-titanium','candy-y2k']

# FUTO SerializedTomlFile.Colors requires the complete color model, even when
# values could otherwise be derived automatically by the editor.
REQUIRED_DEFAULTS = {
    'inverse_primary': '#D0B08A',
    'surface_tint': '#A47745',
    'inverse_surface': '#F5F5F5',
    'inverse_on_surface': '#202020',
    'error': '#FFB4AB',
    'on_error': '#690005',
    'error_container': '#93000A',
    'on_error_container': '#FFDAD6',
    'surface_bright': '#343438',
    'surface_dim': '#101014',
    'surface_container': '#1B1B20',
    'surface_container_high': '#25252B',
    'surface_container_highest': '#303038',
    'surface_container_low': '#151519',
    'surface_container_lowest': '#08080B',
}

for slug in SLUGS:
    out = BUILD / slug
    theme = out / 'theme.txt'
    text = theme.read_text(encoding='utf-8')
    marker = '\n[options.font]'
    if marker not in text:
        raise SystemExit(f'Missing options.font marker in {theme}')
    additions = []
    for key, value in REQUIRED_DEFAULTS.items():
        if f'{key} =' not in text:
            additions.append(f'{key} = "{value}"')
    if additions:
        text = text.replace(marker, '\n' + '\n'.join(additions) + marker, 1)
        theme.write_text(text, encoding='utf-8')

    # Guard against the exact class of import failure seen on-device.
    required = [
        'primary','on_primary','primary_container','on_primary_container','inverse_primary',
        'secondary','on_secondary','secondary_container','on_secondary_container',
        'tertiary','on_tertiary','tertiary_container','on_tertiary_container',
        'background','on_background','surface','on_surface','surface_variant','on_surface_variant',
        'surface_tint','inverse_surface','inverse_on_surface','error','on_error','error_container',
        'on_error_container','outline','outline_variant','scrim','surface_bright','surface_dim',
        'surface_container','surface_container_high','surface_container_highest','surface_container_low',
        'surface_container_lowest','keyboard_surface','keyboard_surface_dim','keyboard_container',
        'keyboard_container_variant','on_keyboard_container','keyboard_press',
        'keyboard_container_pressed','on_keyboard_container_pressed'
    ]
    missing = [k for k in required if f'{k} =' not in text]
    if missing:
        raise SystemExit(f'{slug}: missing required FUTO colors: {missing}')

    z = DIST / f'{slug}-FUTO.zip'
    z.unlink(missing_ok=True)
    with zipfile.ZipFile(z, 'w', zipfile.ZIP_DEFLATED) as f:
        for p in out.iterdir():
            if p.is_file():
                f.write(p, p.name)
    print(f'validated and rebuilt {z}')
