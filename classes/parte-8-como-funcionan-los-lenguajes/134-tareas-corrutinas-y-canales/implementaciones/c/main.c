#include <stdio.h>

int main(void) {
    long x, maximo;
    if (scanf("%ld", &maximo) != 1) return 1;
    while (scanf("%ld", &x) == 1) {
        if (x > maximo) maximo = x;
    }
    printf("max=%ld\n", maximo);
    return 0;
}
