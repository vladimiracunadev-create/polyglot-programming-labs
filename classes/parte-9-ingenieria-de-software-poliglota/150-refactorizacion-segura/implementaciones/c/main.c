#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    long viejo = n * 2, nuevo = n + n;
    printf("equivalente=%s resultado=%ld\n", viejo == nuevo ? "true" : "false", nuevo);
    return 0;
}
