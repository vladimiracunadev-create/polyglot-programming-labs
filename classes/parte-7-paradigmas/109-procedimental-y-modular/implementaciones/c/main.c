#include <stdio.h>

int main(void) {
    long v[1024];
    int n = 0;
    while (scanf("%ld", &v[n]) == 1) n++;
    long suma = 0;
    for (int i = 0; i < n; i++) suma += v[i];
    printf("promedio=%ld\n", suma / n);
    return 0;
}
