import matplotlib.pyplot as plt
import sys
import json
import os

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
    result_file_name = os.path.splitext(json_file_name)[0]
    plot_file_name = 'plots/' + os.path.basename(result_file_name)
    with open(json_file_name, 'r') as f:
        file_str = f.read()
        try:
            res_list = json.loads('[' + file_str[:-1] + ']')
        except Exception:
            res_list = json.loads('[' + file_str[:-2] + ']')

    stats_by_instance = {}
    for func_stats in res_list:
        if func_stats['instance'] not in stats_by_instance:
            stats_by_instance[func_stats['instance']] = [func_stats]
        else:
            stats_by_instance[func_stats['instance']].append(func_stats)

    for k, instance_stats in stats_by_instance.items():
        stats_by_instance[k] = sorted(
            instance_stats, key=lambda i: i['start'])

    min_time = min(map(lambda stats: stats['pystart_ms'], res_list))
    max_time = max(map(lambda stats: stats['end'], res_list)) - min_time

    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    plt.rc('font', size=20)
    plt.rc('text.latex', preamble=r'\usepackage{libertine}')
    # Declaring a figure "gnt"
    fig, gnt = plt.subplots()
    plt.subplots_adjust(top=0.95, bottom=0.15, left=0.15, right=0.95)

    # gnt.set(title=f"Azure - {len(res_list)} requests")

    # Setting Y-axis limits
    gnt.set_ylim(0, len(res_list)*10)

    # Setting X-axis limits
    gnt.set_xlim(-10, max_time+100)

    # Setting labels for x-axis and y-axis
    gnt.set_xlabel('Time (ms)')
    gnt.set_ylabel('Function')

    # # Setting ticks on y-axis
    # gnt.set_yticks([15, 25, 35])
    # # Labelling tickes of y-axis
    # gnt.set_yticklabels(['1', '2', '3'])
    ticks = gnt.get_yticks()/10
    gnt.set_yticklabels(map(lambda x: int(x), ticks))

    # Setting graph attribute
    gnt.grid(True)

    invocation_i = 0
    col_iter = loop_list(COLORS)
    for instance_id, instance_stats in stats_by_instance.items():
        color = next(col_iter)
        for invocation_stats in instance_stats:
            point = 'yx'
            if invocation_stats['pystart_ms'] is min_time:
                point = 'rx'
            gnt.plot(invocation_stats['pystart_ms'] - min_time,
                     invocation_i + 5, point)
            gnt.plot(invocation_stats['pyend_ms'] - min_time,
                     invocation_i + 5, 'kx')
            gnt.broken_barh([(invocation_stats['start'] - min_time,
                              invocation_stats['duration'])],
                            (invocation_i, 9), facecolors=color)
            invocation_i = invocation_i + 10

    # plt.savefig(plot_file_name+".pdf", dpi=1000, format='pdf')
    plt.savefig(plot_file_name+".png", dpi=1000, format='png')
