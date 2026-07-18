# Concepto — Orientado a eventos y callbacks

Conocimiento independiente del lenguaje.

Practicar el paradigma **orientado a eventos y callbacks**: en vez de un flujo lineal, se registran manejadores que reaccionan cuando ocurre un evento. Aquí un callback recolecta cada evento emitido.

## Definiciones

- **Evento** — suceso al que el programa reacciona (clic, mensaje, dato). Clave: dispara callbacks.
- **Callback** — función registrada para ejecutarse cuando ocurre el evento. Clave: no la llamas tú.
- **Inversión de control** — el sistema invoca tu código, no al revés. Clave: base de la GUI y del servidor.

## Forma neutral

```text
registrar callback ; PARA i de 1 a n: emitir(i) ; ESCRIBIR recolectados
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
