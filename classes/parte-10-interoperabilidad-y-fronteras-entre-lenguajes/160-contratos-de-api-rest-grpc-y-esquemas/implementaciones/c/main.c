#include <stdio.h>

int main(void) {
    char metodo[16], recurso[64];
    if (scanf("%15s %63s", metodo, recurso) != 2) return 1;
    printf("contrato=%s /%s\n", metodo, recurso);
    return 0;
}
