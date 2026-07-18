#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    /* C no tiene async a nivel de lenguaje; se calcula el resultado. */
    printf("resultado=%ld\n", n * 2);
    return 0;
}
