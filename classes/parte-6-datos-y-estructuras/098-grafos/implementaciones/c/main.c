#include <stdio.h>

int main(void) {
    long v[2048];
    int n = 0;
    while (scanf("%ld", &v[n]) == 1) n++;
    int nodos = 0;
    for (int i = 0; i < n; i++) {
        int repetido = 0;
        for (int j = 0; j < i; j++) {
            if (v[j] == v[i]) { repetido = 1; break; }
        }
        if (!repetido) nodos++;
    }
    printf("aristas=%d nodos=%d\n", n / 2, nodos);
    return 0;
}
