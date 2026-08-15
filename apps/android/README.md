# 📱 App Android — Polyglot Programming Labs

> [⬅️ Volver al programa](../../README.md) · [💻 App de Windows](../desktop/README.md) · [📥 Descargas](https://github.com/vladimiracunadev-create/polyglot-programming-labs/releases/latest)

El curso entero en el móvil, **sin conexión**: las 176 clases con el código de los diez
lenguajes a la vista, los 136 anexos de primos, los 136 de lenguajes vivos, las 60 fichas
de lenguaje del Atlas, las rutas, el glosario, el buscador y la autoevaluación. No hay
servidor, no hay cuenta y no se envía nada a ningún sitio: la app **es** el sitio de
GitHub Pages empaquetado dentro del APK.

## Qué lleva dentro

| Contenido | Cantidad |
|---|---:|
| Páginas HTML totales | 542 |
| README de clase | 176 |
| Anexos `primos.md` | 136 |
| Anexos `vivos.md` | 136 |
| Fichas de lenguaje del Atlas | 60 |
| README de parte | 12 |
| Portal (índice, Atlas, rutas, glosario, labs, autoevaluación, docs) | 22 |

Más la portada y el buscador, que se generan aparte.

El [workflow de build](../../.github/workflows/android.yml) **cuenta esas páginas dentro
del APK ya compilado** —las de clase, los dos tipos de anexo y las fichas— y falla si no
están. Un APK que compila no prueba que lleve el curso dentro; esa comprobación sí.

## Cómo está hecho

[Capacitor](https://capacitorjs.com/) envuelve el sitio estático en una WebView de
Android. No hay código de aplicación propio: `site/` se copia a `www/` y Capacitor genera
el proyecto nativo.

```text
apps/android/
├── capacitor.config.json    # appId, nombre y esquema
├── package.json             # @capacitor/core, /android y /cli
├── generar_recursos.py      # icono y splash, generados con Pillow
└── resources/               # icon.png 1024² · splash(-dark).png 2732²
```

`www/` y `android/` **no se versionan**: son artefactos de build que se generan en cada
compilación a partir de `site/`, que a su vez se genera de las clases. Así el APK no puede
quedarse con una copia vieja del curso.

## Compilarla tú

Requisitos: Node 20, Java 17 y el SDK de Android (o Android Studio).

```bash
python scripts/generar_sitio.py          # genera site/ desde las clases
cd apps/android
mkdir -p www && cp -r ../../site/* www/
npm install
npx cap add android
npx capacitor-assets generate --android  # icono y splash desde resources/
npx cap sync android
cd android && ./gradlew assembleDebug
```

El APK queda en `apps/android/android/app/build/outputs/apk/debug/app-debug.apk`.

Comprobación anti-vacío antes de instalarlo en ningún sitio:

```bash
unzip -l app-debug.apk "assets/public/classes/*" | grep -c 'README.html'
```

Debe dar **176**. Si da 0, el APK compiló pero va sin curso.

## Instalarla

El APK del [último release](https://github.com/vladimiracunadev-create/polyglot-programming-labs/releases/latest)
está firmado con la clave de depuración de Android, así que el sistema pedirá permiso para
instalar desde fuera de Play Store (Ajustes → *Instalar apps desconocidas*). Es la vía
normal para una app abierta que no se distribuye por tienda.

## Lo que esta app no hace

- **No sincroniza tu progreso.** Las marcas de clase leída viven en el almacenamiento local de la WebView; si desinstalas, se pierden.
- **No ejecuta código.** Es material de estudio: el verificador de equivalencia necesita los toolchains de los diez lenguajes y corre en tu equipo o en CI, no en el móvil.
- **No tiene telemetría.** Ninguna pantalla, búsqueda ni respuesta sale del dispositivo.
