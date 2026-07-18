#include <stdio.h>

int main(void) {
    /* C variádico real usa stdarg.h; aquí sumamos leyendo la entrada. */
    long suma = 0, x;
    while (scanf("%ld", &x) == 1) {
        suma += x;
    }
    printf("suma=%ld\n", suma);
    return 0;
}
