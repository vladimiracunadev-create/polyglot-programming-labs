#include <stdio.h>

int main(void) {
    long x;
    int primero = 1;
    printf("doblados=");
    while (scanf("%ld", &x) == 1) {
        if (!primero) printf("-");
        printf("%ld", x * 2);
        primero = 0;
    }
    printf("\n");
    return 0;
}
