import docker
import time
import utility
import logging


def main():
    logging.basicConfig(level=logging.INFO)
    logging.info('Main: started')

    #cli = docker.DockerClient(base_url='unix://var/run/docker.sock')
    tls_config = docker.tls.TLSConfig(
        ca_cert='/home/azureuser/ca.pem',
  	client_cert=('/home/azureuser/cert.pem', '/home/azureuser/key.pem'),
  	verify=True
    )
    cli = docker.DockerClient(base_url='https://ape-swarm-manager:3376',
           tls=tls_config,
	   version='1.23') 
   
    '''
    conlist = cli.containers.list()

    for con in conlist:
        print(con.name)
    '''

    con = cli.containers.get('ndsapprelease0858_ndspublicengagement-esb--release_1')

    cpuseries = [0.,0.,0.,0.,0.]

    count = 0
    while (count < 9):
        time.sleep(2)
        cpu = utility.get_CPU_Percentage(con)
        logging.info('Currret CPU: %s' % cpu)

        cpuseries.append(cpu)

        if (len(cpuseries) > 5):
            cpuseries.pop(0)
        
        logging.debug(cpuseries)
        logging.info('Mean: %s' % (sum(cpuseries)/len(cpuseries)))
        count += 1

    logging.info('Main: end')


if __name__ == '__main__':
    main()

