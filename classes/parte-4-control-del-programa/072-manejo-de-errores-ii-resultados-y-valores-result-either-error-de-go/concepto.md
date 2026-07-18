# Concepto — Manejo de errores II: resultados y valores (Result/Either/error de Go)

Conocimiento independiente del lenguaje.

Manejar errores con **valores** en vez de excepciones: `Result`/`Either` (Rust, Haskell), el par `(valor, error)` de Go, u `Option`. El error deja de ser un salto de flujo y pasa a ser un dato que se maneja explícitamente.

## Definiciones

- **Result/Either** — tipo que contiene un valor de éxito o uno de error (Rust, Haskell). Clave: obliga a manejar ambos.
- **Valor de error** — devolver el error como dato en lugar de lanzarlo. Clave: flujo explícito.
- **Convención de Go** — devolver `(valor, error)` y comprobar `if err != nil`. Clave: errores visibles.
- **Manejo explícito** — el compilador o el estilo obligan a tratar el error. Clave: menos fallos silenciosos.

## Forma neutral

```text
LEER a, b
res <- dividir(a,b)  // devuelve Ok(v) o Err
SEGUN res: Ok(v)->"ok="v ; Err->"err=division"
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
