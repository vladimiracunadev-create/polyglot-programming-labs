#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    if (n > 0) {
        printf("resultado=%ld\n", n * 2);
    } else {
        printf("resultado=nada\n");
    }
    return 0;
}
