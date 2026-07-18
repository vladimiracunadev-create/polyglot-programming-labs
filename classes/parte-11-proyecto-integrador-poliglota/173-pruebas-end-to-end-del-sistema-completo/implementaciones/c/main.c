#include <stdio.h>

int main(void) {
    long a, b, e;
    if (scanf("%ld %ld %ld", &a, &b, &e) != 3) return 1;
    printf("e2e=%s\n", a + b == e ? "pasa" : "falla");
    return 0;
}
