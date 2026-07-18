#include <stdio.h>

int main(void) {
    char t[256];
    int c = 0;
    while (scanf("%255s", t) == 1) c++;
    printf("componentes=%d\n", c);
    return 0;
}
