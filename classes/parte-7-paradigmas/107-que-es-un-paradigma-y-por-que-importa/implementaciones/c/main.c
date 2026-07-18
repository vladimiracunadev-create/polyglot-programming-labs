#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    long suma = 0;
    for (long i = 1; i <= n; i++) suma += i;
    printf("suma=%ld\n", suma);
    return 0;
}
