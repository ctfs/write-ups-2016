#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv)
{
	printf("Since you're about to die anyway, I might as well tell you my secret!\n");
	printf("A single password will halt my machine, but you'll never figure it out!\n\n");

	size_t password_length = sizeof(uint32_t)*15 + 2;
	char *buffer = calloc(1, password_length);

	printf("Secret password: \n");
	fgets(buffer, password_length, stdin);
	uint32_t *ints = (uint32_t*) buffer;

	if (ints[0]  == 0x6f645f61 && ints[1]  == 0x64736d6f && ints[2]  == 0x645f7961 && 
		ints[3]  == 0x63697665 && ints[4]  == 0x73695f65 && ints[5]  == 0x6c6e6f5f &&
		ints[6]  == 0x73755f79 && ints[7]  == 0x6c756665 && ints[8]  == 0x5f66695f &&
		ints[9]  == 0x72657665 && ints[10] == 0x656e6f79 && ints[11] == 0x6f6e6b5f &&
		ints[12] == 0x615f7377 && ints[13] == 0x74756f62 && ints[14] == 0x0a74695f)
	{
		printf("Grr, I'll be back!\n");
	}
	else
	{
		printf("Mwahaha! You fools will never stop me! How could the answer be\n");
		printf("0x%08X 0x%08X 0x%08X 0x%08X 0x%08X 0x%08X 0x%08X 0x%08X 0x%08X 0x%08X 0x%08X 0x%08X 0x%08X 0x%08X 0x%08X?\n", 
				ints[0], ints[1], ints[2], ints[3], ints[4], ints[5], ints[6], ints[7], ints[8], ints[9], ints[10], ints[11],
				ints[12], ints[13], ints[14]);
	}

	return 0;
}
