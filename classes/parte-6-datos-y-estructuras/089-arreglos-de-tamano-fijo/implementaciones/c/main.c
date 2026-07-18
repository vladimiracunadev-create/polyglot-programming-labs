#include <stdio.h>

int main(void) {
    long arr[3];
    if (scanf("%ld %ld %ld", &arr[0], &arr[1], &arr[2]) != 3) return 1;
    long suma = 0, max = arr[0];
    for (int i = 0; i < 3; i++) {
        suma += arr[i];
        if (arr[i] > max) max = arr[i];
    }
    printf("suma=%ld max=%ld\n", suma, max);
    return 0;
}
