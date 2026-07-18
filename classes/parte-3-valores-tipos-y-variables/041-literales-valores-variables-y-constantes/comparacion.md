# Comparación — Literales, valores, variables y constantes

| Lenguaje | Declarar constante | Tipado | Mutabilidad por defecto | Formato decimal |
|---|---|---|---|---|
| Python | `PRECIO = 15000.0` (convención) | dinámico, fuerte | mutable | `f"{x:.2f}"` |
| JavaScript | `const precio = 15000` | dinámico, débil | mutable (`let`) | `x.toFixed(2)` |
| TypeScript | `const precio: number = 15000` | estático (inferido) | mutable (`let`) | `x.toFixed(2)` |
| Java | `final double precio = 15000` | estático, nominal | mutable | `String.format(Locale.US,"%.2f")` |
| C# | `const double Precio = 15000` | estático, nominal | mutable | `x.ToString("F2", Invariant)` |
| Go | `const precio = 15000.0` | estático, inferido | mutable | `fmt.Sprintf("%.2f")` |
| Rust | `let precio = 15000.0;` | estático, inferido | **inmutable** (`let mut` para mutar) | `format!("{:.2}")` |
| C | `const double precio = 15000;` | estático, tamaños fijos | mutable | `printf("%.2f")` |
| PHP | `const PRECIO = 15000;` / `$precio` | dinámico, débil | mutable | `sprintf("%.2f")` |
| SQL | `VALUES (15000.0)` (fila) | declarativo | — (no hay asignación) | `printf('%.2f')` |

## Las tres clases de diferencia aquí

- **Sintáctica:** el nombre, el `const`/`final`/`let`, el `;` final. Superficial.
- **Semántica:** si el tipo se fija y se comprueba, si el enlace puede mutar, cómo se convierte
  entre entero y real, qué tamaño tiene un número. Aquí están los bugs reales al portar.
- **Paradigmática:** SQL (y un funcional puro) no tienen "variable que se reasigna". El salto no
  es de sintaxis: es de forma de pensar el cálculo.

## Riesgos al traducir

- Copiar el formateo sin fijar la cultura ⇒ coma decimal en algunas máquinas.
- Asumir que `cantidad` es real cuando es entero (o al revés) ⇒ conversión implícita distinta.
- Esperar que Rust deje reasignar sin `mut` ⇒ error de compilación (a propósito).
