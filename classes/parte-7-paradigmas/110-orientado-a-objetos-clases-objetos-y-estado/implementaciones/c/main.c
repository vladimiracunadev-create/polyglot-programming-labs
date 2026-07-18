#include <stdio.h>

struct Contador {
    long cuenta;
};

void incrementar(struct Contador *c) {
    c->cuenta++;
}

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    struct Contador c = {0};
    for (long i = 0; i < n; i++) incrementar(&c);
    printf("cuenta=%ld\n", c.cuenta);
    return 0;
}
