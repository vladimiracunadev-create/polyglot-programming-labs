#include <stdio.h>

int main(void) {
    long a, b;
    if (scanf("%ld %ld", &a, &b) != 2) return 1;
    long suma = 0;
    printf("rango=");
    for (long i = a; i <= b; i++) {
        if (i > a) printf("-");
        printf("%ld", i);
        suma += i;
    }
    printf(" suma=%ld\n", suma);
    return 0;
}
