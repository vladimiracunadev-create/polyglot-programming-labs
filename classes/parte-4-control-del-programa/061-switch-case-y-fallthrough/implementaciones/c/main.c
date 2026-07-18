#include <stdio.h>

int main(void) {
    long d;
    if (scanf("%ld", &d) != 1) return 1;
    const char *dia;
    switch (d) {
        case 1: dia = "lunes"; break;
        case 2: dia = "martes"; break;
        case 3: dia = "miercoles"; break;
        case 4: dia = "jueves"; break;
        case 5: dia = "viernes"; break;
        case 6: dia = "sabado"; break;
        case 7: dia = "domingo"; break;
        default: dia = "invalido";
    }
    printf("dia=%s\n", dia);
    return 0;
}
