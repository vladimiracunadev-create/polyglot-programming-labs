# Concepto — Pruebas de integración y el verificador de equivalencia

Conocimiento independiente del lenguaje.

Entender las **pruebas de integración** y el **verificador de equivalencia**: en vez de una unidad aislada, se comprueba que dos partes (o dos implementaciones) producen el mismo resultado. Es exactamente lo que hace el CI de este curso.

## Definiciones

- **Prueba de integración** — verifica que varias partes funcionan juntas. Clave: más allá de la unidad.
- **Equivalencia** — dos implementaciones dan el mismo resultado. Clave: base del verificador.
- **Regresión** — un cambio rompe algo que funcionaba. Clave: las pruebas la detectan.

## Forma neutral

```text
LEER x, y ; ESCRIBIR equivalente=(x==y)
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
