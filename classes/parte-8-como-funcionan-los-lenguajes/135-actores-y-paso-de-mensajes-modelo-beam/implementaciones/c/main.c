#include <stdio.h>

int main(void) {
    long total = 0, m;
    while (scanf("%ld", &m) == 1) {
        total += m; /* el 'actor' acumula cada mensaje */
    }
    printf("total=%ld\n", total);
    return 0;
}
