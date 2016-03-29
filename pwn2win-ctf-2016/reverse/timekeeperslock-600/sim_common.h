#ifndef SIM_COMMON_H
#define SIM_COMMON_H

#include <iostream>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <assert.h>
#include <verilated.h>
#include <verilated_vcd_c.h>
#include "Vchip.h"
#include "pinout.h"

using namespace std;

static Vchip *chip;
static vluint64_t main_time = 0;
#if VM_TRACE
static VerilatedVcdC* tfp = NULL;
#endif

static inline void cycle_clock() {
	chip->pin_clk = 0; chip->eval();
	main_time++;
#if VM_TRACE
	if(tfp != NULL) tfp->dump(main_time);
#endif
	chip->pin_clk = 1; chip->eval();
	main_time++;
#if VM_TRACE
	if(tfp != NULL) tfp->dump(main_time);
#endif
}

static void reset_chip() {
	chip->pin_rstn = 0;
	chip->pin_keypad = 1;
	chip->pin_gps = 1;
	cycle_clock();
	chip->pin_rstn = 1;
}

static void create_chip(const char *vcd_filename = NULL) {
	chip = new Vchip;
#if VM_TRACE
	if (vcd_filename != NULL) {
		Verilated::traceEverOn(true);
		tfp = new VerilatedVcdC;
		chip->trace(tfp, 99);
		tfp->open(vcd_filename);
	}
#endif
	reset_chip();
}

static void finish_chip() {
#if VM_TRACE
	if (tfp != NULL) {
		tfp->close();
		delete tfp;
	}
#endif
	chip->final();
	delete chip;
}

static inline int char_to_uart(int c) {
	return (c <= 0) ? 0x3ff : 0x200 | (c << 1);
}

static void uart_input_chars(int c_keypad, int c_gps) {
	c_keypad = char_to_uart(c_keypad);
	c_gps = char_to_uart(c_gps);
	for (int i = 0; i < 10; i++) {
		chip->pin_keypad = c_keypad & 1;
		chip->pin_gps = c_gps & 1;
		for (int j = 0; j < 256; j++)
			cycle_clock();
		c_keypad >>= 1;
		c_gps >>= 1;
	}
}

static void uart_input_str(const char *s_keypad, const char *s_gps) {
	while (*s_keypad || *s_gps) {
		uart_input_chars(*s_keypad, *s_gps);
		if (*s_keypad) ++s_keypad;
		if (*s_gps)    ++s_gps;
	}
}

static void wait_processing() {
	// simulate a number of cycles sufficient for the circuit to compute a hash
	for (int i = 0; i < 800; i++)
		cycle_clock();
}

static int nmea_cksum(const char *s_gps) {
	int cksum = 0;
	for (; *s_gps != '\0' && *s_gps != '$'; ++s_gps);
	if (*s_gps == '$')
		++s_gps;
	for (; *s_gps != '\0' && *s_gps != '*'; ++s_gps)
		cksum ^= *s_gps;
	return cksum;
}

static void build_gps_str(char *buf, const size_t bufsz, const char *s_HHMM = NULL, const char *s_ddmmyy = NULL) {
	struct tm gmt;
	time_t curtime = time(NULL);
	gmtime_r(&curtime, &gmt);

	static char HHMM[8], ddmmyy[8];
	if (s_HHMM != NULL) {
		assert(strlen(s_HHMM) == 4);
		strncpy(HHMM, s_HHMM, sizeof(HHMM));
	}
	else {
		strftime(HHMM, sizeof(HHMM), "%H%M", &gmt);
	}
	if (s_ddmmyy != NULL) {
		assert(strlen(s_ddmmyy) == 6);
		strncpy(ddmmyy, s_ddmmyy, sizeof(ddmmyy));
	}
	else {
		strftime(ddmmyy, sizeof(ddmmyy), "%d%m%y", &gmt);
	}

	assert(strlen(HHMM)   == 4);
	assert(strlen(ddmmyy) == 6);

	size_t n = snprintf(buf, bufsz, "$GPRMC,%s00.000,A,1547.9730,S,4751.8510,W,0.02,31.66,%s,,,A*", HHMM, ddmmyy);
	snprintf(&buf[n], bufsz - n, "%02X", nmea_cksum(buf));
}

#endif
