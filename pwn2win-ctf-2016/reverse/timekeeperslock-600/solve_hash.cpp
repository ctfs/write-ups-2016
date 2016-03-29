#include <stdlib.h>
#include <set>
#include "sim_common.h"
#include "reginfo.h"
#include "keypad_regs.h"

static const char *lock_reg_input_net = "n7127";

int main(int argc, char** argv) {
	Verilated::commandArgs(argc, argv);
	if (argc != 1 && (argc != 3 || strlen(argv[1]) != 4 || strlen(argv[2]) != 6)) {
		cerr << "usage: " << argv[0] << " [HHMM ddmmyy]" << endl;
		exit(1);
	}

	const char *s_keypad = "";
	static char s_gps[128];
	const char *s_HHMM   = argc == 3 ? argv[1] : NULL;
	const char *s_ddmmyy = argc == 3 ? argv[2] : NULL;

	build_gps_str(s_gps, sizeof(s_gps), s_HHMM, s_ddmmyy);

	create_chip(NULL);
	uart_input_str(s_keypad, s_gps);
	wait_processing();

	static char regs[reg_num];
	reg_snapshot(regs);

	FILE *fp = fopen("problem.spec", "w");
	if (fp == NULL) {
		perror("can't write to problem.spec");
		return 1;
	}
	// add constraint
	fprintf(fp, "=%s\t1\n", lock_reg_input_net);
	// add incognita
	set<int> exclude_reg;
	for (int i = 0; i < 256; i++) {
		for (int j = 0; keypad_regs[i][j] != -1; j++) {
			const int kreg = keypad_regs[i][j];
			exclude_reg.insert(kreg);
			if (strcmp(reg_en[kreg], "1'b1"))
				fprintf(fp, "%s\t?\n", reg_names[kreg]);
		}
	}
	// add register values
	for (int i = 0; i < reg_num; i++) {
		if (exclude_reg.find(i) == exclude_reg.end())
			fprintf(fp, "%s\t%d\n", reg_names[i], regs[i]);
	}
	fclose(fp);

	const int ret =
		system("./solve_circuit.py chip.v problem.spec");

	finish_chip();
	return 0;
}
