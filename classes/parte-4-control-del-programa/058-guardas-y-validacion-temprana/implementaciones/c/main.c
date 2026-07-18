#include <stdio.h>

int main(void) {
    long edad;
    if (scanf("%ld", &edad) != 1) return 1;
    if (edad < 0) {
        printf("invalido\n");
    } else if (edad < 18) {
        printf("menor\n");
    } else {
        printf("adulto\n");
    }
    return 0;
}
