#include <stdio.h>

static const char *tf(int x) {
    return x ? "true" : "false";
}

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    int pos = n > 0;
    int par = n % 2 == 0;
    printf("positivo=%s par=%s ambos=%s\n", tf(pos), tf(par), tf(pos && par));
    return 0;
}
