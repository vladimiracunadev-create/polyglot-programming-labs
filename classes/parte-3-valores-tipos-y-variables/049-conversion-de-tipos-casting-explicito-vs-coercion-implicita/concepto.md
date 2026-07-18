# Concepto — Conversión de tipos: casting explícito vs. coerción implícita

Conocimiento independiente del lenguaje.

Distinguir **conversión explícita** (casting) de **coerción implícita**. Convertir un texto a real, y ese real a entero (truncando), muestra cómo cada lenguaje exige o realiza la conversión.

## Definiciones

- **Conversión (casting)** — cambiar el tipo de un valor explícitamente. Clave: `int(x)`, `(long)f`.
- **Coerción** — conversión automática que hace el lenguaje. Clave: fuente de sorpresas en los débilmente tipados.
- **Truncamiento** — descartar la parte decimal hacia cero. Clave: distinto de redondear.
- **Parseo** — interpretar un texto como un número. Clave: primer paso de casi toda entrada.

## Forma neutral

```text
LEER texto
real <- A_REAL(texto)
entero <- TRUNCAR(real)
ESCRIBIR "entero=" entero " real=" FORMATEAR(real,2)
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
