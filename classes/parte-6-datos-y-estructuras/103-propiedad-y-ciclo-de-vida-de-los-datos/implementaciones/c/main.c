#include <stdio.h>
#include <stdlib.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    long *recurso = malloc(sizeof(long));
    *recurso = n;
    long valor = *recurso;
    free(recurso); /* liberación manual */
    printf("valor=%ld estado=liberado\n", valor);
    return 0;
}
