# Clase 039 — Empaquetado y distribución: wheels, jars, binarios, contenedores

> Parte **2 — Herramientas, toolchains y anatomía de comandos** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

Entender cómo se entrega un programa a quien lo va a usar. Según el lenguaje, el artefacto es una wheel (Python), un jar (Java), un binario (Go/Rust/C) o una imagen de contenedor (Docker) que empaqueta el programa con su entorno. Empaquetar bien es la diferencia entre 'funciona en mi máquina' y 'funciona en cualquier parte'.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Nombrar el formato de distribución típico de cada lenguaje.
2. Explicar qué resuelve un contenedor frente a distribuir solo el artefacto.
3. Relacionar el empaquetado con la reproducibilidad.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Formatos de artefacto | wheel, jar, binario, dll |
| 2 | El binario autocontenido | Go y Rust producen un solo archivo |
| 3 | Contenedores | Empaquetan el programa con su entorno |
| 4 | Distribución | Repositorios, registries y releases |

## 📖 Definiciones y características

- **Empaquetado** — preparar un programa y sus dependencias para distribuirlo. Clave: define cómo lo instala el usuario final.
- **wheel/jar** — formatos empaquetados de Python y Java. Clave: instalables sin recompilar.
- **Binario autocontenido** — un único ejecutable con todo dentro (típico de Go). Clave: se copia y corre sin instalar nada más.
- **Contenedor** — imagen que incluye el programa y su sistema operativo mínimo (Docker). Clave: elimina el 'funciona en mi máquina'.

## 🧩 Situación

Un servicio en Python funciona en desarrollo pero falla en producción por una versión distinta de una librería del sistema. Empaquetarlo en un contenedor lleva el entorno entero consigo, y el problema desaparece.

## 🔎 Ejemplo

Formato de distribución por lenguaje:

```text
Python   wheel (.whl) / sdist       → pip install
Java     jar (.jar)                → java -jar app.jar
Go/Rust  binario único             → copiar y ejecutar
C#       dll / ejecutable .NET
Cualquiera  imagen Docker          → docker run
```

## ✍️ Práctica

Piensa cómo entregarías un programa a alguien sin tu entorno: ¿un binario, una wheel, un contenedor? Justifica según el lenguaje.

## ⚠️ Errores comunes

- **Distribuir el código fuente y pedir 'que lo compilen'** → causa: trasladar la complejidad al usuario → solución: entregar un artefacto o imagen lista para usar
- **Asumir que el entorno destino es igual al tuyo** → causa: el clásico 'en mi máquina funciona' → solución: empaquetar el entorno con un contenedor cuando importe

## ❓ Preguntas frecuentes

- **¿Un contenedor es una máquina virtual?** No: comparte el kernel del host, es más ligero; empaqueta el entorno, no un SO completo.
- **¿Por qué Go es cómodo de distribuir?** Compila a un binario estático único: se copia y funciona sin dependencias externas.

## 🔗 Referencias

- W. Shotts — *The Linux Command Line* (2ª ed., No Starch Press) — [gratis online](https://linuxcommand.org/tlcl.php).
- B. W. Kernighan y R. Pike — *The Unix Programming Environment* (Prentice Hall).
- A. Hunt y D. Thomas — *The Pragmatic Programmer* (2ª ed., Addison-Wesley).

---

> [⏮️ Clase 038](../../parte-2-herramientas-toolchains-y-anatomia-de-comandos/038-pruebas-desde-la-terminal-pytest-node-test-go-test-cargo-test-dotnet-test-phpunit/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 040 ⏭️](../../parte-2-herramientas-toolchains-y-anatomia-de-comandos/040-variables-de-entorno-rutas-y-el-path-en-windows-y-unix/README.md)
