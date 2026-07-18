#include <stdio.h>
#include <stdlib.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    printf("abs=%ld\n", labs(n));
    return 0;
}
