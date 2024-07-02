FROM ubuntu:latest

# Update and install required packages
RUN apt-get update && apt-get install -y openssh-client autossh python3 python3-pip net-tools inetutils-ping ncat


# Copy SSH key. Ensure your SSH key is named `id_rsa`
#COPY id_rsa /root/.ssh/id_rsa

# Setting permissions for SSH key
#RUN chmod 600 /root/.ssh/id_rsa && \
#    echo "Host *\n\tStrictHostKeyChecking no\n\tUserKnownHostsFile=/dev/null" > /root/.ssh/config

# Copy your SSH config file
#COPY ssh_config /root/.ssh/config

# Install Python dependencies

RUN mkdir -p /etc/pip \
    && echo "[global]" > /etc/pip.conf \
    && echo "trusted-host = pypi.python.org" >> /etc/pip.conf \
    && echo "               pypi.org" >> /etc/pip.conf \
    && echo "               files.pythonhosted.org" >> /etc/pip.conf \
    && echo "               github.com" >> /etc/pip.conf \
    && echo "               codeload.github.com" >> /etc/pip.conf


RUN pip3 install paramiko --break-system-packages

# Copy the Python script that sets up SSH tunnels
COPY setup_tunnels.py /setup_tunnels.py

# Set the command to execute the Python script
CMD ["python3", "/setup_tunnels.py"]
