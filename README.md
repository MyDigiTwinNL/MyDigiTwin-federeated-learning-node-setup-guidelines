
# Setup instructions for a dedicated host (v6 node as a service)


Requirements: administrator user for the organization registered on the vantage6 server.

# Install docker

Refer to [official documentation](https://docs.docker.com/engine/install/ubuntu/)


# Creating application-level user

### 1. Create the New User

To create a new user named v6, use the useradd command followed by the -m option to create the home directory and the -s option to specify the shell. For example, if you want to use the Bash shell, you would use:

```
sudo useradd v6
```

This command creates a new user named v6 with a home directory located at /home/v6 and sets the default shell to Bash.

### 2. Set the home directory

By default, the home directory for the new user is created under /home/v6. However, since you want the home directory to be located at /opt/v6, you'll need to move the existing home directory to the desired location and update the user's home directory path. Set Ownership of the Home Directory
It's important to ensure that the new user owns the home directory. Set the permissions of the /opt/v6 directory so that only the owner (user 'v6') can read, write, and execute files within it. 


```
sudo mkdir /opt/v6-nodes
sudo usermod --home /opt/v6-nodes --shell /bin/bash v6
sudo chown -R v6:v6 /opt/v6-nodes
# Set the permissions of the /opt/v6 directory so that only the owner (user 'v6') can read, write, and execute files within it
sudo chmod 700 /opt/v6-nodes
```

### 3. Set user password

Set a strong password for the v6 user:
```
sudo passwd v6
```

### 4. Verify user 

This command should output information about the user v6, including the home directory, which should now be /opt/v6.

```
id v6
```

### 5. Add User to Docker Group

To add the user v6 to the Docker group, use the following command:

```
sudo usermod -aG docker v6
```

(logout and login again as v6 before continuing)
This command adds the user v6 to the Docker group, granting them access to Docker-related commands and resources.

### 6. Check that the v6 user can execute docker commands

Hello-world from the v6 user

```
v6@node:~$ docker run hello-world
```

# Creating a node for a collaboration

Login as V6 user. Let's assume the node will be called: node_alpha

A node that will be part of a collaboration.That is to say, multiple organizations being part of a federation. You will get an API key and a server URL.


## Install vantage6 on the V6's user home folder.

Create a folder for the node within the v6's user home folder (opt/v6-nodes)

```
mkdir $HOME/node_alpha
mkdir $HOME/node_alpha/data
```

Get test dataset

```
curl https://raw.githubusercontent.com/MyDigiTwinNL/MyDigiTwin-federeated-learning-node-setup-guidelines/main/dummy-data/testdata.csv?token=GHSAT0AAAAAACPNM3N7V5FWFW5SZVLDWTHQZTHBASA -o $HOME/node_alpha/data/testdata.csv
```


Install vantage6 dependencies. This is tested with vantage6 4.4.1 node/server

```
cd $HOME/node_alpha
python -m venv venv
source venv/bin/activate
pip install vantage6=4.4.1
```

Create a new node using the `v6 node` command. Make sure it is created at a user level:

```
v6 node new --user
```

```
mkdir $HOME/.config
mkdir $HOME/node_alpha
mkdir $HOME/node_alpha/data
```


Enter:

```
(venv) v6@node:~/$ v6 node new --user
? Please enter a configuration-name: node_alpha
? Enter given api-key: ENTER_THE_GIVEN_KEY
? The base-URL of the server: ENTER_THE_GIVEN_URL
? Enter port to which the server listens: 443
? Path of the api: /api
? Task directory path: (*USE THE DEFAULT VALUE) /opt/v6-nodes/.local/share/vantage6/node/node_alpha-config
? Do you want to add a database? No *(IT WILL BE ADDED LATER)
? Which level of logging would you like? DEBUG
? Do you want to connect to a VPN server? No
? Do you want to add limit the algorithms allowed to run on your node? No (*THIS WILL UPDATED LATER)
? Encryption is enabled for this collaboration. Accept? Yes
? Path to private key file: * JUST PRESS ENTER (the key will be added later)
[info ] - New configuration created: /opt/v6-nodes/.config/vantage6/node/node_alpha-config.yaml
[info ] - You can start the node by running v6 node start (*Do not start the node yet!)

```

Edit the generated YAML configuration file, and add an entry to the `databases` section so it includes the csv previously downloaded on `/opt/v6-nodes/data` as the 'testdata' database:

```
api_key: THE_GIVEN_API_KEY
api_path: /api
databases:
- label: testdata
  type: csv
  uri: /opt/v6-nodes/node_alpha/data/testdata.csv
 
...
```

Set the node's encryption key. Use one of your server users with 'Organization Admin' privileges.

```
v6 node create-private-key -n node_alpha
```

Expected output:

```

? Username: orgadmin
? Password: ******
[info ] - Generating new private key
[warn ] - Private key written to '/opt/v6-nodes/.local/share/vantage6/InstanceType.NODE/privkey_organization_name.pem'
[warn ] - If you're running multiple nodes, be sure to copy the private key to the appropriate directories!
[info ] - Deriving public key
[info ] - Updating configuration
[info ] - Uploading public key to the server. This will overwrite any previously existing key!
[info ] - [Done]
```

The configuration file (/opt/v6-nodes/.config/vantage6/node/node_alpha-config.yaml) now should have a private key used for data encryption:

```
...
encryption:
  enabled: true
  private_key: /opt/v6-nodes/.local/share/vantage6/InstanceType.NODE/privkey_organization_name.pem
  ...
```

Run the node manually, and check that it doesn't report errors:

```
v6 node start -n node_alpha --attach
```

![alt text](img/node-run-p1.png)
![alt text](img/node-run-p2.png)


Exit the attached node's log (Ctrl-C) and shut down the node:

```
v6 node stop -n node_alpha 
```

## Setup a systemd service for a node



### 1. Create a Service File

As an user within the sudoer group:

You need to create a systemd service file that defines how your service should behave. In ubuntu server, it is on the /etc/systemd/system/ folder. Let's name our service file node_alpha.service.


```
sudo nano /etc/systemd/system/node_alpha.service
```

2. Define the Service
In the service file, you'll define the service's behavior. Here's an example based on your requirements. For name use `? Please enter a configuration-name: `

```
[Unit]
Description=vantage6 node service
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
User=v6
WorkingDirectory=/opt/v6-nodes/alpha-node
Environment="PATH=/opt/v6-nodes/alpha-node/venv/bin"
ExecStart=/opt/v6-nodes/node-alpha/venv/bin/v6 node start --name node_alpha
ExecStop=/opt/v6-nodes/node-alpha/venv/bin/v6 node stop --name node_alpha

[Install]
WantedBy=multi-user.target
```

## Reload Systemd
After creating the service file, you need to reload systemd to make it aware of your new service.

```
sudo systemctl daemon-reload
```

## Start the Service
Now, you can start your service using the following command:

```
sudo systemctl start node_alpha.service
```

5. Enable the Service
To ensure the service with start automatically at boot, enable it:

```
sudo systemctl enable node_alpha.service
```

Check its status

```
sudo systemctl status agnode.service
```

To view the logs, you can use journalctl:

```
sudo journalctl -u my-service
```

or attach to the v6 node's logs:

```
v6 node attach
```


# Update node version

