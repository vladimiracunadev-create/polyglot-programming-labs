#include <stdio.h>

int main(void) {
    long a, b;
    if (scanf("%ld %ld", &a, &b) != 2) return 1;
    /* C no tiene excepciones: comprobar antes de dividir. */
    if (b == 0) {
        printf("error=division por cero\n");
    } else {
        printf("resultado=%ld\n", a / b);
    }
    return 0;
}
