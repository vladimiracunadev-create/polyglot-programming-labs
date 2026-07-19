# 🧩 Ampliar el programa

> [⬅️ Volver al programa](../README.md) · [🧱 Currículo](CURRICULO.md) · [🧭 Metodología](METODOLOGIA.md) · [🤝 Contribuir](../CONTRIBUTING.md)

Cómo añadir una clase, un lenguaje al núcleo o una familia al Atlas sin romper la verificación.

> **Regla de oro:** el problema común **nunca** se adapta para favorecer a un lenguaje. Si un
> lenguaje no puede expresar el concepto, eso se documenta como hallazgo —no se cambia el
> `casos.json`.

## Cómo está montado el repositorio

Todo deriva de una fuente de verdad:

```text
scripts/curriculo.py     PARTES, BIBLIO (libros por parte), LIBROS_NUCLEO (libro por lenguaje)
        └── build.py     genera classes/_manifest.json, el índice, los README de parte
                         y las clases de método
        └── gen_parteN.py  genera las clases de código de cada parte
languages.json           el núcleo: nombre, extensión, comando de ejecución, modelo, familia
```

Scripts de apoyo:

| Script | Qué hace |
|---|---|
| [`verificar_equivalencia.py`](../scripts/verificar_equivalencia.py) | Ejecuta las implementaciones contra `casos.json` y compara salidas. |
| [`validar_estructura.py`](../scripts/validar_estructura.py) | Comprueba que las 176 clases y sus enlaces están bien formados. |
| [`generar_glosario.py`](../scripts/generar_glosario.py) | Deriva `glosario/README.md` de las definiciones de las clases. |
| [`enlazar_codigo.py`](../scripts/enlazar_codigo.py) | Enlaza cada bloque de código a la vista con su archivo real. |
| [`generar_sitio.py`](../scripts/generar_sitio.py) | Construye el sitio de GitHub Pages. |

> ⚠️ Los `gen_parteN.py` **regeneran** README de clase, y el contenido redactado a mano se
> perdería. No los re-ejecutes sobre clases ya escritas: están pensados para el alta inicial de
> una parte. `build.py` es seguro: solo crea las clases que faltan.

## Añadir una clase

1. Declárala en `PARTES`, dentro de [`scripts/curriculo.py`](../scripts/curriculo.py), con su
   título, tipo (`metodo` o de código) y objetivo. **Insertarla renumera** las siguientes: hazlo
   al final de una parte, o asume la renumeración global.
2. Ejecuta `python scripts/build.py` para regenerar el manifiesto, el índice y los README de parte.
3. Si es una clase de código, crea `casos.json` y `implementaciones/<lenguaje>/` para los 10
   lenguajes del núcleo.
4. Redacta el contenido siguiendo la [anatomía de clase](METODOLOGIA.md#anatomía-de-una-clase),
   con sus 🔗 referencias a los libros de la parte.
5. Verifica: `python scripts/verificar_equivalencia.py <NNN>` y `python scripts/validar_estructura.py`.

## Añadir un lenguaje al núcleo

Es la ampliación más cara: implica **una implementación por cada clase de código** (136 y
subiendo). Solo tiene sentido si el lenguaje aporta un modelo que el núcleo no cubre.

1. Regístralo en [`languages.json`](../languages.json) con `nombre`, `extension`, `run` (comando
   reproducible), `model` y `familia`.
2. Añade su libro de referencia a `LIBROS_NUCLEO` en `scripts/curriculo.py`.
3. Crea `implementaciones/<id>/` en **cada** clase de código, con código idiomático que lea de
   stdin y escriba la salida esperada por `casos.json`.
4. Añade el lenguaje a la matriz de [`.github/workflows/ci.yml`](../.github/workflows/ci.yml)
   para que se verifique en paralelo.
5. Declara explícitamente los conceptos que **no** tienen equivalencia directa en ese lenguaje.
6. Verifica todo: `python scripts/verificar_equivalencia.py --all --lang <id>`.

## Añadir una familia al Atlas

Mucho más barato, y suele ser la respuesta correcta: el [Atlas](../atlas/README.md) cubre
amplitud sin coste de mantenimiento.

1. Añade una cápsula en `atlas/README.md` bajo su familia, con **historia** (autor, año, motivo),
   **características** (paradigma, tipos, memoria/ejecución), **con qué se ejecuta**
   (compilador/intérprete y gestor de paquetes), el mapa **"si ya sabes X…"** y su **estado**
   (vivo / legado / nicho).
2. Enlaza la documentación oficial y respeta la fecha de última revisión: los datos históricos son
   estables, las herramientas no.
3. Solo hechos verificables. Ante la duda sobre un dato puntual, omítelo.

## Criterio de equivalencia

Dos soluciones no necesitan compartir estructura interna. Son comparables si resuelven el mismo
contrato y permiten estudiar el mismo conocimiento. La equivalencia puede ser **de resultado**,
**de comportamiento** o **de intención**; la clase debe indicar cuál se está usando. El
verificador comprueba la primera: misma entrada, misma salida.

## Antes de abrir el PR

```bash
python scripts/validar_estructura.py
python scripts/verificar_equivalencia.py --all
npx markdownlint-cli2 "**/*.md"
```

Y repasa la lista de comprobación de [CONTRIBUTING](../CONTRIBUTING.md).
