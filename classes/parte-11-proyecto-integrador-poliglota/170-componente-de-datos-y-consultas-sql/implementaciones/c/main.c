#include <stdio.h>

int main(void) {
    long total = 0, x;
    while (scanf("%ld", &x) == 1) total += x;
    printf("total=%ld\n", total);
    return 0;
}
