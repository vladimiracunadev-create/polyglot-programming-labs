#include <stdio.h>

int main(void) {
    char comando[64], t[64];
    if (scanf("%63s", comando) != 1) return 1;
    int args = 0;
    while (scanf("%63s", t) == 1) args++;
    printf("comando=%s args=%d\n", comando, args);
    return 0;
}
