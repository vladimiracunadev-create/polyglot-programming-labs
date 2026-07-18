#include <stdio.h>

int main(void) {
    long a;
    double b;
    if (scanf("%ld %lf", &a, &b) != 2) return 1;
    printf("suma=%.2f\n", (double) a + b);
    return 0;
}
