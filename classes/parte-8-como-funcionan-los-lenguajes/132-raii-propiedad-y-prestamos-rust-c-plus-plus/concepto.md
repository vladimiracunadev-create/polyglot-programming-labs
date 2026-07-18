# Concepto — RAII, propiedad y préstamos (Rust/C++)

Conocimiento independiente del lenguaje.

Entender **RAII, propiedad y préstamos** como alternativa al GC. En Rust, un valor tiene un dueño y puede prestarse para leerlo sin copiarlo ni transferir la propiedad; se libera determinísticamente al salir del ámbito.

## Definiciones

- **RAII** — la vida del recurso se ata a la del objeto dueño. Clave: liberación determinista, sin GC.
- **Propiedad** — cada valor tiene un dueño responsable de liberarlo. Clave: base de Rust.
- **Préstamo** — referencia temporal para leer/usar sin tomar la propiedad. Clave: `&valor`.

## Forma neutral

```text
prestar n (referencia) a doble(&n) ; ESCRIBIR resultado
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
