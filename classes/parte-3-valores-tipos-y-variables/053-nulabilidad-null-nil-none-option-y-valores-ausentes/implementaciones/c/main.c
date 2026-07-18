#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    if (n == 0) {
        printf("valor=ausente\n");
    } else {
        printf("valor=%ld\n", n);
    }
    return 0;
}
