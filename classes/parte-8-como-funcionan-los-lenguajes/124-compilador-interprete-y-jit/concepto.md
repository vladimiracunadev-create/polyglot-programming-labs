# Concepto — Compilador, intérprete y JIT

Conocimiento independiente del lenguaje.

Diferenciar **compilador, intérprete y JIT** por su forma de ejecutar. El programa (contar dígitos) es el mismo; lo que cambia entre modelos es cuándo y cómo se traduce a instrucciones de la máquina.

## Definiciones

- **Compilador** — traduce todo el programa a código máquina antes de ejecutar. Clave: rápido, errores antes.
- **Intérprete** — ejecuta la fuente instrucción a instrucción. Clave: flexible, más lento.
- **JIT** — compila a máquina las partes calientes durante la ejecución. Clave: combina ambos (V8, JVM).

## Forma neutral

```text
contar dígitos dividiendo por 10 hasta 0 (o longitud del texto)
```

Lo que cambia entre lenguajes es la sintaxis y la semántica (tipos, formato, conversión), no la idea.
