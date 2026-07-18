#include <stdio.h>

int main(void) {
    long v[1024];
    int n = 0;
    while (scanf("%ld", &v[n]) == 1) n++;
    printf("pila=");
    for (int i = n - 1; i >= 0; i--) {
        if (i < n - 1) printf("-");
        printf("%ld", v[i]);
    }
    printf(" cola=");
    for (int i = 0; i < n; i++) {
        if (i > 0) printf("-");
        printf("%ld", v[i]);
    }
    printf("\n");
    return 0;
}
