#include <stdio.h>
#include <string.h>

int main(void) {
    char s[256];
    if (scanf("%255s", s) != 1) return 1;
    /* C: gestión manual; aquí no se copia ni se mueve, se usa directamente. */
    int longitud = (int) strlen(s);
    printf("movido=%s longitud=%d\n", s, longitud);
    return 0;
}
