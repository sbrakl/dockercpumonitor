import clientConn
import logging
import random
import datetime
import re
import os


def get_CPU_Percentage(con):
    conName = con.name
    cpupercentage = 0.0

    # Check if the container is running
    if (con.status != 'running'):
        raise ValueError('"%s" container is not running' % conName)

    # Get CPU Usage in percentage
    constat = con.stats(stream=False)
    prestats = constat['precpu_stats']
    cpustats = constat['cpu_stats']
    # print(cpustats)

    # cpuDelta = res.cpu_stats.cpu_usage.total_usage -  res.precpu_stats.cpu_usage.total_usage;
    # systemDelta = res.cpu_stats.system_cpu_usage - res.precpu_stats.system_cpu_usage;
    # var RESULT_CPU_USAGE = cpuDelta / systemDelta * 100;
    # CPUStats.CPUUsage.PercpuUsage


    prestats_totalusage = prestats['cpu_usage']['total_usage']
    stats_totalusage = cpustats['cpu_usage']['total_usage']
    numOfCPUCore = len(cpustats['cpu_usage']['percpu_usage'])
    logging.debug('prestats_totalusage: %s, stats_totalusage: %s, NoOfCore: %s' % (
    prestats_totalusage, stats_totalusage, numOfCPUCore))

    prestats_syscpu = prestats['system_cpu_usage']
    stats_syscpu = cpustats['system_cpu_usage']
    logging.debug('prestats_syscpu: %s, stats_syscpu: %s' % (prestats_syscpu, stats_syscpu))

    cpuDelta = stats_totalusage - prestats_totalusage
    systemDelta = stats_syscpu - prestats_syscpu

    if cpuDelta > 0 and systemDelta > 0:
        cpupercentage = (cpuDelta / systemDelta) * numOfCPUCore

    formattedcpupert = '{:.1%}'.format(cpupercentage)
    logging.debug('cpuDelta: %s, systemDelta: %s, cpu: %s' % (cpuDelta, systemDelta, cpupercentage))

    logging.info('"%s" Container CPU: %s ' % (conName, formattedcpupert))

    return (cpupercentage * 100)


def fake_get_CPU_Percentage(con):
    return random.uniform(0, 100)


def ScaleContaienr(meanCPU, end_Cool_time, containerCount, containerName):
    coolPeriod = 30

    curr_time = datetime.datetime.now()

    if (end_Cool_time and (curr_time < end_Cool_time)):
        # Means, cooling time if on, don't do anything
        logging.info('No scaling action, Cooling period going on...')
    else:
        if (meanCPU > 50):
            containerCount += 1
            print('Scaling Container UP to %s' % containerCount)
            compose_cmd  = "docker-compose scale " + containerName + "=" + str(containerCount)
            compose_scale_call(compose_cmd)
            end_Cool_time = curr_time + datetime.timedelta(seconds=coolPeriod)
        elif (meanCPU < 50 and containerCount > 1):
            containerCount -= 1
            end_Cool_time = curr_time + datetime.timedelta(seconds=coolPeriod)
            print('Scaling down containers to %s' % containerCount)
            compose_cmd  = "docker-compose scale " + containerName + "=" + str(containerCount)
            compose_scale_call(compose_cmd)
        elif (meanCPU < 50):
            logging.info('Idle CPU, no action')

    return end_Cool_time, containerCount


def compose_scale_call(compose_cmd):
    os.chdir('/home/sbrakl/dockercpumonitor/compose')
    os.system(compose_cmd)


def handleCPUSeries(cpuseries, cpu):
    logging.debug('Currret CPU: %s' % cpu)

    cpuseries.append(cpu)

    if (len(cpuseries) > 5):
        cpuseries.pop(0)

    logging.debug(cpuseries)
    meanCPU = (sum(cpuseries) / len(cpuseries))
    logging.info('Mean CPU: %s' % meanCPU)
    return meanCPU


def getContainerInComposeMode(con_name_pattern, env):
    listOfSameContainerInCompose = []

    regexptn = "^" + con_name_pattern + "_";
    pattern = re.compile(regexptn)

    cli = clientConn.GetDockerClient(env)

    for con in cli.containers.list():
        conname = con.name
        if (pattern.match(conname)):
            listOfSameContainerInCompose.append(conname)

    return listOfSameContainerInCompose
