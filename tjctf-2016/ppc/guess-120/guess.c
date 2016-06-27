#include <stdio.h>
#include <stdlib.h>

int main() {
    int i;
    int num, guess;
    printf("Guess my number 100 times in a row and I'll give you the flag!\n");
    fflush(stdout);
    for (i = 0; i < 100; i++) {
        guess = 0;
        srand(time(NULL));
        num = rand();
        scanf("%d",&guess);
        if (guess == num) {
            printf("Correct!\n");
            fflush(stdout);
        } else {
            printf("Wrong.\n");
            printf("The answer was %d.\n",num);
            exit(0);
        }
    }
    printf("Congrats!\nFlag: ");
    char c;
    FILE *f = fopen("flag", "r");
    while ((c = fgetc(f)) != EOF) {
        putchar(c);
    }
    fclose(f);
    fflush(stdout);
}
