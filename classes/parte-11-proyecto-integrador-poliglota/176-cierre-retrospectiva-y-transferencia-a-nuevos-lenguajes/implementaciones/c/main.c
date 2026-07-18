#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    printf("lecciones=%ld transferible=si\n", n);
    return 0;
}
