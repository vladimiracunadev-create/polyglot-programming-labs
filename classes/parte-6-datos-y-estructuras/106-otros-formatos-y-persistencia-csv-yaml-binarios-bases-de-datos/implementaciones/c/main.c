#include <stdio.h>

int main(void) {
    char tok[64];
    int campos = 0;
    printf("csv=");
    while (scanf("%63s", tok) == 1) {
        if (campos > 0) printf(",");
        printf("%s", tok);
        campos++;
    }
    printf(" campos=%d\n", campos);
    return 0;
}
