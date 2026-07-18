#include <stdio.h>

int main(void) {
    long ma, me, pa;
    if (scanf("%ld.%ld.%ld", &ma, &me, &pa) != 3) return 1;
    printf("mayor=%ld menor=%ld parche=%ld\n", ma, me, pa);
    return 0;
}
