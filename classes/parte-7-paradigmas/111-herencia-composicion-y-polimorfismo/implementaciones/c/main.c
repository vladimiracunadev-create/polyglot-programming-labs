#include <stdio.h>
#include <string.h>

int main(void) {
    char tipo[32];
    if (scanf("%31s", tipo) != 1) return 1;
    const char *sonido;
    if (strcmp(tipo, "perro") == 0) sonido = "guau";
    else if (strcmp(tipo, "gato") == 0) sonido = "miau";
    else sonido = "muu";
    printf("sonido=%s\n", sonido);
    return 0;
}
