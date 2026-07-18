#include <stdio.h>

/* C no tiene 'private'; se usa una struct y funciones por convención. */
struct Cuenta {
    long saldo;
};

void depositar(struct Cuenta *c, long monto) {
    c->saldo += monto;
}

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    struct Cuenta c = {0};
    depositar(&c, n);
    depositar(&c, n);
    printf("saldo=%ld\n", c.saldo);
    return 0;
}
