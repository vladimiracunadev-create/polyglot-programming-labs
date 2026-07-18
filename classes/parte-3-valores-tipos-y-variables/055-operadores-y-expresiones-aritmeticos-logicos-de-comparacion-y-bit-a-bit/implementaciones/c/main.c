#include <stdio.h>

int main(void) {
    long a, b;
    if (scanf("%ld %ld", &a, &b) != 2) return 1;
    printf("suma=%ld resta=%ld mult=%ld div=%ld mod=%ld\n", a + b, a - b, a * b, a / b, a % b);
    return 0;
}
