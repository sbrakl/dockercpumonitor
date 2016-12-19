import logging
import random

def get_CPU_Percentage(con):

    conName = con.name
    cpupercentage = 0.0

    # Get CPU Usage in percentage
    constat = con.stats(stream=False)
    prestats = constat['precpu_stats']
    cpustats = constat['cpu_stats']
    #print(cpustats)

    #cpuDelta = res.cpu_stats.cpu_usage.total_usage -  res.precpu_stats.cpu_usage.total_usage;
    #systemDelta = res.cpu_stats.system_cpu_usage - res.precpu_stats.system_cpu_usage;
    #var RESULT_CPU_USAGE = cpuDelta / systemDelta * 100;
    #CPUStats.CPUUsage.PercpuUsage


    prestats_totalusage = prestats['cpu_usage']['total_usage']
    stats_totalusage = cpustats['cpu_usage']['total_usage']
    numOfCPUCore = len(cpustats['cpu_usage']['percpu_usage'])
    logging.debug('prestats_totalusage: %s, stats_totalusage: %s, NoOfCore: %s' % (prestats_totalusage, stats_totalusage, numOfCPUCore))

    prestats_syscpu = prestats['system_cpu_usage']
    stats_syscpu = cpustats['system_cpu_usage']
    logging.debug('prestats_syscpu: %s, stats_syscpu: %s' % (prestats_syscpu, stats_syscpu))

    cpuDelta = stats_totalusage - prestats_totalusage
    systemDelta = stats_syscpu - prestats_syscpu

    if cpuDelta > 0 and systemDelta > 0:
        cpupercentage = (cpuDelta / systemDelta) * numOfCPUCore

    formattedcpupert = '{:.1%}'.format(cpupercentage)
    logging.debug('cpuDelta: %s, systemDelta: %s, cpu: %s' % (cpuDelta, systemDelta, cpupercentage))

    print('"%s" Container CPU: %s ' % (conName, formattedcpupert))

    return cpupercentage


def fake_get_CPU_Percentage(con):    
    return random.uniform(0,100)
