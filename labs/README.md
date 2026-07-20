# 🧪 Laboratorios

> [⬅️ Volver al programa](../README.md) · [📚 Índice completo](../classes/README.md) · [📊 Rúbrica de laboratorio](../docs/rubrica-evaluacion.md#3-rúbrica-de-laboratorio-verificador-de-equivalencia)

En este programa **el laboratorio es la equivalencia demostrada**. Cada clase construida trae sus
`implementaciones/<lenguaje>/` y un `casos.json`; el laboratorio consiste en **ejecutar todas las
implementaciones y comprobar que producen la misma salida**.

```bash
# Verificar una clase
python scripts/verificar_equivalencia.py 041

# Verificar todas las clases construidas
python scripts/verificar_equivalencia.py --all
```

Esto es lo que **verifica la CI** en cada push: no que un texto sea correcto, sino que las
implementaciones son **realmente equivalentes**. Los lenguajes sin toolchain instalado se omiten e
informan; SQL, declarativo, se marca como ilustrativo.

## El recorrido del laboratorio

Ejecutar el verificador es el paso mínimo. El laboratorio completo, tal como lo evalúa la
[rúbrica](../docs/rubrica-evaluacion.md#3-rúbrica-de-laboratorio-verificador-de-equivalencia), es:

1. **Instala varios toolchains.** Con uno solo no hay comparación posible; apunta al menos a cinco
   lenguajes del núcleo (la [Parte 2](../classes/parte-2-herramientas-toolchains-y-anatomia-de-comandos/README.md) te guía).
2. **Ejecuta el verificador sobre una parte completa** y lee el informe: qué pasó, qué se omitió y por qué.
3. **Rompe algo a propósito.** Cambia un `casos.json` o una implementación y observa cómo falla:
   entender el mensaje de error es la mitad del aprendizaje.
4. **Diagnostica.** Ante un fallo, clasifícalo: ¿es de entrada/salida, es una diferencia semántica
   real entre lenguajes, o falta un toolchain?
5. **Documenta una diferencia.** Anota al menos una diferencia observada entre dos salidas y
   clasifícala (sintáctica / semántica / paradigmática).

## El segundo laboratorio: los primos del Atlas

Cada clase de código trae además un [`primos.md`](../classes/parte-3-valores-tipos-y-variables/041-literales-valores-variables-y-constantes/primos.md)
con el mismo programa resuelto en los lenguajes **primos** de su familia. Ese material nació como
ilustrativo —nadie lo ejecutaba—, y ahora **Ruby, Perl y Lua sí se ejecutan** contra el mismo
`casos.json` que el núcleo:

```bash
python scripts/verificar_primos.py 041                 # una clase
python scripts/verificar_primos.py --all --lang perl   # un primo, todas las clases
python scripts/verificar_primos.py --all --estricto    # falla si alguno falla (lo que hace CI)
```

Mereció la pena a la primera pasada: al ejecutarlos aparecieron 19 clases cuyo Perl no hacía
`chomp`, de modo que el salto de línea se colaba en el dato y `"Ada"` medía 4 caracteres. Un
material que nadie ejecuta acumula ese tipo de defecto sin que se note.

Los otros 17 primos (Zig, Prolog, Objective-C, ActionScript…) siguen siendo **material de lectura**:
verificar tres de veinte no es verificarlos todos, y cada página lo declara.

## Qué NO se verifica

El texto de las clases, las comparaciones y el Atlas están escritos a mano y **no** se ejecutan en
CI. Son material de lectura. El badge verde garantiza la equivalencia de las implementaciones, no la
prosa.
