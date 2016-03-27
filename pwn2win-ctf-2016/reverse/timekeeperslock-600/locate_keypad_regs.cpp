#include <map>
#include "sim_common.h"
#include "reginfo.h"

static void simulate(const int nbit, char *regs) {
	const char *s_gps = "$GPRMC,110000.000,A,1547.9730,S,4751.8510,W,0.02,31.66,010415,,,A*61";

	char s_keypad[128];
	int pos = 0;
	for (int nbyte = 31; nbyte >= 0; nbyte--) {
		const int shifted_nbit = nbit - 8*nbyte;
		const int byte = (shifted_nbit >= 0) && (shifted_nbit < 8)
				? (1 << shifted_nbit)
				: 0;
		pos += snprintf(&s_keypad[pos], sizeof(s_keypad) - pos, "%02x", byte);
	}

	reset_chip();
	uart_input_str(s_keypad, s_gps);
	wait_processing();
	reg_snapshot(regs);
}

int main(int argc, char** argv) {
	Verilated::commandArgs(argc, argv);

	int first_bit, last_bit;
	if (argc != 2 || sscanf(argv[1], "%d-%d", &first_bit, &last_bit) != 2) {
		cerr << "usage: " << argv[0] << " first_bit-last_bit" << endl;
		exit(1);
	}

	create_chip(NULL);
	static char base_regs[reg_num];
	simulate(-1, base_regs);

	map<const char *, int> en_stats;

	for (int nbit = first_bit; nbit < last_bit; nbit++) {
		static char cur_regs[reg_num];
		simulate(nbit, cur_regs);

		printf("\t{ ");
		for (int i = 0; i < reg_num; i++) {
			if (cur_regs[i] != base_regs[i])
				printf("%5d, ", i);
		}
		printf("%5d },\t// ", -1);
		for (int i = 0; i < reg_num; i++) {
			if (cur_regs[i] != base_regs[i]) {
				printf("\"%s\", ", reg_names[i]);
				++en_stats[reg_en[i]];
			}
		}
		printf("\n");
	}

	// Print stats
	cerr << endl;
	cerr << "EN\t#regs" << endl;
	cerr << "--\t-----" << endl;
	for (auto it = en_stats.cbegin(); it != en_stats.cend(); ++it)
		cerr << it->first << "\t" << it->second << endl;
	cerr << endl;

	finish_chip();
	return 0;
}