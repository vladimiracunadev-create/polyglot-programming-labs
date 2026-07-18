# Concepto — ABI, enlace y convenciones de llamada

Conocimiento independiente del lenguaje.

Entender el **ABI, el enlace y las convenciones de llamada**: para que dos piezas binarias se comuniquen, deben compartir la misma ABI (cómo se pasan los datos y se llaman las funciones). Un desajuste (p. ej. 32 vs 64 bits) rompe la interoperabilidad.

## Definiciones

- **ABI** — Application Binary Interface: cómo se representan datos y se llaman funciones a nivel binario. Clave: debe coincidir para enlazar.
- **Convención de llamada** — reglas de paso de argumentos y retorno. Clave: parte de la ABI.
- **API vs. ABI** — API es el contrato en código fuente; ABI, el binario. Clave: distinto nivel.

## Forma neutral

```text
LEER a, b ; compatible <- (a == b)
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
