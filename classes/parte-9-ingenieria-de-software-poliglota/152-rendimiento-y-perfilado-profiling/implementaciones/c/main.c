#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    long ops = 0, suma = 0;
    for (long i = 1; i <= n; i++) {
        suma += i;
        ops++;
    }
    printf("operaciones=%ld resultado=%ld\n", ops, suma);
    return 0;
}
