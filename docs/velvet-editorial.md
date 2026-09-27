# Velvet Editorial

**Author:** Latan Villegas

Velvet Editorial is an advanced FUTO Keyboard theme with a matte black-plum editorial aesthetic, rose/copper accents, custom low-resolution 9-slice key borders, dedicated pressed/popup/action states, and an embedded Google Font.

## Typography

The build uses **Cormorant Garamond** from Google Fonts. The build script downloads the font from the official Google Fonts repository and packages its original OFL license as `OFL-CormorantGaramond.txt`.

The exported FUTO configuration assigns it through:

```toml
[options.font]
font = "CormorantGaramond-Regular.ttf"
```

## Assets

- `background.webp` — 1440×900 original background
- `normal.png` — 128×140 9-slice border
- `functional.png` — 128×140 9-slice border
- `action.png` — 128×140 Enter/action border
- `pressed.png` — 128×140 pressed state
- `popup.png` — 128×140 popup state
- `CormorantGaramond-Regular.ttf` — font asset

Specific matchrules are intentionally ordered before broad rules because FUTO applies only the first matching rule.
