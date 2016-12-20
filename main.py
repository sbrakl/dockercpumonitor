import docker
import time
import utility
import clientConn
import logging
import os


def main():
    containerToMonitor = 'stress'
    #containerToMonitor = 'ndsapprelease0858_ndspublicengagement-esb--release_1'


    logging.basicConfig(level=logging.INFO)
    logging.info('Main: started')

    cli = clientConn.GetDockerClient('local')

    try:
        con = cli.containers.get(containerToMonitor)
    except Exception as e:
        logging.warning('Cant find "%s" container running' % containerToMonitor)
        logging.error(e)
        exit()

    cpuseries = [0.,0.,0.,0.,0.]

    count = 0
    while (count < 9):
        time.sleep(2)

        try:
            cpu = utility.get_CPU_Percentage(con)
        except:
            cpu = 0.

        logging.debug('Currret CPU: %s' % cpu)

        cpuseries.append(cpu)

        if (len(cpuseries) > 5):
            cpuseries.pop(0)
        
        logging.debug(cpuseries)
        meanCPU = (sum(cpuseries)/len(cpuseries))
        logging.info('Mean CPU: %s' % meanCPU)
        count += 1

        containCount = 1
        if (meanCPU > 50):
            os.system('echo "Scale container up"')
            containCount += 1
            print('Wating for couple of minutes to container to start')
            time.sleep(30)
        elif (meanCPU < 50 and containCount > 1):
            os.system('echo "Scale container down"')
            containCount -= 1
        elif (meanCPU < 50):
            print('Idle CPU, no action')


    logging.info('Main: end')


if __name__ == '__main__':
    main()

