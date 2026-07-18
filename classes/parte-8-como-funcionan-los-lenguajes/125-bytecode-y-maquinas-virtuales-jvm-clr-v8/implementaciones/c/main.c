#include <stdio.h>

int main(void) {
    long x, y;
    char op;
    if (scanf("%ld %ld %c", &x, &y, &op) != 3) return 1;
    long r = op == '+' ? x + y : op == '-' ? x - y : x * y;
    printf("resultado=%ld\n", r);
    return 0;
}
