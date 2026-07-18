# Concepto — Igualdad vs. identidad

Conocimiento independiente del lenguaje.

Distinguir **igualdad** (mismo valor) de **identidad** (mismo objeto en memoria). Con valores primitivos coinciden; con objetos no siempre, y cada lenguaje ofrece operadores distintos (`==` vs. `is`/`===`).

## Definiciones

- **Igualdad** — dos valores son iguales si representan lo mismo. Clave: `a == b`.
- **Identidad** — dos referencias apuntan al mismo objeto. Clave: `is` (Python), `===` no es exactamente eso en JS.
- **equals vs. ==** — en Java `==` compara referencias de objetos; `equals` compara valor. Clave: fuente de bugs.

## Forma neutral

```text
LEER a, b ; ESCRIBIR iguales=(a==b)
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
