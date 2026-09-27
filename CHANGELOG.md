# Changelog

Todos los cambios importantes del proyecto se documentarán aquí.

## [1.0.0] - 2026-09-27

### Añadido

- AMOLED Purple Neon.
- AMOLED Purple Clean.
- AMOLED Purple Cyberpunk.
- Midnight Aurora.
- Obsidian Gold.
- Ancient Arcane.
- Generador automático de assets y paquetes FUTO.
- GitHub Actions para compilación automática.
- Publicación automática de ZIP en GitHub Releases.
- Licencia del proyecto y sistema de créditos para componentes de terceros.

### Infraestructura

- `tools/build_themes.py` como generador central.
- Artifact `futo-keyboard-themes` generado en cada compilación.
- Los eventos `release: published` compilan y adjuntan automáticamente los paquetes a la Release correspondiente.
