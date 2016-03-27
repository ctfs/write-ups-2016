#!/usr/bin/python3
import sys, re
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import beta
from lmfit import Model

def plt_rc():
    plt.rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
    plt.rc('text.latex', unicode=True)
    plt.rc('text.latex', preamble=[r"\usepackage{helvet}",
                                   r"\usepackage{nicefrac}",
                                   r"\DeclareSymbolFont{operators}{OT1}{phv}{sb}{n}",
                                   r"\DeclareSymbolFont{letters}{OML}{phv}{sb}{it}",
                                   r"\DeclareSymbolFont{symbols}{OMS}{cmsy}{sb}{n}",
                                   r"\DeclareSymbolFont{largesymbols}{OMX}{cmex}{sb}{n}"])
    plt.rc('text', usetex=True)

def read_results(f):
    res = {}
    for line in f.readlines():
        line = re.split(r'\s+', line.strip())
        en, num_cumulative = line[0], int(line[1])
        samples = map(int, line[2:])
        l = res.setdefault(en, {}).setdefault(num_cumulative, [])
        l += samples
    for en, dic in res.items():
        assert np.all(np.diff(list(sorted(dic.keys()))) == 1), \
               'num_cumulative must not have holes'
        res[en] = [dic[i] for i in sorted(dic.keys())]
    return res

def ClopperPearsonError(num_changes, num_random_bits, samples=1, alpha=.05):
    num_changes = np.array(num_changes)
    n = np.round(num_random_bits)
    x = n - num_changes
    x = x.clip(1e-12, n)
    x *= samples
    n *= samples
    # https://en.wikipedia.org/wiki/Binomial_proportion_confidence_interval#Clopper-Pearson_interval
    interv = np.vstack((beta.ppf(1.-alpha/2., x+1, n-x), beta.ppf(alpha/2., x, n-x+1)))
    interv = n * (1. - interv) / samples
    # convert to error
    interv[0,:] = num_changes - interv[0,:]
    interv[1,:] = interv[1,:] - num_changes
    return interv

def change(ncum, num_random_bits):
    return num_random_bits * (1. - 0.5**ncum)
change_model = Model(change)

def apply_model(res_matrix):
    num_changes_mean = np.array([np.mean(samples) for samples in res_matrix])
    ncum = np.arange(1, len(num_changes_mean) + 1)
    # pre-fit
    result = change_model.fit(num_changes_mean, ncum=ncum, num_random_bits=1)
    # estimate error
    err = ClopperPearsonError(num_changes_mean,
                              result.params['num_random_bits'].value,
                              samples=len(res_matrix))
    # final fit
    result = change_model.fit(num_changes_mean, ncum=ncum, num_random_bits=1,
                              weights=1./err.sum(axis=0))
    sys.stderr.write(result.fit_report()+'\n\n')
    return ncum, num_changes_mean, err, result

def plot_data_model(res_matrix, c, en):
    ncum, num_changes_mean, err, result = apply_model(res_matrix)

    nrandbit = int(np.round(result.params['num_random_bits'].value))
    plt.plot([ncum[0]-1, ncum[-1]+1], 2*[nrandbit], 'k--', alpha=.2, lw=3)

    plt.errorbar(ncum, num_changes_mean, yerr=err, fmt=c+'.')

    ncum = np.linspace(ncum[0], ncum[-1], 100)
    plt.plot(ncum, result.model.eval(params=result.params, ncum=ncum),
             c+'-', lw=2, alpha=.3)

    plt.ylabel(r'Mean change in registers enabled by \texttt{%s} (bits)' % en)
    plt.xlabel(r'Time after the initial snapshot (minutes)')

    ymin, ymax = num_changes_mean[0], min(nrandbit, num_changes_mean[-1])
    ymin, ymax = tuple(int(float(np.round(y))) for y in (ymin, ymax))
    ystep = (ymax-ymin)//8
    yticks = list(range(ymin, ymax+1, ystep))
    yticks = [y for y in yticks if y <= nrandbit-ystep//2]
    yticks.append(nrandbit)
    plt.yticks(yticks)
    plt.ylim(yticks[0]-ystep//2, yticks[-1]+ystep//2)

if __name__ == '__main__':
    if len(sys.argv) != 4:
        sys.stderr.write('usage: %s report.txt enable_sig fig.svg\n' % sys.argv[0])
        sys.exit(1)

    with open(sys.argv[1]) as f:
        res = read_results(f)

    enable_sig = sys.argv[2]
    out_fig = sys.argv[3]

    plt_rc()
    plot_data_model(res[enable_sig], 'r', enable_sig)
    plt.tight_layout()
    plt.savefig(out_fig)
