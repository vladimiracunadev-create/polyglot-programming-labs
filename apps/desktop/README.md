# 💻 App de escritorio — Polyglot Programming Labs

> [⬅️ Volver al programa](../../README.md) · [📱 App Android](../android/README.md) · [📥 Descargas](https://github.com/vladimiracunadev-create/polyglot-programming-labs/releases/latest)

Un ejecutable único que lleva **el curso entero dentro** y lo abre en tu navegador sin
conexión: las 176 clases con el código de los diez lenguajes resaltado, los 136 anexos de
primos, el Atlas, las rutas, el glosario, el buscador y la autoevaluación.

## Cómo funciona

El ejecutable trae empaquetado el sitio estático (`site/`, el mismo que se publica en
GitHub Pages), levanta un servidor **solo en `127.0.0.1`** y abre esa dirección en tu
navegador. Una ventana pequeña queda de fondo con el recuento de lo que hay dentro y los
accesos directos.

```text
[ejecutable] → sirve site/ en http://127.0.0.1:8765 → tu navegador muestra el curso
```

**Por qué un servidor local y no abrir los archivos con `file://`:** el buscador del portal
pide `busqueda.json` con `fetch`, y los navegadores bloquean esa petición bajo `file://`
por política de origen. Con un servidor de loopback el portal funciona completo — buscador
incluido — y **nada se expone a la red**: el socket escucha en la interfaz local, no en la
tarjeta de red.

## Descargar y usar

Baja `PolyglotProgrammingLabs-windows.exe` del
[último release](https://github.com/vladimiracunadev-create/polyglot-programming-labs/releases/latest)
y ejecútalo. No necesita instalación, ni Python, ni permisos de administrador.

Windows SmartScreen avisará de que el editor no está verificado: es lo normal en un
ejecutable sin firma de código comercial. *Más información → Ejecutar de todas formas*. El
[SHA256 publicado en el release](https://github.com/vladimiracunadev-create/polyglot-programming-labs/releases/latest)
permite comprobar que el archivo es el mismo que compiló CI:

```powershell
Get-FileHash .\PolyglotProgrammingLabs-windows.exe -Algorithm SHA256
```

## Ejecutarla desde el código

Funciona igual en Windows, macOS y Linux, con Python 3.10 o superior y sin dependencias:

```bash
python scripts/generar_sitio.py     # genera site/ desde las clases
python apps/desktop/main.py
```

Opciones: `--puerto N` para elegir puerto, `--no-abrir` para no lanzar el navegador y
`--no-gui` para dejar solo el servidor (útil por SSH o en un contenedor).

## Compilar el ejecutable

```bash
pip install pyinstaller
python scripts/generar_sitio.py
pyinstaller --onefile --windowed --name PolyglotProgrammingLabs \
            --add-data "site;site" apps/desktop/main.py
```

En macOS y Linux el separador de `--add-data` es `:` en vez de `;` (`"site:site"`).

Comprobación anti-vacío antes de distribuirlo — un ejecutable que arranca no prueba que
lleve el curso dentro:

```bash
python apps/desktop/verificar_exe.py dist/PolyglotProgrammingLabs.exe
```

Cuenta las páginas de clase **dentro del binario**; falla si no están las 176. Es el mismo
control que ejecuta el [workflow de build](../../.github/workflows/desktop.yml).

## Lo que esta app no hace

- **No ejecuta el verificador de equivalencia.** Eso necesita los toolchains de los diez lenguajes instalados; corre en tu equipo con `python scripts/verificar_equivalencia.py` o en CI.
- **No se actualiza sola.** Cada release trae el curso tal como estaba al compilarlo; para la versión viva está el [sitio](https://vladimiracunadev-create.github.io/polyglot-programming-labs/).
- **No tiene telemetría ni cuentas.** El progreso que marques vive en el almacenamiento local de tu navegador.
