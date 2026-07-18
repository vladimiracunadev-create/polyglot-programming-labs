#include <stdio.h>
#include <string.h>

int main(void) {
    char w[256];
    if (scanf("%255s", w) != 1) return 1;
    int valido = 1;
    for (int i = 0; w[i]; i++) {
        if (w[i] < 'a' || w[i] > 'z') valido = 0;
    }
    printf("valido=%s\n", valido ? "true" : "false");
    return 0;
}
