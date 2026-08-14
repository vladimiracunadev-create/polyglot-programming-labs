# Política de seguridad

## Propósito del repositorio

Este es un **programa educativo de programación comparada**. Contiene material didáctico
(clases, código de ejemplo, un verificador de equivalencia) en 10 lenguajes del núcleo.
El código de ejemplo está pensado para **aprender**, no para ejecutarse en producción.

## Alcance

- Las **implementaciones de las clases** son ilustrativas: priorizan la claridad sobre la
  robustez. Algunas muestran a propósito construcciones (p. ej. `eval`, gestión manual de
  memoria) para enseñar el concepto y sus riesgos; **no deben copiarse a producción sin
  revisión**.
- El **tooling** (`scripts/`) se analiza con `bandit` y el repositorio se escanea con
  `gitleaks` en cada push (workflow [Security](.github/workflows/security.yml)).
- Las **apps** ([Android](apps/android/README.md) y [escritorio](apps/desktop/README.md))
  solo muestran contenido: no ejecutan el código de las clases, no piden permisos de red
  y no envían nada a ningún servidor. La de escritorio levanta un servidor **únicamente en
  `127.0.0.1`**, que es lo que permite que funcione el buscador del portal (bajo `file://`
  el navegador bloquea la petición de `busqueda.json`).

## Versiones con soporte

| Versión | Soporte |
|---|---|
| 1.0.x | ✅ correcciones de contenido y de tooling |
| < 1.0 | ❌ preliminar, sin soporte |

Los binarios publicados en los [releases](https://github.com/vladimiracunadev-create/polyglot-programming-labs/releases)
se compilan **en GitHub Actions**, no en una máquina personal, y cada release incluye un
`SHA256SUMS.txt` para comprobar que el archivo descargado es el que produjo CI. El APK va
firmado con la clave de depuración de Android y el `.exe` no lleva firma de código
comercial: ambos son artefactos de un proyecto abierto, no software comercial firmado.

## Reportar un problema

Si encuentras un problema de seguridad **en el tooling del repositorio** (los scripts, los
workflows) o un secreto filtrado por error:

1. **No abras un issue público** con el detalle.
2. Escribe a **[vladimir.acuna.dev@gmail.com](mailto:vladimir.acuna.dev@gmail.com)** con una descripción y, si es posible, pasos
   para reproducir.
3. Recibirás acuse de recibo y se coordinará la corrección.

Para erratas o mejoras del **contenido educativo**, abre un issue o un pull request normal.
