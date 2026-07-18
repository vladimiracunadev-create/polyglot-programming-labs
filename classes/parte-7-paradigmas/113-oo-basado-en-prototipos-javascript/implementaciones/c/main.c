#include <stdio.h>

struct Obj {
    long valor;
};

long doble(struct Obj *o) {
    return o->valor * 2;
}

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    struct Obj o = {n};
    printf("resultado=%ld\n", doble(&o));
    return 0;
}
