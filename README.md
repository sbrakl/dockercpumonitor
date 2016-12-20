# dockercpumonitor
Python script to monitor the docker container CPU

It's just a Proof of concept done for auto scaling container based on the CPU utilization

It design for local as well as Swarm 1.2.5 on docker v1.11

main.py is the primary file where entire logic is written

If you running docker on TLS, you need to modify clientConn.py to specify the client certificates

It uses Docker.stat API to get the container CPU utilization and scale up or down based on the CPU used

You can extent to do crazy stuff like spawn new box with docker-machine, make it join the swarm and make it work


