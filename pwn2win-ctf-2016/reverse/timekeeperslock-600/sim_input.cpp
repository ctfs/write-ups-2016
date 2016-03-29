#include "sim_common.h"

int main(int argc, char** argv) {
	Verilated::commandArgs(argc, argv);
	if (argc != 3 && argc != 4) {
		cerr << "usage: " << argv[0] << " 'keypad_input' 'gps_input' [dump.vcd]" << endl;
		exit(1);
	}

	const char *s_keypad = argv[1];
	const char *s_gps = argv[2];
	const char *vcd_filename = argc == 4 ? argv[3] : NULL;

	create_chip(vcd_filename);
	uart_input_str(s_keypad, s_gps);
	wait_processing();

	cout << "lock: " << int(chip->pin_lock) << endl;

	finish_chip();
	return 0;
}
