#include <stdio.h>
#include <stdlib.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    long *lista = malloc(n * sizeof(long));
    for (long i = 0; i < n; i++) lista[i] = n - i;
    printf("lista=");
    for (long i = 0; i < n; i++) {
        if (i > 0) printf("-");
        printf("%ld", lista[i]);
    }
    printf("\n");
    free(lista);
    return 0;
}
