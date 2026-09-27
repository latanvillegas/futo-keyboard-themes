# FUTO Keyboard Themes

Colección de temas personalizados para **FUTO Keyboard**, diseñados y mantenidos por **Latan Villegas**.

[![Build FUTO themes](https://github.com/latanvillegas/futo-keyboard-themes/actions/workflows/build-themes.yml/badge.svg)](https://github.com/latanvillegas/futo-keyboard-themes/actions/workflows/build-themes.yml)
[![Latest Release](https://img.shields.io/github/v/release/latanvillegas/futo-keyboard-themes)](https://github.com/latanvillegas/futo-keyboard-themes/releases/latest)

## Descargar

Los paquetes listos para instalar se publican en **GitHub Releases**:

**[Descargar la última versión](https://github.com/latanvillegas/futo-keyboard-themes/releases/latest)**

### Temas disponibles

| Tema | Estilo | ZIP v1.0.0 |
| --- | --- | --- |
| AMOLED Purple Neon | Negro AMOLED + neón morado | [Descargar](https://github.com/latanvillegas/futo-keyboard-themes/releases/download/v1.0.0/amoled-purple-neon-FUTO.zip) |
| AMOLED Purple Clean | AMOLED morado minimalista | [Descargar](https://github.com/latanvillegas/futo-keyboard-themes/releases/download/v1.0.0/amoled-purple-clean-FUTO.zip) |
| AMOLED Purple Cyberpunk | Morado futurista / cyberpunk | [Descargar](https://github.com/latanvillegas/futo-keyboard-themes/releases/download/v1.0.0/amoled-purple-cyberpunk-FUTO.zip) |
| Midnight Aurora | Azul, violeta y turquesa | [Descargar](https://github.com/latanvillegas/futo-keyboard-themes/releases/download/v1.0.0/midnight-aurora-FUTO.zip) |
| Obsidian Gold | Obsidiana negra + detalles dorados | [Descargar](https://github.com/latanvillegas/futo-keyboard-themes/releases/download/v1.0.0/obsidian-gold-FUTO.zip) |
| Ancient Arcane | Arcano, violeta y oro envejecido | [Descargar](https://github.com/latanvillegas/futo-keyboard-themes/releases/download/v1.0.0/ancient-arcane-FUTO.zip) |

## Compilación automática

Los temas se generan mediante `tools/build_themes.py`. GitHub Actions ejecuta el generador, crea los ZIP instalables y los publica como artifacts. Al publicar una Release, los ZIP se adjuntan automáticamente a la versión.

```text
definición del tema
       ↓
tools/build_themes.py
       ↓
PNG / WebP / theme.txt
       ↓
ZIP instalable
       ↓
GitHub Actions / Releases
```

## Estructura

```text
.github/workflows/       Automatización de builds y Releases
tools/                   Generadores de temas
themes/                  Documentación y fuentes por tema
build/                   Salida temporal del generador
dist/                    ZIP instalables generados
```

## Autor

**Latan Villegas**

## Licencias y créditos

Los diseños y assets originales están sujetos a `LICENSE.md` y/o a la licencia incluida en cada tema. Las tipografías y otros componentes de terceros conservan sus autores, avisos y licencias originales. Cuando un tema incluya componentes de terceros, sus créditos deben mantenerse separados de la autoría del diseño.

## FUTO Keyboard

Proyecto independiente de temas personalizados para FUTO Keyboard. No implica afiliación, patrocinio ni respaldo oficial de FUTO.
