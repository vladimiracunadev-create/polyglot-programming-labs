#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    printf("pares=");
    for (long i = 1; i <= n; i++) {
        if (i > 1) printf("-");
        printf("%ld", 2 * i);
    }
    printf("\n");
    return 0;
}
