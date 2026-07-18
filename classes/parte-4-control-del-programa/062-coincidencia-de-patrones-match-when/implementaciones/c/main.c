#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    const char *signo = n > 0 ? "positivo" : (n < 0 ? "negativo" : "cero");
    printf("signo=%s\n", signo);
    return 0;
}
