
Setup instructions for a dedicated host (v6 node as a service)


Requirements: administrator user for the organization registered on the vantage6 server.


### v6-node service

Step 2: Create the New User
To create a new user named v6, use the useradd command followed by the -m option to create the home directory and the -s option to specify the shell. For example, if you want to use the Bash shell, you would use:

sudo useradd v6
This command creates a new user named v6 with a home directory located at /home/v6 and sets the default shell to Bash.

Step 3: Set the Home Directory
By default, the home directory for the new user is created under /home/v6. However, since you want the home directory to be located at /opt/v6, you'll need to move the existing home directory to the desired location and update the user's home directory path.

First, move the home directory:


sudo mkdir /opt/v6-nodes


sudo usermod -d /opt/v6 v6
Step 4: Set Ownership of the Home Directory
It's important to ensure that the new user owns the home directory. You can change the ownership of the /opt/v6 directory to the v6 user and group:

sudo chown -R v6:v6 /opt/v6

Set Permissions: Set the permissions of the /opt/v6 directory so that only the owner (user 'v6') can read, write, and execute files within it. This is done using the chmod command:
sudo chmod 700 /opt/v6-nodes


Step 5: Verify the Changes
To verify that the changes were successful, you can check the home directory of the v6 user:

id v6
This command should output information about the user v6, including the home directory, which should now be /opt/v6.


Set a password for the new user:
sudo passwd v6



Step 3: Add User to Docker Group
To add the user v6 to the Docker group, use the following command:

sudo usermod -aG docker v6
This command adds the user v6 to the Docker group, granting them access to Docker-related commands and resources.


Hello-world from the v6 user

v6@v6mdtaggregator:~$ docker run hello-world


### Creating a node for a collaboration

A node that will be part of a collaboration.That is to say, multiple organizations being part of a federation.
You will get an API key



### Creating a linux service


1. Create a Service File
First, you need to create a systemd service file. This file will define how your service should behave. You can create this file anywhere, but it's common to put it in /etc/systemd/system/. Let's name our service file agnode.service.

sudo nano /etc/systemd/system/agnode.service
2. Define the Service
In the service file, you'll define the service's behavior. Here's an example based on your requirements:

[Unit]
Description=vantage6 mdt aggregator node service
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
User=v6
WorkingDirectory=/opt/v6-nodes/agnode
Environment="PATH=/opt/v6-nodes/agnode/venv/bin"
ExecStart=/opt/v6-nodes/agnode/venv/bin/v6 node start --name agnode-config
ExecStop=/opt/v6-nodes/agnode/venv/bin/v6 node stop --name agnode-config

[Install]
WantedBy=multi-user.target

//running at boot
WantedBy=multi-user.target



Replace <your_username> with your actual username. This file tells systemd to run your service after the network is up (After=network.target), specifies the user under which the service should run (User=<your_username>), sets the working directory, defines the environment variables, and specifies the commands to start and stop the service.

3. Reload Systemd
After creating the service file, you need to reload systemd to make it aware of your new service.

sudo systemctl daemon-reload
4. Start the Service
Now, you can start your service using the following command:

sudo systemctl start agnode.service
5. Enable the Service
If you want your service to start automatically at boot, enable it:

sudo systemctl enable agnode.service
6. Check the Status
To check if your service is running, use:

sudo systemctl status agnode.service
7. Stop the Service
To stop your service, use:

sudo systemctl stop agnode.service

View Logs for a Specific Service: To view the logs for a specific service, use the -u option followed by the service name. For example, to view logs for a service named my-service, you would use:

sudo journalctl -u my-service



## v6 user

python -m venv venv

source venv/bin/activate

pip install vantage6

v6 node new --user



```
(venv) hcadavid@v6-aggregator:~/PROXMOX_node$ v6 node new
? Please enter a configuration-name: proxmox-agg-node
? Enter given api-key: 6e409f05-9cda-491a-a627-8abbc3a80dd8
? The base-URL of the server: https://v6-server.tail984a0.ts.net
? Enter port to which the server listens: 443
? Path of the api: /api
? Task directory path: /home/hcadavid/PROXMOX_node/tasks
? Do you want to add a database? No
? Which level of logging would you like? DEBUG
? Do you want to connect to a VPN server? No
? Do you want to add limit the algorithms allowed to run on your node? This should always be done for production scenarios. No
? Encryption is enabled for this collaboration. Accept? Yes
? Path to private key file:
[info ] - New configuration created: /home/hcadavid/.config/vantage6/node/proxmox-agg-node.yaml
[info ] - You can start the node by running v6 node start

```


```
(venv) hcadavid@v6-aggregator:~/PROXMOX_node$ v6 node create-private-key
? Select the configuration you want to use: proxmox-agg-node
[info ] - Connecting to server at 'https://v6-server.tail984a0.ts.net:443/api'
? Username: mdtadmin
? Password: *************
[info ] - Generating new private key
[warn ] - Private key written to '/home/hcadavid/.local/share/vantage6/InstanceType.NODE/privkey_MyDigiTwin-org.pem'
[warn ] - If you're running multiple nodes, be sure to copy the private key to the appropriate directories!
[info ] - Deriving public key
[info ] - Updating configuration
[info ] - Uploading public key to the server. This will overwrite any previously existing key!
[info ] - [Done]
```

v6-start

![alt text](image-1.png)



mkdir .config

v6 node create-private-key

v6 node

--configuration file
v6 node files

more /apt/v6-node/.config/vantage6/node/mdt-agg-node-config.yaml
nano /apt/v6-node/.config/vantage6/node/mdt-agg-node-config.yaml
cd /apt/v6-node/.local/share/vantage6/InstanceType.NODE/

Ensure the key is properly created

mv 'privkey_MyDigiTwin consortium.pem' privkey_MyDigiTwin_consortium.pem

nano /apt/v6-node/.config/vantage6/node/mdt-agg-node-config.yaml

ls /apt/v6-node/.local/share/vantage6/InstanceType.NODE/privkey_MyDigiTwin_consortium.pem

more /apt/v6-node/.local/share/vantage6/InstanceType.NODE/privkey_MyDigiTwin_consortium.pem

#create service
v6 node start




# New setup:

```
ls
ls -l
ls data
ls data/mdt-v6-aggregator-storage/
df
ls
docker
[200~# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update~
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
echo   "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" |   sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
traceroute
sudo apt install inetutils-traceroute
traceroute v6mdtserver.mydigitwin-umcu.src.surf-hosted.nl
curl v6mdtserver.mydigitwin-umcu.src.surf-hosted.nl
curl https://v6mdtserver.mydigitwin-umcu.src.surf-hosted.nl
ls
docker
sudo groupadd docker
sudo usermod -aG docker hcadavid
docker run hello-world
sudo docker run hello-world
mkdir collab_within_surf
cd collab_within_surf/
ls
python3 -m venv venv
sudo apt install python3.10-venv
python -m venv venv
source  venv/bin/activate
pip install vantage6
ls
v6 node list
exit
ls
cd collab_within_surf/
ls
source venv/bin/activate
v6 node list
ls
v6 node new
mkdir /home/hcadavid/.config
v6 node new
v6 node
v6 node create-private-key
cd /home/hcadavid/.local/share/vantage6/InstanceType.NODE/
ls
mv 'privkey_MyDigiTwin consortium.pem' privkey_MyDigiTwin_consortium.pem
ls
cd ~
ls
cd collab_within_surf/
ls
v6 node
v6 node fikes
v6 node files
nano /home/hcadavid/.config/vantage6/node/collab-within-surf-test.yaml
ls
v6 node
v6 node start
v6 node attach --name collab-within-surf-test
v6 node stop
ls
v6 node list
v6 node start
v6 node attach --name collab-within-surf-test
v6 node stop
ls
history
history | cut -c 8-
```