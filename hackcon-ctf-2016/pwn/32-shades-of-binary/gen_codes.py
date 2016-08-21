import random
import os

template = """#include <stdio.h>
#include <string.h>

int main() {
    char input[%s];
    printf("taking input at: %%p\\n", input);
    gets(input);
	return 0;
}
"""

mybins = []

# generate 100 binaries
for a in range(0, 100):
	b = random.randint(150, 500)
	b = str(b)
	code = template % (b,)

	fp = open('abc/' + b + '.c', 'w')
	fp.write(code)
	fp.close()
	command = 'gcc abc/' + b + '.c -m32 -fno-stack-protector -z execstack -o abc/' + b
	print command
	os.system(command)

	mybins.append(b)

print mybins
