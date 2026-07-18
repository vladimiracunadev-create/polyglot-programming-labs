#include <stdio.h>

/* C no tiene defectos: se simula pasando siempre el exponente. */
long potencia(long base, int exp) {
    long r = 1;
    for (int i = 0; i < exp; i++) r *= base;
    return r;
}

int main(void) {
    long base;
    int exp;
    int leidos = scanf("%ld %d", &base, &exp);
    if (leidos < 1) return 1;
    if (leidos < 2) exp = 2;
    printf("resultado=%ld\n", potencia(base, exp));
    return 0;
}
