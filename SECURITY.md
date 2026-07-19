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

## Reportar un problema

Si encuentras un problema de seguridad **en el tooling del repositorio** (los scripts, los
workflows) o un secreto filtrado por error:

1. **No abras un issue público** con el detalle.
2. Escribe a **[vladimir.acuna.dev@gmail.com](mailto:vladimir.acuna.dev@gmail.com)** con una descripción y, si es posible, pasos
   para reproducir.
3. Recibirás acuse de recibo y se coordinará la corrección.

Para erratas o mejoras del **contenido educativo**, abre un issue o un pull request normal.
