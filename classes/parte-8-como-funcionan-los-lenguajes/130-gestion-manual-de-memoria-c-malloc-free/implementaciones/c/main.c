#include <stdio.h>
#include <stdlib.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    long *arr = malloc(n * sizeof(long));
    long suma = 0;
    for (long i = 0; i < n; i++) {
        arr[i] = i + 1;
        suma += arr[i];
    }
    printf("reservado=%ld suma=%ld\n", n, suma);
    free(arr);
    return 0;
}
