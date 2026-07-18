#include <stdio.h>

void doblar(long *p) {
    *p *= 2;
}

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    long antes = n;
    doblar(&n);
    printf("antes=%ld despues=%ld\n", antes, n);
    return 0;
}
