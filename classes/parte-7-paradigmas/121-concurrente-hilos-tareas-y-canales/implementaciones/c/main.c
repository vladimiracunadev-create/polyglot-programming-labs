#include <stdio.h>

int main(void) {
    long v[1024];
    int n = 0;
    while (scanf("%ld", &v[n]) == 1) n++;
    int medio = n / 2;
    long p1 = 0, p2 = 0;
    for (int i = 0; i < medio; i++) p1 += v[i];
    for (int i = medio; i < n; i++) p2 += v[i];
    printf("suma=%ld\n", p1 + p2);
    return 0;
}
