#include <set>
#include "sim_common.h"
#include "reginfo.h"
#include "keypad_regs.h"

static void simulate_correct(char *regs) {
	const char *s_gps = "$GPRMC,110000.000,A,1547.9730,S,4751.8510,W,0.02,31.66,010415,,,A*61";
	const char *s_keypad = "01cd9de119e1231e29b0972a618da6c79fc1f3bd96cee86c93a8068bdc5e4c59";
	reset_chip();
	uart_input_str(s_keypad, s_gps);
	wait_processing();
	reg_snapshot(regs);
}

static void perturbate_keypad_bit(char *dest, const char *orig, const int nbit) {
	memcpy(dest, orig, reg_num * sizeof(char));
	for (int i = 0; keypad_regs[nbit][i] != -1; i++) {
		const int regn = keypad_regs[nbit][i];
		dest[regn] ^= 1;
	}
}

static int locate_hash_reg(set<const char*> accepted_en, const char *base_regs) {
	for (int regn = 0; regn < reg_num; regn++) {
		if (accepted_en.find(reg_en[regn]) == accepted_en.end())
			continue;  // not found

		// toggle the bit and check if it opens the lock
		static char regs[reg_num];
		memcpy(regs, base_regs, reg_num * sizeof(char));
		regs[regn] ^= 1;

		reg_restore(regs);
		cycle_clock();
		if (chip->pin_lock)
			return regn;
	}
	return -1;
}

int main(int argc, char** argv) {
	Verilated::commandArgs(argc, argv);

	if (argc != 1) {
		cerr << "usage: " << argv[0] << endl;
		exit(1);
	}

	create_chip(NULL);
	static char base_regs[reg_num];
	simulate_correct(base_regs);

	set<const char*> accepted_en;
	accepted_en.insert("n4");

	cout << "#ifndef HASH_REGS_H" << endl;
	cout << "#define HASH_REGS_H" << endl;
	cout << "static int hash_regs[] = {" << endl;

	for (int nbit = 0; nbit < 256; nbit++) {
		static char perturbated_base_regs[reg_num];
		perturbate_keypad_bit(perturbated_base_regs, base_regs, nbit);
		const int regn = locate_hash_reg(accepted_en, perturbated_base_regs);
		cout << "\t" << regn << ", \t// " << reg_names[regn] << endl;
	}

	cout << "};" << endl;
	cout << "#endif" << endl;

	finish_chip();
	return 0;
}