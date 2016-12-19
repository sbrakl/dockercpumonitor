import docker
import time
import utility
import logging


def main():
    logging.basicConfig(level=logging.INFO)
    logging.info('Main: started')

    cli = docker.DockerClient(base_url='unix://var/run/docker.sock')
    con = cli.containers.get('stress')

    cpuseries = []

    count = 0
    while (count < 9):
        time.sleep(2)
        cpu = utility.get_CPU_Percentage(con)
        logging.info('Currret CPU: %s' % cpu)

        cpuseries.append(cpu)

        if (len(cpuseries) > 5):
            cpuseries.pop(0)
        
        logging.debug(cpuseries)
        logging.debug('Mean: %s' % (sum(cpuseries)/len(cpuseries)))
        count += 1

    logging.info('Main: end')


if __name__ == '__main__':
    main()

