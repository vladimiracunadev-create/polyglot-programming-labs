#include <stdio.h>

struct Persona {
    char nombre[64];
    long edad;
};

int main(void) {
    struct Persona p;
    if (scanf("%63s %ld", p.nombre, &p.edad) != 2) return 1;
    printf("Persona(nombre=%s, edad=%ld)\n", p.nombre, p.edad);
    return 0;
}
