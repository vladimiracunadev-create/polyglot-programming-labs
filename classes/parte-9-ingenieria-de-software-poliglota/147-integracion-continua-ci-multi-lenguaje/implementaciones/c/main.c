#include <stdio.h>

int main(void) {
    long x;
    int verde = 1;
    while (scanf("%ld", &x) == 1) {
        if (x != 1) verde = 0;
    }
    printf("ci=%s\n", verde ? "verde" : "rojo");
    return 0;
}
