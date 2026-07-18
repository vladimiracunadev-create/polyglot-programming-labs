#include <stdio.h>

/* C: se usa un valor de retorno para señalar el error (0 = ok, 1 = error). */
int dividir(long a, long b, long *out) {
    if (b == 0) return 1;
    *out = a / b;
    return 0;
}

int main(void) {
    long a, b, r;
    if (scanf("%ld %ld", &a, &b) != 2) return 1;
    if (dividir(a, b, &r) != 0) {
        printf("err=division\n");
    } else {
        printf("ok=%ld\n", r);
    }
    return 0;
}
