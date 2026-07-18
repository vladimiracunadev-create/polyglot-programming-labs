#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    printf("eventos=");
    for (long i = 1; i <= n; i++) {
        if (i > 1) printf("-");
        printf("%ld", i);
    }
    printf("\n");
    return 0;
}
