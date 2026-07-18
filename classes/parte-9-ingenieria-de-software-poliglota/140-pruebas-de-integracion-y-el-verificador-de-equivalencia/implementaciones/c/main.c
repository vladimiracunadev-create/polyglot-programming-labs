#include <stdio.h>
#include <string.h>

int main(void) {
    char x[64], y[64];
    if (scanf("%63s %63s", x, y) != 2) return 1;
    printf("equivalente=%s\n", strcmp(x, y) == 0 ? "true" : "false");
    return 0;
}
