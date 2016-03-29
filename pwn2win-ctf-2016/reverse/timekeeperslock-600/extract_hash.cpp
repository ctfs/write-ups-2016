#include "sim_common.h"
#include "reginfo.h"
#include "hash_regs.h"

static void extract_hash_regs(char *buf, const size_t bufsz, const char *regs) {
	size_t n = 0;
	for (int i = 255; i >= 0; i -= 8) {
		int byte = 0;
		for (int j = 0; j < 8; j++) {
			const int regn = hash_regs[i-j];
			byte <<= 1;
			byte |= regs[regn];
		}
		n += snprintf(&buf[n], bufsz - n, "%02x", byte);
	}
}

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

	static char buf[128];
	extract_hash_regs(buf, sizeof(buf), regs);
	cout << buf << endl;

	finish_chip();
	return 0;
}
