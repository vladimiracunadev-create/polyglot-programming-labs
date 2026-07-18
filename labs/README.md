# 🧪 Laboratorios

> [⬅️ Volver al programa](../README.md) · [📚 Índice completo](../classes/README.md)

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

## Qué NO se verifica

El texto de las clases, las comparaciones y el Atlas están escritos a mano y **no** se ejecutan en
CI. Son material de lectura. El badge verde garantiza la equivalencia de las implementaciones, no la
prosa.
