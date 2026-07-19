# Clase 040 — Variables de entorno, rutas y el PATH en Windows y Unix

> Parte **2 — Herramientas, toolchains y anatomía de comandos** · ⏱️ Duración estimada: **75 min** · Nivel: **Fundamentos**
> ✅ **Clase construida.**

---

## 🎯 Objetivo

Entender el entorno donde corren tus comandos: las variables de entorno (configuración que el sistema pasa a los programas) y en especial el PATH, la lista de carpetas donde el sistema busca los ejecutables. Dominar esto explica el 90% de los errores tipo 'command not found' y las diferencias entre Windows y Unix.

## 📚 Resultados de aprendizaje

Al finalizar, podrás:

1. Explicar qué es una variable de entorno y para qué sirve el PATH.
2. Diagnosticar un 'command not found' a partir del PATH.
3. Reconocer las diferencias de rutas entre Windows y Unix.

## 🗺️ Temas

| # | Tema | Por qué importa |
|---|------|-----------------|
| 1 | Variables de entorno | Configuración que reciben los programas |
| 2 | El PATH | Dónde busca el sistema los ejecutables |
| 3 | Rutas Windows vs. Unix | Separadores, mayúsculas, barras |
| 4 | Diagnóstico | Por qué 'command not found' y cómo resolverlo |

## 📖 Definiciones y características

- **Variable de entorno** — valor con nombre que el sistema pasa a los programas (PATH, HOME). Clave: configura sin tocar el código.
- **PATH** — lista de carpetas donde se buscan los ejecutables. Clave: si un programa no está en el PATH, 'no se encuentra'.
- **Ruta absoluta vs. relativa** — desde la raíz (/usr/bin) o desde la carpeta actual (./main). Clave: evita ambigüedad sobre qué se ejecuta.
- **Separador de rutas** — ':' en Unix y ';' en Windows para el PATH; '/' vs. '\' en las rutas. Clave: fuente de errores multiplataforma.

## 🧩 Situación

Instalas una herramienta y la terminal responde 'command not found'. No está rota: simplemente su carpeta no está en el PATH, así que el sistema no sabe dónde buscarla. Añadirla al PATH lo resuelve.

## 🔎 Ejemplo

Ver y usar variables de entorno y el PATH:

```text
Unix (bash):
  echo $PATH                    # ver el PATH
  export API_KEY="abc123"       # definir una variable

Windows (PowerShell):
  $env:PATH                     # ver el PATH
  $env:API_KEY = "abc123"       # definir una variable
```

## ✍️ Práctica

Muestra tu PATH (`echo $PATH` o `$env:PATH`). Cuenta cuántas carpetas incluye. ¿Está la del lenguaje que instalaste?

## ⚠️ Errores comunes

- **Culpar al programa por 'command not found'** → causa: no revisar el PATH → solución: verificar si la carpeta del ejecutable está en el PATH
- **Escribir rutas con '/' en scripts de Windows (o al revés)** → causa: ignorar el separador del sistema → solución: usar rutas relativas o herramientas que abstraigan el separador

## ❓ Preguntas frecuentes

- **¿Dónde guardo secretos como una API key?** En variables de entorno, no en el código; nunca las subas al repositorio.
- **¿Por qué Windows y Unix difieren tanto?** Herencias históricas distintas; por eso el curso muestra ambos y prefiere lo portable.

## 🔗 Referencias

- W. Shotts — *The Linux Command Line* (2ª ed., No Starch Press) — [gratis online](https://linuxcommand.org/tlcl.php).
- B. W. Kernighan y R. Pike — *The Unix Programming Environment* (Prentice Hall).
- A. Hunt y D. Thomas — *The Pragmatic Programmer* (2ª ed., Addison-Wesley).

---

> [⏮️ Clase 039](../../parte-2-herramientas-toolchains-y-anatomia-de-comandos/039-empaquetado-y-distribucion-wheels-jars-binarios-contenedores/README.md) · [📂 Parte](../README.md) · [📚 Índice](../../README.md) · [🌐 Atlas](../../../atlas/README.md) · [Clase 041 ⏭️](../../parte-3-valores-tipos-y-variables/041-literales-valores-variables-y-constantes/README.md)
