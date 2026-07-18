#include <stdio.h>

static const char *tf(int x) {
    return x ? "true" : "false";
}

int main(void) {
    int a, b;
    if (scanf("%d %d", &a, &b) != 2) return 1;
    a = a != 0;
    b = b != 0;
    printf("and=%s or=%s not_a=%s\n", tf(a && b), tf(a || b), tf(!a));
    return 0;
}
