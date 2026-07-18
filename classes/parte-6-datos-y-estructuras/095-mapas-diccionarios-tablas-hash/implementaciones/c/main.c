#include <stdio.h>

int main(void) {
    long v[1024];
    int n = 0;
    while (scanf("%ld", &v[n]) == 1) n++;
    int cuenta = 0;
    for (int i = 0; i < n; i++) {
        if (v[i] == v[0]) cuenta++;
    }
    printf("cuenta=%d\n", cuenta);
    return 0;
}
