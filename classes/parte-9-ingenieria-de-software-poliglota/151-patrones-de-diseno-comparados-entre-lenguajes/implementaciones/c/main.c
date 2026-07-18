#include <stdio.h>
#include <string.h>

int main(void) {
    char e[32];
    long a, b;
    if (scanf("%31s %ld %ld", e, &a, &b) != 3) return 1;
    long r;
    if (strcmp(e, "suma") == 0) r = a + b;
    else if (strcmp(e, "resta") == 0) r = a - b;
    else r = a * b;
    printf("resultado=%ld\n", r);
    return 0;
}
