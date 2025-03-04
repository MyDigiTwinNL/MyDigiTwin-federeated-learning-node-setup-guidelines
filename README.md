
# Guidelines for setting up a vantage6 node as a Linux systemd service


Requirements: 

 - A linux user with sudo privileges
 - Information provided by the vantage6 server admin:
	 - 	Server URL
	 -  API key
	 -  User name and password of the vantage6 server's organization admin

# 1. Installing docker

Refer to [official documentation](https://docs.docker.com/engine/install/ubuntu/)


# 2. Creating an user for the service

### Create a user for the service

Create a regular user (no sudo privileges)

```
sudo useradd v6
```

### Create a home directory for the service

Create a folder on /opt/ as the home directory of the service-related user, and ensure that only the 'v6' user can access it:


```
sudo mkdir /opt/v6-nodes
sudo usermod --home /opt/v6-nodes --shell /bin/bash v6
sudo chown -R v6:v6 /opt/v6-nodes
# Set the permissions of the /opt/v6 directory so that only the owner (user 'v6') can read, write, and execute files within it
sudo chmod 700 /opt/v6-nodes
```

### Set user password

Set a strong password for the v6 user:

```
sudo passwd v6
```

### Verify that the user was properly configured

This command should output information about the user v6, including the home directory, which should now be /opt/v6-nodes.

```
id v6
```

### Add the new user to the Docker Group

This is needed as the service will lauch the docker daemon as the 'v6' user. To add the user v6 to the Docker group, use the following command:

```
sudo usermod -aG docker v6
```

Logout and login again as v6 before continuing, so that the user's group rights are reloaded.

### Check that the v6 user can execute docker commands

Hello-world from the v6 user

```
v6@node:~$ docker run hello-world
```

# 3. Creating a node for a collaboration

### Login as the new v6 user

```
su v6
```

### Create a folder for the service software and data

The following steps assume that the service will be called **'node_alpha'**. You can change it to one that suits your setup. These steps also require an API key, the vantage6 server URL, and the credentials of a vantage6 user with organization management privileges.

### Install vantage6 on the service home folder.

Create a folder for the node configurations (.config):

```
mkdir $HOME/.config
```

And one for each node environment/data within the v6's user home folder (opt/v6-nodes):

```
mkdir $HOME/node_alpha
mkdir $HOME/node_alpha/data
```

Get the test dataset included in this repository on the 'data' folder previously created:

```
curl https://raw.githubusercontent.com/MyDigiTwinNL/MyDigiTwin-federeated-learning-node-setup-guidelines/main/dummy-data/testdata.csv?token=GHSAT0AAAAAACPNM3N7V5FWFW5SZVLDWTHQZTHBASA -o $HOME/node_alpha/data/testdata.csv
```

Install vantage6 dependencies. This setup has been tested with vantage6 4.5.3 node/server

```
cd $HOME/node_alpha
python -m venv venv
source venv/bin/activate
pip install vantage6==4.5.3
```

Create a new node using the `v6 node` command. Make sure it is created at a user level:

```
v6 node new --user
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

Set the node's encryption key. When running the following command, you will be asked for the organization's manager user name and password:

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

## Setting up a systemd service for the vantage6 node

**Login again as an user with sudo privileges**

### Creating a Service File

Create a systemd service file that defines how the should behave. On an ubuntu server, it is on the /etc/systemd/system/ folder. In this case we will call the service file 'node_alpha.service'.

```
sudo nano /etc/systemd/system/node_alpha.service
```

For the file content, make sure that as a value for the `--name` flag of ExecStart and ExecStop you are using the configuration name you gave when you executed the `v6 node new` command (`? Please enter a configuration-name: `). Also make sure you use the right folder paths:

```
[Unit]
Description=vantage6 node service
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
User=v6
WorkingDirectory=/opt/v6-nodes/node_alpha
Environment="PATH=/opt/v6-nodes/node_alpha/venv/bin"
ExecStart=/opt/v6-nodes/node_alpha/venv/bin/v6 node start --name node_alpha
ExecStop=/opt/v6-nodes/node_alpha/venv/bin/v6 node stop --name node_alpha

[Install]
WantedBy=multi-user.target
```

### Reloading Systemd
After creating the service file, you need to reload systemd to make it aware of your new service.

```
sudo systemctl daemon-reload
```

### Starting the Service
Now, you can start your service using the following command:

```
sudo systemctl start node_alpha.service
```

### Checking the status of the service

To view the status of the service, you can use journalctl:

```
sudo journalctl -u node_alpha.service
```

### Checking the node status

As the vantage6 node runs within a Docker container, it is important to also check the logs within it. One option is to install and run [lazydocker](https://github.com/jesseduffield/lazydocker), to see which containers are running once the service has started:

![alt text](img/lazydocker.png)

Alternatively, you can login to as the v6 user, and use the 'attach' command to check the logs:

```
/opt/v6-nodes/node_alpha/venv/bin/v6 node attach --name node_alpha
```


### Enabling the Service

Once you have configured the systemd service, make sure it will start automatically at boot:

```
sudo systemctl enable node_alpha.service
```

# Administrative tasks - [Updating node settings](#update_settings)

To make changes on your node(s) do the following:

### 1. Stop the vantage6 node service

With a user with 'sudoer' privileges (replace `node_alpha` with the service name created through the previous steps):

```
sudo systemctl stop node_alpha.service
```

### 2. Edit the node configuration 

Log in as the v6 user

#### 2.1 (Optional) Locate the node configuration file

If the node was set up as described in the previous steps, the configuration file should be located at `/opt/v6-nodes/.config/vantage6/node/`. For example, if the configuration name given in Step 3 was used (node-alpha), the file to be edited would be `/opt/v6-nodes/.config/vantage6/node/node-alpha-config.yaml`.

You can also use the `v6 node files` command to get the absolute path of the configuration file:

```
cd $HOME/node_alpha
source venv/bin/activate
v6 node files
```

#### 2.2 Edit the corresponding file. 

Update the settings as decribed by v6's [node administration documentation](https://docs.vantage6.ai/en/version-4.0.0/node/configure.html#all-configuration-options). Some important settings include:


- The datasources the node is getting access to, for example:

  ```yaml
  # path or endpoint to the local data source. The client can request a
  # certain database by using its label. The type is used by the
  # auto_wrapper method used by algorithms. This way the algorithm wrapper
  # knows how to read the data from the source. The auto_wrapper currently
  # supports: 'csv', 'parquet', 'sql', 'sparql', 'excel', 'omop'. If your
  # algorithm does not use the wrapper and you have a different type of
  # data source you can specify 'other'.
  databases:
    - label: lifelines
      uri: /data/location/lifelines_fhirdb.db.sqlite
      type: sql
  ```

- The policies on which algorithms are allowed to run -and hence to get access to data- on this node. The following configuration will restrict the node to only execute the [FedAvg](https://github.com/MyDigiTwinNL/FedAvg_vantage6) algorithm, with a SHA-256 hash as a tag:

  ```yaml
  # Define who is allowed to run which algorithms on this node.
  policies:
    # Control which algorithm images are allowed to run on this node. This is
    # expected to be a valid regular expression.
    allowed_algorithms:
      - ^ghcr\.io\/mydigitwinnl\/federated_cvdm_training_poc:[0-9a-f]{64}$

  ```
  Restrict the node to only execute the [FedAvg](https://github.com/MyDigiTwinNL/FedAvg_vantage6) algorithm image, with a **specific** SHA-256 hash as a tag:

  ```yaml
  # Define who is allowed to run which algorithms on this node.
  policies:
    # Control which algorithm images are allowed to run on this node. This is
    # expected to be a valid regular expression.
    allowed_algorithms:
      - ^ghcr\.io\/mydigitwinnl\/federated_cvdm_training_poc:82b6390525e5690a56c1ddde3dd2a2eb2d98b1c8$

  ```

  Restrict the node to only execute the [FedAvg](https://github.com/MyDigiTwinNL/FedAvg_vantage6) algorithm image, with any tag:

  ```yaml
  # Define who is allowed to run which algorithms on this node.
  policies:
    # Control which algorithm images are allowed to run on this node. This is
    # expected to be a valid regular expression.
    allowed_algorithms:
      - ^ghcr\.io\/mydigitwinnl\/federated_cvdm_training_poc:[a-zA-Z0-9_.-]{1,128}$
  ```

  ## Node admins:
  Please refer to the [reviewewing algorithms section](reviewing_v6_algorithms.md) for more information on what to consider when reviewing an algorithm before 'whitelisting' it.


### 2.3. Restart the vantage6 node service

With a user with 'sudoer' privileges (replace `node_alpha` with the service name created through the previous steps):

```
sudo systemctl start node_alpha.service
```




# Administrative tasks - [Updating vantage6 node version](#updating_v6_version)

When the collaboration's central server is updated to a new vantage6 version, e.g., due to the need for a recently introduced feature, in some cases the nodes need to be updated as well. The following are the steps to update the node's underlying v6 version to verion X.Y.Z.

### 1. Stop the vantage6 node service

With a user with 'sudoer' privileges (replace `node_alpha` with the service name created through the previous steps):

```
sudo systemctl stop node_alpha.service
```

Note: if you are not sure about the service name, you can list the existing ones:

```
sudo systemctl list-unit-files --type=service
```

### 2. Update the vantage6 packages used by the systemd service

Login with the v6 user, go to the node's folder (e.g., `$HOME/node_alpha`), and update the vantage6 packages (replace X.Y.Z with the version you want to update to):

```
cd $HOME/node_alpha
source venv/bin/activate
pip install --upgrade vantage6==X.Y.Z
```
<!--
### 3. **(Only if needed)** Update the API key and regenerate the encryption key

In some cases the v6-server's admin need to regenerate the node-API keys after updating the server. If a new API key is given to you, edit the node's configuration file and update the `api_key` field accordingly. 

If you are not sure about the location of your node's configuration file, use the following command (as the v6 user):

```
v6 node files
```

In case the encryption key is also needed to be regenerated, use the same command from previous steps:

```
v6 node create-private-key -n node_alpha --overwrite

```
-->

### 3. Restart the service

With the user with 'sudoer' privileges:

```
sudo systemctl start node_alpha.service
```




