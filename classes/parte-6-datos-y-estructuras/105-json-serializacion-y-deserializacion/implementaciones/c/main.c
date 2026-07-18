#include <stdio.h>

int main(void) {
    char nombre[64];
    long edad;
    if (scanf("%63s %ld", nombre, &edad) != 2) return 1;
    printf("{\"nombre\": \"%s\", \"edad\": %ld}\n", nombre, edad);
    return 0;
}
