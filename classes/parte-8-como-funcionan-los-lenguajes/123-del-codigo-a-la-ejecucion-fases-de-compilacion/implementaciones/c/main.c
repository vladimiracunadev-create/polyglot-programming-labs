#include <stdio.h>

int main(void) {
    long a, b;
    char op;
    if (scanf("%ld %c %ld", &a, &op, &b) != 3) return 1;
    long r = op == '+' ? a + b : op == '-' ? a - b : a * b;
    printf("resultado=%ld\n", r);
    return 0;
}
