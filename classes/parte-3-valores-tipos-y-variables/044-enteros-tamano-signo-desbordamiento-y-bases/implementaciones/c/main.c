#include <stdio.h>

int main(void) {
    unsigned long n;
    if (scanf("%lu", &n) != 1) return 1;

    /* C no tiene especificador para binario: se construye a mano. */
    char bin[65];
    int i = 0;
    if (n == 0) {
        bin[i++] = '0';
    } else {
        char tmp[65];
        int j = 0;
        unsigned long t = n;
        while (t > 0) {
            tmp[j++] = (char) ('0' + (t & 1UL));
            t >>= 1;
        }
        while (j > 0) {
            bin[i++] = tmp[--j];
        }
    }
    bin[i] = '\0';

    printf("dec=%lu hex=%lx oct=%lo bin=%s\n", n, n, n, bin);
    return 0;
}
