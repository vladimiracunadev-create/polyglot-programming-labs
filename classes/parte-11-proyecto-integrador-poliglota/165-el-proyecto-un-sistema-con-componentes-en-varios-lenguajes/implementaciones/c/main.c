#include <stdio.h>
#include <string.h>

int main(void) {
    char t[64];
    char buf[4096];
    buf[0] = '\0';
    int n = 0;
    while (scanf("%63s", t) == 1) {
        if (n > 0) strcat(buf, "-");
        strcat(buf, t);
        n++;
    }
    printf("componentes=%d nombres=%s\n", n, buf);
    return 0;
}
