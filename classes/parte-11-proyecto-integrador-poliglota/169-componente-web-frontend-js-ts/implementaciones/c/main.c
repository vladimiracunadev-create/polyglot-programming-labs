#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    printf("items=%ld render=ok\n", n);
    return 0;
}
