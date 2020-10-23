![](https://raw.githubusercontent.com/linuxserver/docker-templates/master/linuxserver.io/img/linuxserver_small.png)

# How to use these Reverse Proxy Configs

This folder contains sample reverse proxy configs for various docker images linuxserver provides and other commonly used applications. 

NOTE: We avoid providing samples that publicly expose server management software (ex: syno, qnap, unraid, proxmox, esxi, etc). Pull requests to add samples for this category of applications will not be accepted.

They are grouped in two:

1. `subfolder` these will allow accessing services at https://yourdomain.com/servicename
2. `subdomain` these will allow accessing services at https://servicename.yourdomain.com

## To enable the reverse proxy configs:

### Configure your default site config

Make sure that your default site config contains the following lines in the appropriate spots as seen in the default version:

1) For subfolder methods: `include /config/nginx/proxy-confs/*.subfolder.conf;`
2) For subdomain methods: `include /config/nginx/proxy-confs/*.subdomain.conf;`

### Ensure you have a custom docker network

These confs assume that the swag container can reach other containers via their dns hostnames (defaults to container name) resolved via docker's internal dns. This is achieved through having the containers attached to the same user defined docker bridge network. 

- If you are using docker-compose and the containers are managed through the same yaml file, docker-compose will automatically create a custom network and attach all containers to it. Nothing extra is required.

- If you are starting the containers via command line, first create a bridge network with the command `docker network create [networkname]` Then define that network in the container run/create command via `--network [networkname]`.

- If you are using a gui manager like portainer, you can create a custom bridge network in the gui, and select it when creating a new container.

- If you are using unraid, create a custom network in command line via `docker network create [networkname]`, then go to docker service settings (under advanced) and set the option `Preserve user defined networks:` to `Yes`. Then in each container setting, including the swag container, in the network type dropdown, select `Custom : [networkname]`.  This is a necessary step as the bridge network that unraid uses by default does not allow container to container communication.

If the reverse proxied containers are not reachable via dns or they are running on a different machine, you will have to modify these confs to fit your needs.

### Rename the required proxy configs

1) Rename the conf files and remove the `.sample` at the end (ie. `sonarr.subfolder.conf`)
2) Restart the swag container

### Make any necessary changes detailed in the config

Some applications require you to make changes to the service containers such as adding base urls in their settings. Each conf file lists the required changes on the first line.

If you are reverse proxying linuxserver containers installed on the same host with the recommended options, you shouldn't need to edit these conf files.

## To disable the configs:

Simply delete the confs and restart swag.
