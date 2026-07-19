# Clase 037 — Formateadores y linters: black, prettier, gofmt, rustfmt, clang-format, php-cs-fixer

> Parte **2 — Herramientas, toolchains y anatomía de comandos** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

En la Parte 0 estudiaste que el código se lee muchas más veces de las que se escribe, y que la legibilidad no es estética sino mantenibilidad. Esta clase te da las dos herramientas que automatizan esa calidad sin esfuerzo manual: el **formateador**, que reescribe tu código con un estilo consistente (espaciado, sangría, saltos de línea), y el **linter**, que analiza el código en busca de errores probables y malas prácticas antes de ejecutarlo. El objetivo es que las distingas con claridad —una arregla el *aspecto*, la otra señala el *fondo*— y que sepas invocarlas en cada lenguaje del núcleo, porque en cualquier proyecto profesional corren automáticamente en el editor y en el CI.

La motivación de fondo la resume *The Pragmatic Programmer* con su insistencia en la automatización: todo lo que puede hacer una máquina de forma fiable no debería consumir atención humana. Discutir si van dos o cuatro espacios, o revisar a ojo si una variable quedó sin usar, es trabajo que una herramienta hace mejor y sin cansarse. Delegarlo libera la energía del equipo para lo que sí requiere criterio: la lógica.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Distinguir con precisión qué hace un formateador y qué hace un linter.
2. Nombrar e invocar el formateador y el linter de cada lenguaje del núcleo.
3. Comprobar formato sin modificar (`--check`) frente a aplicarlo, y saber cuándo usar cada modo.
4. Explicar por qué automatizar el estilo mejora la revisión de código y el trabajo en equipo.

## 🧩 Situación

En una revisión de código, el hilo de comentarios se llena de discusiones sobre espacios, comillas y dónde va la llave de apertura. Media hora de energía del equipo gastada en algo que a nadie le importa de verdad, mientras el bug real pasa desapercibido. En un equipo con formateador, esa discusión sencillamente no existe: `gofmt` o `black` deciden, todos aceptan, y las revisiones se concentran en si la lógica es correcta. La herramienta no solo ahorra tiempo: elimina una fuente entera de fricción interpersonal. Cuando el estilo deja de ser opinión y pasa a ser output de una herramienta, el equipo discute lo que importa.

## 📖 Dos herramientas, dos trabajos

El **formateador** es determinista y no opina sobre tu lógica: toma tu código, posiblemente desordenado, y lo reescribe siguiendo un estilo fijo. No cambia lo que el programa *hace*, solo cómo se ve. Su gran virtud es eliminar el estilo como tema de conversación. El ejemplo más radical es `gofmt`, el formateador de Go, que deliberadamente *no admite configuración*: hay un único estilo para toda la comunidad Go, y esa uniformidad es un rasgo cultural buscado, no una limitación. `black` en Python adopta la misma filosofía —«the uncompromising formatter», con poquísimas opciones—, y `rustfmt`, `prettier`, `clang-format` y `php-cs-fixer` cumplen el mismo papel en sus lenguajes.

El **linter** es analítico y sí mira el fondo: examina tu código en busca de patrones sospechosos que probablemente sean errores o malas prácticas, aunque el código compile y funcione. Una variable declarada y nunca usada, una comparación que siempre es verdadera, un recurso que no se cierra, un cast peligroso. `clippy` en Rust es célebre por sus sugerencias pedagógicas; `go vet` detecta errores sutiles en Go; `ruff` y `flake8` en Python, `eslint` en JS/TS. El linter no reescribe (aunque algunos ofrecen autofix para casos claros): *señala*, y tú decides corregir o justificar. Es una segunda lectura incansable de tu código, un revisor que nunca se distrae.

La distinción práctica es que **formateador y linter se usan juntos**, no uno en vez del otro. El formateador garantiza que todo el código *luzca* igual; el linter garantiza que no contenga trampas conocidas. Ambos se integran en dos lugares: en el editor, para verlos al escribir, y en el CI, para bloquear cambios que no cumplan. Y ambos ofrecen un modo `--check` que no modifica nada, solo informa si algo está mal formateado o sospechoso —ese es el modo que usa el CI, porque debe fallar sin tocar los archivos—.

## 🔬 Laboratorio guiado: formatear y analizar en cada lenguaje

Cada formateador tiene dos modos: aplicar (reescribe) y comprobar (`--check`, solo informa). Compara el comando de formateo del núcleo:

```bash
black archivo.py              # Python: reescribe con el estilo de black
black --check archivo.py      # solo comprueba; falla si habría cambios (modo CI)

prettier --write archivo.ts   # JS/TS: aplica el formato
prettier --check archivo.ts   # solo comprueba

gofmt -w archivo.go           # Go: -w escribe los cambios en el archivo
gofmt -l .                    # lista los archivos mal formateados, sin tocarlos

rustfmt archivo.rs            # Rust: formatea (o 'cargo fmt' en un proyecto)
cargo fmt --check             # comprueba todo el proyecto sin modificar

clang-format -i archivo.c     # C: -i edita el archivo en el sitio (in-place)
php-cs-fixer fix archivo.php  # PHP: aplica el estándar de estilo
```

Y el linter de cada uno, que señala problemas de fondo:

```bash
ruff check archivo.py         # Python: linter rápido (alternativa: flake8)
eslint archivo.ts             # JS/TS
go vet ./...                  # Go: análisis de errores probables
cargo clippy                  # Rust: sugerencias idiomáticas y de corrección
```

Observa el «antes y después» de un formateador. Parte de código desordenado pero válido:

```python
# antes: espaciado inconsistente, comillas mezcladas
def suma( a,b ):
  return a+b
x=suma(  1 , 2)
```

Tras `black archivo.py`, el mismo programa queda uniforme, con espaciado y sangría canónicos, sin que su comportamiento cambie en absoluto. La lección: no memorizas reglas de estilo, las delegas.

## ✍️ Práctica

Si tienes un formateador instalado, crea un archivo deliberadamente desordenado —espaciado irregular, sangría inconsistente, líneas demasiado largas— pero sintácticamente válido, y pásale el formateador (`black`, `prettier --write`, `gofmt -w`). Compara el antes y el después: ¿qué reglas aplicó?, ¿cambió el comportamiento del programa o solo su aspecto? Después ejecuta el modo `--check` sobre un archivo ya formateado y sobre uno sin formatear, y observa que en el primero no dice nada y en el segundo falla: ese es el mecanismo con el que el CI bloquea código mal formateado. Si tienes un linter, introduce a propósito una variable sin usar y córrelo (`ruff check`, `cargo clippy`): lee la advertencia y fíjate en que el programa *funcionaría*, pero el linter te avisa igual.

## ⚠️ Errores comunes

| Síntoma / mensaje | Causa y cómo arreglar |
|-------------------|-----------------------|
| Formatear a mano y discutir estilo en revisiones | Trabajo que hace una máquina. Delega en el formateador, integrado en el editor |
| El CI falla «por formato» sin decir qué línea | Corriste el modo `--check`: reformatea en local (`black .`, `gofmt -w`) y vuelve a subir |
| Ignorar todos los avisos del linter | Se dejan pasar bugs latentes. Trata cada aviso como una pista: corrígelo o justifícalo |
| Esperar que `gofmt` respete tu estilo personal | No es configurable a propósito. Go impone un único estilo comunitario |
| Confundir formateador con linter | Uno cambia el aspecto, el otro señala el fondo. Se usan juntos, no uno en vez del otro |

## ❓ Preguntas frecuentes

- **¿Formateador y linter son lo mismo?** No. El formateador reescribe el aspecto (espacios, sangría) sin tocar la lógica; el linter analiza el fondo y señala errores probables y malas prácticas. Se complementan y suelen correr ambos.
- **¿`gofmt` de verdad no se puede configurar?** Casi nada, y es intencional. Go sacrifica la personalización a cambio de que todo el código del ecosistema luzca igual, lo que facilita leer proyectos ajenos. `black` sigue una filosofía parecida.
- **¿El linter arregla los problemas o solo los señala?** Principalmente los señala; algunos ofrecen autofix (`ruff --fix`, `eslint --fix`) para casos inequívocos, pero muchas advertencias requieren tu criterio para decidir.
- **¿Cuándo se ejecutan estas herramientas?** Idealmente en tres momentos: al guardar en el editor (formateo automático), antes de hacer commit (un hook), y en el CI con `--check` para bloquear lo que no cumpla.

## 🔗 Referencias

- W. Shotts — *The Linux Command Line* (2ª ed., No Starch Press) — [gratis online](https://linuxcommand.org/tlcl.php).
- B. W. Kernighan y R. Pike — *The Unix Programming Environment* (Prentice Hall).
- A. Hunt y D. Thomas — *The Pragmatic Programmer* (2ª ed., Addison-Wesley), sobre automatización y consistencia del código.

---

> [⏮️ Clase 036](../../parte-2-herramientas-toolchains-y-anatomia-de-comandos/036-repl-e-interpretes-interactivos-por-lenguaje/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 038 ⏭️](../../parte-2-herramientas-toolchains-y-anatomia-de-comandos/038-pruebas-desde-la-terminal-pytest-node-test-go-test-cargo-test-dotnet-test-phpunit/README.md)
