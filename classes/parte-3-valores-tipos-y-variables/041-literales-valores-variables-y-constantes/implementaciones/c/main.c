#include <stdio.h>

int main(void) {
    double precio_unitario, descuento;
    long cantidad;

    /* C: tipos primitivos de tamaño fijo; scanf convierte el texto de entrada. */
    if (scanf("%lf %ld %lf", &precio_unitario, &cantidad, &descuento) != 3) {
        return 1;
    }

    double subtotal = precio_unitario * (double)cantidad;
    double total = subtotal * (1.0 - descuento);

    printf("Total: %.2f\n", total);
    return 0;
}
