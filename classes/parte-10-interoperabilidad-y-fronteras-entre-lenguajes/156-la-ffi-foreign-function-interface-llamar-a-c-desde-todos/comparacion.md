# Comparación — La FFI (Foreign Function Interface): llamar a C desde todos

| Clase de diferencia | Observación entre lenguajes |
|---|---|
| Sintáctica | ctypes/cffi (Python), extern (Rust/C), JNI (Java). |
| Semántica | La FFI cruza la frontera de lenguaje con una convención de llamada. |
| Paradigmática | SQL llama a funciones definidas por el usuario. |

## El concepto en la familia

ctypes (Python), extern "C" (Rust/C++), JNI (Java), cgo (Go): todos hacia C.
