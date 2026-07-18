#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    long cuenta = 0;
    for (long i = 0; i < n; i++) cuenta++;
    printf("cuenta=%ld\n", cuenta);
    return 0;
}
