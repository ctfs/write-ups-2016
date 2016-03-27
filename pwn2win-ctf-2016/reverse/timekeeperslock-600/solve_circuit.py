#!/usr/bin/pypy
from __future__ import print_function, division, absolute_import, unicode_literals
from functools import reduce
from tempfile import NamedTemporaryFile
from subprocess import Popen
import re, sys, math

from verilog import *
from grako.exceptions import FailedParse


class TempVar(object):
    def __init__(self, var):
        assert var > 0
        self.var = var
    def __repr__(self):
        return '<TempVar %d>' % self.var


class Literal(object):
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return '<Literal %d>' % self.value
    def tseytin(self, problem, result):
        problem.add_clause((-1,  1), (self, result))
        problem.add_clause(( 1, -1), (self, result))


class Identifier(object):
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return '<Identifier %r>' % self.name
    def tseytin(self, problem, result):
        problem.add_clause((-1,  1), (self, result))
        problem.add_clause(( 1, -1), (self, result))


class BitwiseAnd(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b
    def __repr__(self):
        return '<BitwiseAnd %r, %r>' % (self.a, self.b)
    def tseytin(self, problem, result):
        problem.add_clause((-1, -1, 1), (self.a, self.b, result))
        problem.add_clause((1, -1), (self.a, result))
        problem.add_clause((1, -1), (self.b, result))


class BitwiseOr(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b
    def __repr__(self):
        return '<BitwiseOr %r, %r>' % (self.a, self.b)
    def tseytin(self, problem, result):
        problem.add_clause((1, 1, -1), (self.a, self.b, result))
        problem.add_clause((-1, 1), (self.a, result))
        problem.add_clause((-1, 1), (self.b, result))


class TernaryOp(object):
    def __init__(self, cond, ifT, ifF):
        self.cond = cond
        self.ifT = ifT
        self.ifF = ifF
    def __repr__(self):
        return '<TernaryOp %r ? %r : %r>' % (self.cond, self.ifT, self.ifF)
    def tseytin(self, problem, result):
        problem.add_clause(( 1,  1, -1), (self.cond, self.ifF, result))
        problem.add_clause((-1,  1, -1), (self.cond, self.ifT, result))
        problem.add_clause(( 1,  1, -1), (self.ifT, self.ifF, result))
        problem.add_clause((-1, -1,  1), (self.cond, self.ifT, result))
        problem.add_clause(( 1, -1,  1), (self.cond, self.ifF, result))


class Assignment(object):
    def __init__(self, ident, val):
        self.ident = ident
        self.val = val
    def __repr__(self):
        return '<Assignment %r = %r>' % (self.ident, self.val)


class verilogSemantics(object):
    def identifier(self, ast):
        return Identifier(ast)
    def literal(self, ast):
        if ast in {"0", "1'b0"}: return Literal(0)
        if ast in {"1", "1'b1"}: return Literal(1)
        raise ValueError('"%s" is not a valid literal' % str(ast))
    def primary_expr(self, ast):
        return ast
    def bitwiseand_expr(self, ast):
        return self._multiop(ast, BitwiseAnd)
    def bitwiseor_expr(self, ast):
        return self._multiop(ast, BitwiseOr)
    def ternary_expr(self, ast):
        if ast['override'] is not None:
            return ast['override']
        return TernaryOp(ast['cond'], ast['ifT'], ast['ifF'])
    def expr(self, ast):
        return ast
    def assignment(self, ast):
        return Assignment(ast['ident'], ast['val'])
    def _multiop(self, ast, cls):
        if len(ast) == 1:
            return ast[0]
        return reduce(cls, ast)


class Problem(object):
    def __init__(self):
        self.assignments = {}
        self.known_values = {}
        self.visited = set()
        self.queue = []
        self.var = {}
        self.num_var = 0
        self.clauses = []
        self.last_incognitum = 0

    def add_assignment(self, ast):
        assert isinstance(ast, Assignment)
        name, val = ast.ident.name, ast.val
        if name not in self.assignments:
            self.assignments[name] = val

    def add_known_value(self, name, value, is_constraint=False):
        self.known_values[name] = value
        if is_constraint:
            self.queue.append(name)

    def add_incognitum(self, name):
        self.visited.add(name)  # do not visit definition of incognita
        self.last_incognitum = self.get_var(name)  # assert incognita are the first vars

    def solve(self):
        self._tseytin()

        with NamedTemporaryFile(suffix='.cnf', mode='w') as f:
            f.write('p cnf %d %d\n' % (self.num_var, len(self.clauses)))
            for clause in self.clauses:
                f.write(' '.join(map(str, clause)) + ' 0\n')
            f.flush()
            with NamedTemporaryFile(mode='r') as outf:
                Popen(['minisat', f.name, outf.name]).wait()
                result = outf.read().split()

        if result[0] == 'UNSAT':
            return None

        bits = 0
        result = map(int, result[1:self.last_incognitum+1])
        for i, b in enumerate(result):
            if b == 0: break
            b = 1 if b > 0 else 0
            bits |= b << i
        return bits

    def get_var(self, name=None):
        if name is not None and name in self.var:
            return self.var[name]
        self.num_var += 1
        if name is not None:
            self.var[name] = self.num_var
        return self.num_var

    def _lookup(self, term):
        if isinstance(term, Identifier):
            name = term.name
            if name in self.known_values:
                return Literal(self.known_values[name])
            if name not in self.visited:
                self.queue.append(name)
        return term

    def _iter_queue(self):
        while len(self.queue) != 0:
            name = self.queue[0]
            self.queue = self.queue[1:]
            if name not in self.visited:
                self.visited.add(name)
                yield name

    def _tseytin(self):
        for name in self._iter_queue():
            self.assignments[name].tseytin(self, Identifier(name))


    def add_clause(self, sign, terms):
        assert len(sign) == len(terms)
        terms = map(self._lookup, terms)
        clause = []
        for s, term in zip(sign, terms):
            assert s in {-1, 1}
            if isinstance(term, Literal):
                assert term.value in {0, 1}
                val = term.value if s == 1 else not term.value
                if val: return  # clause always true
                else: continue  # term doesn't matter
            elif isinstance(term, Identifier):
                var = self.get_var(term.name)
            elif isinstance(term, TempVar):
                var = term.var
            else:
                var = self.get_var()
                term.tseytin(self, TempVar(var))
            clause.append(s * var)
        self.clauses.append(clause)


def main(verilog_filename, problem_filename):
    problem = Problem()
    with open(problem_filename) as problem_file:
        for line in problem_file.xreadlines():
            name, val = re.split(r'\s+', line.strip())
            if val == '?':
                problem.add_incognitum(name)
            elif val in {'0', '1'}:
                is_constraint = name.startswith('=')
                if is_constraint:
                    name = name[1:]
                problem.add_known_value(name, int(val), is_constraint)
            else:
                raise ValueError('Parsing error at line: %r', line.strip())
    with open(verilog_filename) as verilog_file:
        parser = verilogParser(parseinfo=False)
        for line in verilog_file.xreadlines():
            try:
                ast = parser.parse(line, 'assignment', semantics=verilogSemantics())
                problem.add_assignment(ast)
            except FailedParse as e:
                pass  # not an assignment
    result = problem.solve()
    if result is not None:
        fmt = '%%0%dx' % math.ceil(problem.last_incognitum / 4.)
        print(fmt % result)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.stderr.write('usage: %s chip.v problem.spec\n')
        sys.exit(1)
    verilog_filename = sys.argv[1]
    problem_filename = sys.argv[2]
    main(verilog_filename, problem_filename)
