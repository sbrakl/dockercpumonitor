import docker

tls_config = docker.tls.TLSConfig(
  ca_cert='/home/azureuser/ca.pem', 
  client_cert=('/home/azureuser/cert.pem', '/home/azureuser/key.pem'), 
  verify=True
)
client = docker.DockerClient(base_url='https://ape-swarm-manager:3376',
	tls=tls_config)
#client = docker.DockerClient(base_url='127.0.0.1:3376', 
#	tls=tls_config)
print(client.info())
