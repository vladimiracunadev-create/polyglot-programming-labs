#include <stdio.h>

int main(void) {
    long x;
    int primero = 1;
    printf("stream=");
    while (scanf("%ld", &x) == 1) {
        if (x % 2 == 0) {
            if (!primero) printf("-");
            printf("%ld", x * 2);
            primero = 0;
        }
    }
    printf("\n");
    return 0;
}
