#include <stdio.h>
#include <string.h>

int main(void) {
    char buf[1024];
    if (fgets(buf, sizeof buf, stdin) == NULL) return 1;
    buf[strcspn(buf, "\r\n")] = '\0';
    printf("eco: %s\n", buf);
    return 0;
}
