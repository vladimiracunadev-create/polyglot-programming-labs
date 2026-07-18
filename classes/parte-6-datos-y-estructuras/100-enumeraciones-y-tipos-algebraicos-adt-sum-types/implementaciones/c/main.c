#include <stdio.h>
#include <string.h>

int main(void) {
    char tipo[32];
    if (scanf("%31s", tipo) != 1) return 1;
    long area;
    if (strcmp(tipo, "cuadrado") == 0) {
        long l;
        if (scanf("%ld", &l) != 1) return 1;
        area = l * l;
    } else {
        long a, b;
        if (scanf("%ld %ld", &a, &b) != 2) return 1;
        area = a * b;
    }
    printf("area=%ld\n", area);
    return 0;
}
