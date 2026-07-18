# Concepto — Números reales: punto flotante, precisión y decimales

Conocimiento independiente del lenguaje.

Trabajar con números de punto flotante y su formateo. El foco: los reales son **aproximados** (`0.1 + 0.2` no es exactamente `0.3`), y por eso casi siempre se muestran con un número fijo de decimales usando un formato que fuerza la cultura (punto, no coma).

## Definiciones

- **Punto flotante** — representación binaria aproximada de números reales (IEEE 754). Clave: no todos los decimales son exactos.
- **Precisión** — cuántos dígitos significativos conserva un real. Clave: limitada; genera pequeños errores.
- **Formateo** — convertir el real a texto con N decimales. Clave: cómo se presenta el resultado.
- **Cultura invariante** — formato que usa el punto decimal sin importar el idioma del sistema. Clave: evita la coma decimal.

## Forma neutral

```text
LEER a, b
ESCRIBIR "suma=" FORMATEAR(a+b,2) " producto=" FORMATEAR(a*b,2)
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
