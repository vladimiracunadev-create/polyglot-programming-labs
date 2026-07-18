#include <stdio.h>

int main(void) {
    long a, b;
    if (scanf("%ld %ld", &a, &b) != 2) return 1;
    printf("iguales=%s\n", a == b ? "true" : "false");
    return 0;
}
