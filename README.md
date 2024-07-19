# ssh-tunnel-docker-image
A docker image could setup multiple ssh tunnels and SSH port forwarding.

## Get started
docker run -d --name ssh_multi_tunnel_container   -v ./.ssh/config:/root/.ssh/config   -v ./.ssh/id_rsa:/root/.ssh/id_rsa   -p 8002:8001   magiccpp1/ssh-multi-tunnel
