#include <stdio.h>

int main(void) {
    long v[1024];
    int n = 0;
    while (scanf("%ld", &v[n]) == 1) n++;
    long indice = v[0];
    long *lista = v + 1; /* aritmética de punteros */
    printf("valor=%ld\n", *(lista + indice));
    return 0;
}
