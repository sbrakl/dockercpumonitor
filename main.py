import docker
import time
import utility
import clientConn
import logging
import datetime

def main():
    composeFolder = 'compose'
    containerToMonitor = 'stress'
    composePattern = composeFolder + '_' + containerToMonitor
    #containerToMonitor = 'ndsapprelease0858_ndspublicengagement-esb--release_1'

    logging.basicConfig(level=logging.INFO)
    logging.info('Main: started')

    cli = clientConn.GetDockerClient('local')
    #
    # try:
    #     con = cli.containers.get(containerToMonitor)
    # except Exception as e:
    #     logging.warning('Cant find "%s" container running' % containerToMonitor)
    #     logging.error(e)
    #     exit()

    # Initialize loop variables

    cons = utility.getContainerInComposeMode(composePattern, 'local')
    containerCount = len(cons)

    if containerCount < 1:
        logging.error('No containers found with pattern "%s"' % containerToMonitor)
        exit()
    else:
        firstCon = cons[0]
        con = cli.containers.get(firstCon)


    cpuseries = [0.,0.,0.,0.,0.]

    count = 0
    end_Cool_time = None

    while (count < 30):

        time.sleep(2)

        try:
            cpu = utility.get_CPU_Percentage(con)
        except:
            cpu = 0.

        meanCPU = utility.handleCPUSeries(cpuseries, cpu)


        end_Cool_time, containerCount = utility.ScaleContaienr(meanCPU, end_Cool_time, containerCount, containerToMonitor)

        count += 1


    logging.info('Main: end')


if __name__ == '__main__':
    main()

