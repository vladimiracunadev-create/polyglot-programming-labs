#include <stdio.h>

long doble(long x) { return x * 2; }

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    printf("envuelto=wrap(%ld)\n", doble(n));
    return 0;
}
