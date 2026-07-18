#include <stdio.h>

int main(void) {
    long c = 0, x;
    while (scanf("%ld", &x) == 1) c += x;
    printf("checksum=%ld\n", c);
    return 0;
}
