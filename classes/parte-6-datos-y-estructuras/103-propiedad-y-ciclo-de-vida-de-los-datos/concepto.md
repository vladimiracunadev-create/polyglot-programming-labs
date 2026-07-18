# Concepto — Propiedad y ciclo de vida de los datos

Conocimiento independiente del lenguaje.

Entender la **propiedad y el ciclo de vida** de los datos: cuándo se crea y cuándo se libera un recurso. RAII (Rust/C++), `defer` (Go), `try-with-resources` (Java) y `using` (C#) atan la liberación al ámbito.

## Definiciones

- **Ciclo de vida** — el tiempo entre que un recurso se crea y se libera. Clave: gestionarlo evita fugas.
- **RAII** — Resource Acquisition Is Initialization: el recurso se libera al destruirse el dueño. Clave: Rust/C++.
- **defer/using** — mecanismos que garantizan la liberación al salir del ámbito. Clave: Go, C#, Java.

## Forma neutral

```text
LEER n ; crear recurso ; usar ; liberar al salir del ámbito
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
