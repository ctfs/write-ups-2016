import random
import os

template = """#include <stdio.h>
#include <string.h>

int main() {
        char *cap = "%s";
        char input[100];

        fgets(input, 100, stdin);
        input[strlen(input) - 1] = '\\0';

        if (!strncmp(cap, input, 100)) {
                printf("Yes\\n");
        } else {
                printf("Nope\\n");
        }
	return 0;
}
"""

mybins = []

# generate 100 binaries
for a in range(0, 100):
	b = random.randint(10, 45)
	cap = os.urandom(b).encode('hex')
	code = template % (cap,)

	fp = open('abc/' + cap + '.c', 'w')
	fp.write(code)
	fp.close()
	command = 'gcc abc/' + cap + '.c -o abc/' + cap
	print command
	os.system(command)

	mybins.append(cap)

print mybins
