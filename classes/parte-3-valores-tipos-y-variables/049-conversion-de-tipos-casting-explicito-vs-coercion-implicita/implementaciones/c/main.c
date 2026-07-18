#include <stdio.h>

int main(void) {
    double f;
    if (scanf("%lf", &f) != 1) return 1;
    printf("entero=%ld real=%.2f\n", (long) f, f);
    return 0;
}
