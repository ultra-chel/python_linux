import sys
from datetime import datetime


def get_report():
    from subprocess import run, PIPE
    from operator import itemgetter

    res = run(['ps', 'aux'], stdout=PIPE)
    procs = res.stdout.decode().split('\n')
    titles = procs[0].split()

    used_cpu = []
    used_mem = []
    max_cpu = 0
    max_mem = 0
    max_cpu_proc = ''
    max_mem_proc = ''
    user_list = []

    for p in procs[1:]:
        if not p == '':
            chunks = p.split(maxsplit=len(titles) - 1)
            user_list.append(chunks[titles.index('USER')])
            proc_cpu = float(chunks[titles.index('%CPU')])
            used_cpu.append(proc_cpu)
            proc_mem = float(chunks[titles.index('%MEM')])
            used_mem.append(proc_mem)
            if proc_cpu >= max_cpu:
                max_cpu = proc_cpu
                max_cpu_proc = chunks[titles.index('COMMAND')]
            if proc_mem >= max_mem:
                max_mem = proc_mem
                max_mem_proc = chunks[titles.index('COMMAND')]

    unique_users = set(user_list)
    result = {i: user_list.count(i) for i in user_list}
    sorted_result = dict(sorted(result.items(), key=itemgetter(1), reverse=True))

    print(f'Отчет о состоянии системы:')
    print(f'\nПользователи системы: ', end=' ')
    for x in unique_users:
        print(x + ',', end=' ')
    print(f'\n\nПроцессов запущено: {len(procs)}')
    print(f'\nПользовательских процессов:')
    for key, value in sorted_result.items():
        print(key, ":", value)
    print(f'\nВсего памяти используется: {float("{0:.1f}".format(sum(used_mem)))} %')
    print(f'\nВсего CPU используется: {float("{0:.1f}".format(sum(used_cpu)))} %')
    print(f'\nБольше всего CPU использует: {max_cpu_proc[0: 20]} ({max_cpu} %)')
    print(f'\nБольше всего памяти использует: {max_mem_proc[0: 20]} ({max_mem} %) \n')

    out = sys.stdout
    date_time = datetime.now()
    str_date_time = date_time.strftime("%d-%m-%Y-%H:%M")
    with open(str_date_time + '-report.txt', 'w') as f:
        sys.stdout = f
        print(f'Отчет о состоянии системы:')
        print(f'\nПользователи системы: ', end=' ')
        for x in unique_users:
            print(x + ',', end=' ')
        print(f'\n\nПроцессов запущено: {len(procs)}')
        print(f'\nПользовательских процессов:')
        for key, value in sorted_result.items():
            print(key, ":", value)
        print(f'\nВсего памяти используется: {float("{0:.1f}".format(sum(used_mem)))} %')
        print(f'\nВсего CPU используется: {float("{0:.1f}".format(sum(used_cpu)))} %')
        print(f'\nБольше всего CPU использует: {max_cpu_proc[0: 20]} ({max_cpu} %)')
        print(f'\nБольше всего памяти использует: {max_mem_proc[0: 20]} ({max_mem} %) \n')
    sys.stdout = out


if __name__ == '__main__':
    get_report()
