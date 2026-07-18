#include <stdio.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    printf("tareas=%ld estado=completado\n", n);
    return 0;
}
