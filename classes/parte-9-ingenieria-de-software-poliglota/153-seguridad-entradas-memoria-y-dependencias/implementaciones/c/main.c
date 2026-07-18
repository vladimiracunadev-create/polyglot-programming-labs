#include <stdio.h>
#include <ctype.h>

int main(void) {
    char w[256];
    if (scanf("%255s", w) != 1) return 1;
    int seguro = 1;
    for (int i = 0; w[i]; i++) {
        if (!isalnum((unsigned char) w[i])) seguro = 0;
    }
    printf("seguro=%s\n", seguro ? "true" : "false");
    return 0;
}
