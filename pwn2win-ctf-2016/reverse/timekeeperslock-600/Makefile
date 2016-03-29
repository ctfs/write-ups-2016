ICESTORM ?= $(HOME)/git/icestorm
CXXFLAGS ?= -O -march=native -std=gnu++11

TASKS256 := 000-032 032-064 064-096 096-128 128-160 160-192 192-224 224-256
TASKS8 := 0 1 2 3 4 5 6 7

TOOLS := sim_input locate_keypad_regs analyze_hash_regs \
		sort_hash_regs solve_hash extract_hash

all: $(TOOLS)

chip.bitmap: bitfile/timekeeperslock.bin
	$(ICESTORM)/icepack/iceunpack $< $@
chip.v: chip.bitmap
	$(ICESTORM)/icebox/icebox_vlog.py -ls $< > $@


reginfo.h: chip.v gen_reginfo.py
	./gen_reginfo.py $< $@

keypad_regs.h: $(addprefix temp/,$(addsuffix .keypad_regs,$(TASKS256)))
	@echo '#ifndef KEYPAD_REGS_H' > $@
	@echo '#define KEYPAD_REGS_H' >>$@
	@echo 'static int keypad_regs[256][4] = {' >>$@
	cat temp/*.keypad_regs >>$@
	@echo '};' >>$@
	@echo '#endif' >>$@
temp/%.keypad_regs: locate_keypad_regs
	./locate_keypad_regs $(notdir $(basename $@)) > $@

hash_regs.h: sort_hash_regs
	./sort_hash_regs > $@

fig/hash_regs_always.svg fig/hash_regs_n4.svg: hash_regs_report.txt plot_hash_regs.py
	./plot_hash_regs.py $< $(subst always,1\'b1,$(patsubst fig/hash_regs_%.svg,%,$@)) $@
hash_regs_report.txt: $(addprefix temp/,$(addsuffix .hash_regs,$(TASKS8)))
	cat temp/*.hash_regs > $@
temp/%.hash_regs: analyze_hash_regs
	./analyze_hash_regs 11 10 > $@

verilog.py: verilog.grako
	pypy -m grako $< > $@


COMMONSRC=chip.v sim_common.h pinout.h

sim_input: %: %.cpp $(COMMONSRC)
	verilator --trace --Mdir obj_$@ --cc chip.v --exe $< -o $@
	$(MAKE) CXXFLAGS="$(CXXFLAGS)" -C obj_$@ -f Vchip.mk
	ln -sf obj_$@/$@ .

locate_keypad_regs analyze_hash_regs: %: %.cpp reginfo.h $(COMMONSRC)
	verilator --Mdir obj_$@ --cc chip.v --exe $< -o $@
	$(MAKE) CXXFLAGS="$(CXXFLAGS)" -C obj_$@ -f Vchip.mk
	ln -sf obj_$@/$@ .

sort_hash_regs: %: %.cpp reginfo.h keypad_regs.h $(COMMONSRC)
	verilator --Mdir obj_$@ --cc chip.v --exe $< -o $@
	$(MAKE) CXXFLAGS="$(CXXFLAGS)" -C obj_$@ -f Vchip.mk
	ln -sf obj_$@/$@ .

solve_hash: %: %.cpp reginfo.h keypad_regs.h verilog.py $(COMMONSRC)
	verilator --Mdir obj_$@ --cc chip.v --exe $< -o $@
	$(MAKE) CXXFLAGS="$(CXXFLAGS)" -C obj_$@ -f Vchip.mk
	ln -sf obj_$@/$@ .

extract_hash: %: %.cpp reginfo.h hash_regs.h $(COMMONSRC)
	verilator --Mdir obj_$@ --cc chip.v --exe $< -o $@
	$(MAKE) CXXFLAGS="$(CXXFLAGS)" -C obj_$@ -f Vchip.mk
	ln -sf obj_$@/$@ .

clean:
	rm -f chip.bitmap chip.v
	rm -f reginfo.h keypad_regs.h hash_regs.h
	rm -f hash_regs_report.txt
	rm -f verilog.py
	rm -f $(TOOLS)
	rm -rf obj_*
	rm -rf temp/*
