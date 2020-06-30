import matplotlib.pyplot as plt
import sys
import json
import os
import numpy as np
import math

COLORS = ['#e66101',
          '#fdb863',
          '#b2abd2',
          '#5e3c99']


def loop_list(iterable):
    """
    Return a Generator that will infinitely repeat the given iterable.

    >>> l = loop_list(['sam', 'max'])
    >>> for i in range(1, 11):
    ...     print i, l.next()
    ...
    1 sam
    2 max
    3 sam
    4 max
    ...

    >>> l = loop_list(['sam', 'max'])
    >>> for i in range(1, 2):
    ...     print i, l.next()
    ...
    1 sam
    """
    iterable = tuple(iterable)
    n = len(iterable)
    num = 0
    while num < n:
        yield iterable[num]
        num += 1
        if num >= n:
            num = 0


if __name__ == "__main__":
    json_file_name = str(sys.argv[1])
    result_file_name = os.path.basename(os.path.splitext(json_file_name)[0])
    with open(json_file_name, 'r') as f:
        file_str = f.read()
        try:
            res_list = json.loads('[' + file_str[:-1] + ']')
        except Exception:
            res_list = json.loads('[' + file_str[:-2] + ']')

    uptime = []
    for func_stats in res_list:
        uptime.append(float(func_stats['func_data']['uptime']))

    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    plt.rc('font', size=20)
    plt.rc('text.latex', preamble=r'\usepackage{libertine}')
    # Declaring a figure "gnt"
    fig, plot = plt.subplots()
    plt.subplots_adjust(top=0.95, bottom=0.15, left=0.15, right=0.85)
    cdf = plot.twinx()

    # plot.set(title=f"IBM - {len(res_list)} requests - VM uptime")

    # Setting Y-axis limits
    # plot.set_ylim(0, len(res_list)*10)
    cdf.set_ylim(0, 1)

    # Setting X-axis limits
    # plot.set_xlim(0, 20000)

    # Setting labels for x-axis and y-axis
    plot.set_xlabel('VM uptime (s)')
    plot.set_ylabel('Instance count')
    cdf.set_ylabel('CDF')

    # Setting graph attribute
    plot.grid(True, which='both')

    maxup = math.ceil(max(uptime) / 50.0) * 50.0
    minup = math.floor(min(uptime) / 50.0) * 50.0
    bins = np.arange(minup-50, maxup+50, 25)
    # We pack uptimes in bins of 50 seconds. Likely to be the same host if
    # the gotten uptime is in in this 50 second margin.
    bins2 = np.arange(minup-50, maxup+50, 0.25)

    plot.set_xticks(bins, minor=True)

    plot.hist(uptime, bins=bins, rwidth=1, alpha=0.8, color=COLORS[0])

    cdf.hist(uptime, bins=bins2, cumulative=True, label='CDF',
             histtype='stepfilled', alpha=0.3, color=COLORS[-1], density=True)

    # plt.savefig("uptime/"+result_file_name+".pdf", dpi=1000, format='pdf')
    plt.savefig("uptime/"+result_file_name+".png", dpi=1000, format='png')
