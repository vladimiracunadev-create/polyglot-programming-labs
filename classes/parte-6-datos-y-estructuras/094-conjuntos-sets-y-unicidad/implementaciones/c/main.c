#include <stdio.h>

int main(void) {
    long v[1024];
    int n = 0;
    while (scanf("%ld", &v[n]) == 1) n++;
    int unicos = 0;
    for (int i = 0; i < n; i++) {
        int repetido = 0;
        for (int j = 0; j < i; j++) {
            if (v[j] == v[i]) { repetido = 1; break; }
        }
        if (!repetido) unicos++;
    }
    printf("unicos=%d\n", unicos);
    return 0;
}
