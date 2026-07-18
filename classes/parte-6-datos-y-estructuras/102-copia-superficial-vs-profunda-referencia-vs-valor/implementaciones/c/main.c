#include <stdio.h>

int main(void) {
    long v[1024];
    int n = 0;
    while (scanf("%ld", &v[n]) == 1) n++;
    long copia[1024];
    for (int i = 0; i < n; i++) copia[i] = v[i];
    copia[n - 1] = 99;
    printf("original=");
    for (int i = 0; i < n; i++) { if (i) printf("-"); printf("%ld", v[i]); }
    printf(" copia=");
    for (int i = 0; i < n; i++) { if (i) printf("-"); printf("%ld", copia[i]); }
    printf("\n");
    return 0;
}
