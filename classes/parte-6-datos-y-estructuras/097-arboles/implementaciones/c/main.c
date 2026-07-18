#include <stdio.h>
#include <stdlib.h>

int cmp(const void *a, const void *b) {
    long x = *(const long *) a, y = *(const long *) b;
    return (x > y) - (x < y);
}

int main(void) {
    long v[1024];
    int n = 0;
    while (scanf("%ld", &v[n]) == 1) n++;
    qsort(v, n, sizeof(long), cmp);
    printf("inorden=");
    for (int i = 0; i < n; i++) {
        if (i > 0) printf("-");
        printf("%ld", v[i]);
    }
    printf("\n");
    return 0;
}
