#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    long suma = 0;
    long i = 1;
    while (i <= n) {
        suma += i;
        i++;
    }
    printf("suma=%ld\n", suma);
    return 0;
}
