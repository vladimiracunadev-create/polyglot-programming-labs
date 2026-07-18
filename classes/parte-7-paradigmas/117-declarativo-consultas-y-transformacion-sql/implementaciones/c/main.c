#include <stdio.h>

int main(void) {
    long suma = 0, x;
    while (scanf("%ld", &x) == 1) {
        if (x % 2 == 0) suma += x;
    }
    printf("suma_pares=%ld\n", suma);
    return 0;
}
