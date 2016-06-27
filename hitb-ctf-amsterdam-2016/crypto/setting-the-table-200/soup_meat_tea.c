// Soup Meat Tea (SMT) (TM)
//
// We welcome you to our delicious kitchen featuring many dishes from all
// around the world. With so many choices we really don't know the perfect
// combination. Fortunately our previous chef left the best set of dishes for
// a table of 8 people. Can you reconstruct the set of dishes?
//
// The service provided by our last chef can be found at.. find the ip/port
// as if it's a stego001 challenge :-)
//
// Compile with:    gcc -std=c99 soup_meat_tea.c -o soup_meat_tea
// Test with:       echo -n $'... payload ...'|./soup_meat_tea

#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <unistd.h>

uint32_t state = 42;

typedef enum {
    D_SOUP_CHICKEN,
    D_SOUP_MEAT,
    D_SOUP_NAZI,
    D_CHICKEN_RAW,
    D_CHICKEN_BLACK,
    D_MEAT_BLACKANGUS,
    D_MEAT_WAGYU,
    D_MEAT_HORSE,
    D_TIRAMISU,
    D_ICE_BANANA,
    D_ICE_STRAWBERRY,
    D_OVERFLOW,
} dish_t;

const char *dishes[] = {
    "soup-chicken", "soup-meat", "soup-nazi", "chicken-raw", "chicken-black",
    "meat-blackangus", "meat-wagyu", "meat-horse", "tiramisu", "ice-banana",
    "ice-strawberry",
};

void dish(uint8_t d)
{
    state = ((state + d) * 3294782) ^ 3159238819;
}

int main()
{
    uint8_t input[32];
    read(0, input, 32);

    for (uint32_t idx = 0; idx < 32; idx++) {
        dish(input[idx]);
    }

    printf("That's some delicious.. ");
    for (uint32_t idx = 0; idx < 32; idx++) {
        if(input[idx] < D_OVERFLOW) {
            printf("%s ", dishes[input[idx]]);
        }
        else {
            printf("%s ", "<YUEATTHIS>");
        }
    }

    if(state == 0xde11c105) {
        system("/bin/cat flag.txt");
    }
    return 0;
}
