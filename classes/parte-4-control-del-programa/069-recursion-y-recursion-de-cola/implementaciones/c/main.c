#include <stdio.h>

long fib(long n) {
    return n < 2 ? n : fib(n - 1) + fib(n - 2);
}

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    printf("fib=%ld\n", fib(n));
    return 0;
}
