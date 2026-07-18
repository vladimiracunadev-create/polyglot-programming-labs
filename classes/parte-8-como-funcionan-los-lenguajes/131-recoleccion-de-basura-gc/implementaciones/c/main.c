#include <stdio.h>
#include <stdlib.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    for (long i = 0; i < n; i++) {
        long *tmp = malloc(sizeof(long)); /* en C se libera a mano */
        free(tmp);
    }
    printf("creados=%ld estado=recolectado\n", n);
    return 0;
}
