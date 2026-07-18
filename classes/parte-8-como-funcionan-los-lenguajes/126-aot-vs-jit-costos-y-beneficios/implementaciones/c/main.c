#include <stdio.h>

int main(void) {
    int n;
    if (scanf("%d", &n) != 1) return 1;
    long r = 1;
    for (int i = 0; i < n; i++) r *= 2;
    printf("resultado=%ld\n", r);
    return 0;
}
