# Concepto — Reactivo y flujos de datos (streams)

Conocimiento independiente del lenguaje.

Practicar el paradigma **reactivo / de flujos (streams)**: procesar datos como una corriente que pasa por operadores (filtrar, mapear) encadenados. Aquí un flujo filtra pares y los duplica.

## Definiciones

- **Flujo/stream** — secuencia de datos procesada por etapas. Clave: filter/map encadenados.
- **Operador** — etapa que transforma el flujo (filter, map). Clave: se encadenan.
- **Reactivo** — reaccionar a datos que llegan con el tiempo. Clave: streams y observables.

## Forma neutral

```text
flujo(lista) |> filtrar(par) |> mapear(x->2x) |> recolectar
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
