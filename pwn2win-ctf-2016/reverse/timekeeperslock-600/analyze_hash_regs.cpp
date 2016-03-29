#include <map>
#include "sim_common.h"
#include "reginfo.h"

static int max_cumulative, num_samples;

class ResultMatrix {
	int **m;
public:
	ResultMatrix() {
		const size_t arr_size = num_samples * max_cumulative;
		m = new int*[num_samples];
		m[0] = new int[arr_size];
		memset(m[0], 0, arr_size*sizeof(int));
		for (int i = 1; i < num_samples; i++)
			m[i] = m[i-1] + max_cumulative;
	}
	~ResultMatrix() {
		delete [] m[0];
		delete [] m;
	}
	int *const&operator[] (size_t i) const {
		return m[i];
	}
};

class DateTimeIterator {
	time_t cur;
public:
	DateTimeIterator() {
		// Choose initial random time
		int fd = open("/dev/urandom", O_RDONLY);
		size_t sz = read(fd, &cur, sizeof(cur));
		assert(sz == sizeof(cur));
		close(fd);
		cur %= time(NULL);
	}
	void inc() {
		cur += 60;  // seconds
	}
	const char *gprmc() const {
		struct tm gmt;
		gmtime_r(&cur, &gmt);
		static char buf[128];
		size_t n = strftime(buf, sizeof(buf), "$GPRMC,%H%M%S.000,A,1547.9730,S,4751.8510,W,0.02,31.66,%d%m%y,,,A*", &gmt);
		snprintf(&buf[n], sizeof(buf) - n, "%02X", nmea_cksum(buf));
		return buf;
	}
};

static map<const char*, ResultMatrix> results;
static DateTimeIterator datetime;

void simulate(char *regs) {
	const char *s_keypad = "0000000000000000000000000000000000000000000000000000000000000000";
	reset_chip();
	uart_input_str(s_keypad, datetime.gprmc()); datetime.inc();
	wait_processing();
	reg_snapshot(regs);
}

void complete_sample(const int samplen) {
	static char base_regs[reg_num], cur_regs[reg_num], cumulative_change[reg_num];
	memset(cumulative_change, 0, sizeof(cumulative_change));
	simulate(base_regs);
	for (int i = 0; i < max_cumulative; i++) {
		simulate(cur_regs);
		for (int j = 0; j < reg_num; j++) {
			cumulative_change[j] |= cur_regs[j] != base_regs[j];
			if(cumulative_change[j])
				++results[reg_en[j]][samplen][i];
		}
	}
}

int main(int argc, char **argv) {
	Verilated::commandArgs(argc, argv);

	if (argc != 3
			|| sscanf(argv[1], "%d", &max_cumulative) != 1
			|| sscanf(argv[2], "%d", &num_samples) != 1) {
		cerr << "usage: " << argv[0] << " max_cumulative num_samples" << endl;
		exit(1);
	}

	create_chip(NULL);

	for (int i = 0; i < num_samples; i++)
		complete_sample(i);

	for (auto it = results.cbegin(); it != results.cend(); ++it) {
		const char *en = it->first;
		const ResultMatrix &m = it->second;
		for (int i = 0; i < max_cumulative; i++) {
			cout << en << "\t" << (i+1) << "\t";
			for (int j = 0; j < num_samples; j++) {
				cout << m[j][i] << "\t";
			}
			cout << endl;
		}

	}

	finish_chip();
	return 0;
}
