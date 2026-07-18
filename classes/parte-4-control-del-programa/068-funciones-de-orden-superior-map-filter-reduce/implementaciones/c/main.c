#include <stdio.h>

int main(void) {
    long x, total = 0;
    int primero = 1;
    printf("doblados=");
    long primeros[1024];
    int k = 0;
    while (scanf("%ld", &x) == 1) {
        primeros[k++] = x * 2;
    }
    for (int i = 0; i < k; i++) {
        if (!primero) printf("-");
        printf("%ld", primeros[i]);
        total += primeros[i];
        primero = 0;
    }
    printf(" total=%ld\n", total);
    return 0;
}
