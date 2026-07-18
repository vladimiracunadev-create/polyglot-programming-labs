#include <stdio.h>
#include <string.h>
#include <ctype.h>

int main(void) {
    char buf[4096];
    if (fgets(buf, sizeof buf, stdin) == NULL) return 1;
    buf[strcspn(buf, "\r\n")] = '\0';
    int caracteres = (int) strlen(buf);
    int palabras = 0, dentro = 0;
    for (int i = 0; buf[i]; i++) {
        if (isspace((unsigned char) buf[i])) {
            dentro = 0;
        } else if (!dentro) {
            dentro = 1;
            palabras++;
        }
    }
    printf("palabras=%d caracteres=%d\n", palabras, caracteres);
    return 0;
}
