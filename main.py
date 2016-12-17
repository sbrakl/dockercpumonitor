import docker
import time
import utility
import logging


def main():
    logging.basicConfig(level=logging.INFO)
    logging.info('Main: started')

    cli = docker.DockerClient(base_url='unix://var/run/docker.sock')
    con = cli.containers.get('stress')

    count = 0
    while (count < 9):
        utility.get_CPU_Percentage(con)
        time.sleep(2)
        count += 1

    logging.info('Main: end')


if __name__ == '__main__':
    main()

