#include <stdio.h>
#include <string.h>

int main(void) {
    char tipo[32];
    if (scanf("%31s", tipo) != 1) return 1;
    const char *r;
    if (strcmp(tipo, "sistemas") == 0) r = "Rust";
    else if (strcmp(tipo, "web") == 0) r = "TypeScript";
    else if (strcmp(tipo, "datos") == 0) r = "SQL";
    else r = "Python";
    printf("lenguaje=%s\n", r);
    return 0;
}
