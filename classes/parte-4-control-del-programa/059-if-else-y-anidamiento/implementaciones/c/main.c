#include <stdio.h>

int main(void) {
    long score;
    if (scanf("%ld", &score) != 1) return 1;
    char nota;
    if (score >= 90) nota = 'A';
    else if (score >= 80) nota = 'B';
    else if (score >= 70) nota = 'C';
    else nota = 'F';
    printf("nota=%c\n", nota);
    return 0;
}
