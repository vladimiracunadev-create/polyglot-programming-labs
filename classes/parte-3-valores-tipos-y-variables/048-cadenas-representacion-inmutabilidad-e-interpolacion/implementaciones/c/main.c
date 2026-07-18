#include <stdio.h>
#include <string.h>

int main(void) {
    char buf[256];
    if (scanf("%255s", buf) != 1) return 1;
    printf("hola=%s longitud=%d\n", buf, (int) strlen(buf));
    return 0;
}
