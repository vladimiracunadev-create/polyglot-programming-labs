#include <stdio.h>

int main(void) {
    long x;
    int cuenta = 0;
    while (scanf("%ld", &x) == 1) cuenta++;
    printf("cuenta=%d\n", cuenta);
    return 0;
}
