import os
from paramiko import SSHConfig
import time
import subprocess

def parse_ssh_config(config_path):
    with open(config_path) as f:
        config = SSHConfig()
        config.parse(f)
        return config

def establish_ssh_tunnels(ssh_config):
    tunnel_processes = []
    for host in ssh_config.get_hostnames():
        if host != "*":
            config = ssh_config.lookup(host)
            user = config.get('user')
            hostname = config.get('hostname')
            local_forwards = config.get('localforward', [])

            for forward in local_forwards:
                local_port, remote = forward.split()
                remote_host, remote_port = remote.split(':')
                
                autossh_command = [
                    'autossh', '-f', '-N', '-M', '0',
                    f'{user}@{hostname}',
                    '-L', f'{local_port}:localhost:{remote_port}',
                    '-o', 'ExitOnForwardFailure yes',
                    '-o', 'ServerAliveInterval=30',
                    '-o', 'ServerAliveCountMax=3',
                    '-o', 'StrictHostKeyChecking=no'
                ]
                
                print(f'Starting tunnel from localhost:{local_port} to {remote_host}:{remote_port}')
                process = subprocess.Popen(autossh_command)
                tunnel_processes.append((process, autossh_command))
    return tunnel_processes

def monitor_and_maintain_tunnels(tunnel_processes):
    try:
        while True:
            for i, (process, command) in enumerate(tunnel_processes):
                if process.poll() is not None:  # Process has terminated
                    print(f"Tunnel {command} has stopped. Restarting...")
                    new_process = subprocess.Popen(command)
                    tunnel_processes[i] = (new_process, command)  # Replace the old process with the new one
            time.sleep(10)  # Check every 10 seconds
    except KeyboardInterrupt:
        print("Stopping SSH tunnel manager.")
        

if __name__ == '__main__':
    config_file = '/root/.ssh/config'
    # check if file exists, if not, exit.
    if not os.path.isfile(config_file):
        print(f'Config file {config_file} does not exist.')
        exit(1)
        
    config = parse_ssh_config(config_file)
    tunnel_processes = establish_ssh_tunnels(config)
    monitor_and_maintain_tunnels(tunnel_processes)
