#include <stdio.h>

int main(void) {
    long a, b, esperado;
    if (scanf("%ld %ld %ld", &a, &b, &esperado) != 3) return 1;
    printf("test=%s\n", a + b == esperado ? "pasa" : "falla");
    return 0;
}
