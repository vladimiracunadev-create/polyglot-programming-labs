#include <stdio.h>

int main(void) {
    int codigo;
    if (scanf("%d", &codigo) != 1) return 1;
    const char *e;
    switch (codigo) {
        case 1: e = "sintaxis"; break;
        case 2: e = "tipos"; break;
        case 3: e = "enlace"; break;
        case 4: e = "ejecucion"; break;
        default: e = "desconocido";
    }
    printf("error=%s\n", e);
    return 0;
}
