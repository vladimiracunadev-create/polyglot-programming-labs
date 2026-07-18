# Incorporar un concepto o lenguaje

## Nuevo concepto

Copiar `plantillas/concepto`, asignar un identificador estable y completar primero `concepto.md`, `pseudocodigo.txt` y `casos.json`. Las implementaciones se agregan después: el problema común no debe adaptarse para favorecer un lenguaje.

## Nuevo lenguaje

1. Documentar su modelo de ejecución y sistema de tipos en `lenguajes/<id>.md`.
2. Crear una implementación idiomática en los módulos compatibles.
3. Registrar comandos reproducibles en `languages.json`.
4. Declarar explícitamente los conceptos que no tienen equivalencia directa.
5. Conservar las mismas entradas y salidas observables.

## Criterio de equivalencia

Dos soluciones no necesitan compartir estructura interna. Son comparables si resuelven el mismo contrato y permiten estudiar el mismo conocimiento. La equivalencia puede ser de resultado, comportamiento o intención; el laboratorio debe indicar cuál se está usando.
