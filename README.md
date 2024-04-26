




Create an admin user


## v6 user

python -m venv venv

source venv/bin/activate

pip install vantage6

v6 node new --user

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
