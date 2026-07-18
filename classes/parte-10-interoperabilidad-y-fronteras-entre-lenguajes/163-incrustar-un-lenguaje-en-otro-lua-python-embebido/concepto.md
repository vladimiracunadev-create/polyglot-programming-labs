# Concepto — Incrustar un lenguaje en otro (Lua, Python embebido)

Conocimiento independiente del lenguaje.

Entender el **incrustar un lenguaje en otro**: motores como Lua o Python se embeben en aplicaciones para permitir scripting sin recompilar. El anfitrión pasa datos al script, este los procesa y devuelve un resultado.

## Definiciones

- **Lenguaje embebido** — intérprete integrado en una aplicación anfitriona (Lua, Python). Clave: scripting sin recompilar.
- **Anfitrión** — la aplicación que hospeda el intérprete. Clave: expone datos y funciones al script.
- **Script embebido** — código interpretado que corre dentro del anfitrión. Clave: extiende la app.

## Forma neutral

```text
anfitrión pasa a, b ; el script suma ; devuelve el resultado
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
