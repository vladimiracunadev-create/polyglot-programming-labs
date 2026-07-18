# Concepto — Dependencias, versiones y lockfiles

Conocimiento independiente del lenguaje.

Entender **dependencias, versiones y lockfiles**: el versionado semántico (SemVer) 'mayor.menor.parche' comunica compatibilidad. Descomponerlo es el primer paso para gestionar dependencias con criterio.

## Definiciones

- **Versionado semántico** — esquema mayor.menor.parche donde cada número señala el tipo de cambio. Clave: comunica compatibilidad.
- **Mayor/menor/parche** — cambios incompatibles / nuevas features / correcciones. Clave: guían las actualizaciones.
- **Lockfile** — archivo con las versiones exactas resueltas. Clave: builds reproducibles.

## Forma neutral

```text
LEER version ; separar por '.' ; ESCRIBIR componentes
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
