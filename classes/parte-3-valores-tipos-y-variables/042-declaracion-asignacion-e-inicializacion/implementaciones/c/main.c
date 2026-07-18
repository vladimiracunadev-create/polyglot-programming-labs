#include <stdio.h>

int main(void) {
    long a, b;
    if (scanf("%ld %ld", &a, &b) != 2) return 1;

    /* C exige una variable temporal para intercambiar. */
    long tmp = a;
    a = b;
    b = tmp;

    printf("a=%ld b=%ld\n", a, b);
    return 0;
}
