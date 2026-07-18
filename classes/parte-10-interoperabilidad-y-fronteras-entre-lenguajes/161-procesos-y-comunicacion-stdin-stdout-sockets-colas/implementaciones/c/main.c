#include <stdio.h>

int main(void) {
    long recibido = 0, m;
    while (scanf("%ld", &m) == 1) recibido += m;
    printf("recibido=%ld\n", recibido);
    return 0;
}
