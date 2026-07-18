#include <stdio.h>
#include <string.h>

int main(void) {
    char w[256];
    if (scanf("%255s", w) != 1) return 1;
    int n = (int) strlen(w);
    printf("invertido=");
    for (int i = n - 1; i >= 0; i--) putchar(w[i]);
    printf("\n");
    return 0;
}
