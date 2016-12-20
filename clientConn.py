import docker
import logging

def GetDockerClient(env):
    cli = None

    if (env == 'local'):
        cli = docker.DockerClient(base_url='unix://var/run/docker.sock',
                                  version='1.22')
    elif (env == 'swarm'):
        tls_config = docker.tls.TLSConfig(
            ca_cert='/home/azureuser/ca.pem',
            client_cert=('/home/azureuser/cert.pem', '/home/azureuser/key.pem'),
            verify=True
        )
        cli = docker.DockerClient(base_url='https://ape-swarm-manager:3376',
                                  tls=tls_config,
                                  version='1.23')
    return  cli


def TestDockerClient(env):
    cli = GetDockerClient(env)

    conlist = cli.containers.list()
    logging.info('List of container running')
    for con in conlist:
        logging.info(con.name)

    logging.info('Docker info')
    logging.info(cli.info())