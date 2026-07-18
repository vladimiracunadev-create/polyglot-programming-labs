#include <stdio.h>

int main(void) {
    char clave[64], valor[64];
    if (scanf("%63s %63s", clave, valor) != 2) return 1;
    printf("guardado=%s=%s\n", clave, valor);
    return 0;
}
