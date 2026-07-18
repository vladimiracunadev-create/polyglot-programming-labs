#include <stdio.h>

long doble(const long *x) {
    return *x * 2; /* se accede por referencia sin copiar */
}

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    printf("resultado=%ld\n", doble(&n));
    return 0;
}
