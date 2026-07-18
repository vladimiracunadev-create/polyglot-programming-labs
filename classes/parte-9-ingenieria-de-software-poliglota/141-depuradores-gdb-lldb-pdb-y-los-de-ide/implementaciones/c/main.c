#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    long acc = 0;
    printf("traza=");
    for (long i = 1; i <= n; i++) {
        acc += i;
        if (i > 1) printf("-");
        printf("%ld", acc);
    }
    printf("\n");
    return 0;
}
