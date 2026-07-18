#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    const char *par = (n % 2 == 0) ? "true" : "false";
    printf("entero=%ld real=%.1f par=%s\n", n, (double) n, par);
    return 0;
}
