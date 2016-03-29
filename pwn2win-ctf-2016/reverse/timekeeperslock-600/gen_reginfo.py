#!/usr/bin/python3
import sys, re

pin_clk = 'pin_G1'


def attrname(reg):
    if not reg.startswith('pin_'):
        return 'v__DOT__'+reg
    return reg


def gen(infile, outfile, print_stats=False):
    expr = re.compile(r'always\s*@\(\s*posedge\s+' +
                      re.escape(pin_clk) +
                      '\s*\)\s*if\s*\(\s*([^)]+)\s*\)\s*(\w+)\s*<=')
    regs = []
    for line in infile.readlines():
        m = expr.search(line)
        if m:
            regs.append(m.groups()[::-1])

    outfile.write('#ifndef REGINFO_H\n')
    outfile.write('#define REGINFO_H\n\n')

    outfile.write('static const int reg_num = %d;\n\n' % len(regs))

    outfile.write('static const char *reg_names[reg_num] = {\n%s\n};\n\n' %
                  ',\n'.join('\t"%s"'%reg for reg, en in regs))

    outfile.write('static const char *reg_en[reg_num] = {\n%s\n};\n\n' %
                  ',\n'.join('\t"%s"'%en for reg, en in regs))

    outfile.write('static void reg_snapshot(char *regs) {\n%s\n}\n\n' %
                  '\n'.join('\tregs[%5d] = chip->%s;' % (i, attrname(reg))
                          for i, (reg, en) in enumerate(regs)))

    outfile.write('static void reg_restore(const char *regs) {\n%s\n}\n\n' %
                  '\n'.join('\tchip->%s\t= regs[%5d];' % (attrname(reg), i)
                          for i, (reg, en) in enumerate(regs)))

    outfile.write('#endif\n')

    if print_stats:
        sys.stderr.write('Design has %d registers.\n\n' % len(regs))
        sys.stderr.write('EN\t#regs\n')
        sys.stderr.write('--\t-----\n')
        en_reg = {}
        for reg, en in regs:
            en_reg.setdefault(en, []).append(reg)
        for en in sorted(en_reg.keys()):
            en_r = en_reg[en]
            whichones = '\t('+', '.join(en_r)+')' if len(en_r) < 4 else ''
            sys.stderr.write('%s\t%s%s\n' % (en, len(en_r), whichones))


if __name__ == '__main__':
    if len(sys.argv) > 3 or (len(sys.argv) > 1 and sys.argv[1] == '-h'):
        sys.stderr.write('usage: %s [infile] [outfile]\n' % sys.argv[0])
        sys.exit(1)
    infile  = open(sys.argv[1], 'r') if len(sys.argv) > 1 else sys.stdin
    outfile = open(sys.argv[2], 'w') if len(sys.argv) > 2 else sys.stdout
    gen(infile, outfile, print_stats=True)

