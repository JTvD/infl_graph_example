# InfluxDB Grafana example
An example of how to setup a grafana instance, with influxDB as database and run a few types of commands.

## Preperation
For platform indepency and think ahead towards deployment, it is recommended to work with Docker containers.
The steps where tested on a windows machine, using [Docker Desktop](https://www.docker.com/products/docker-desktop/).
How to setup influx DB and grafana from scratch isdescribed in the following subsections, these can also be replaced by the docker compose.

### Docker compoase
Build and start the containers: `docker-compose up -d --build`  
Stop all containers: `docker kill $(docker ps -q)`  
View the logs: `docker logs --follow container_name` or check `/var/log/grafana` in the grafana container.

### Influx DB
There is a step by step guide on how to setup Influx DB on most operating systems: [influxDB installation procedure](https://docs.influxdata.com/influxdb/v2/install).  
However, it is recommended to start from the docker: [influx docker](https://hub.docker.com/_/influxdb)
as done by the docker-compose script.

## Connecting
If the docker compose script ran succesful the grafana dashboard is available on `http://localhost:3000/` with the credentials set in the `.env` file.
InfluxDB can be found on: `http://localhost:8086`

This setup has been tried on all OS'es, only on IOS users have to change the `localhost` to their own ipaddress.

### influxDB API
An API token must is required to read and write data to InfluxDB.
Create an API token via the `Load Data` menu on the left hand side, and `API tokens`. Press `GENERATE API TOKEN`. For testing it is recommended to start with an All Access token.

Next to the API token two additional fields are required to upload data:
•	Org: the organisation which was filled in on InfluxDB
•	Bucket: the bucket in which the data will be stored

Uploaded data can be viewed in InfluxDB's  Data Explorer. 

### Grafana datasource
In the Menu in Grafana sellect `Connections`, to add a new connection. Search for `InfluxDB`, `Add new data source`. 
A few things have to be filled in:
- URL: http://<the ip address of the machine>:8086/ 
- Name: define a name for the data source
- Query language: select the InfuxQL language
- Auth: Basic auth
- Database: InfluxDB bucket.
- User: InfluxDB username.
- Password: InfluxDB token.
Don't forget to test the connection. Each influxDB get's it's own bucket.
A full description is also available on the website of grafana: [influxdb datasource](https://grafana.com/docs/grafana/latest/datasources/influxdb/configure-influxdb-data-source/)

### Grafana queries & showing images
There are a lot of tutorials on grafana, it is recommended to take a look: [grafana tutorials](https://grafana.com/tutorials/)
In the examples only the `Business Media`, previously known as the `Base64` plugin is used to show images.

A handy trick is that the JSON model of the dashboard can be seen under `dashboard settings`, it is possible to create dashboards by code and back them up somewhere safe.


## The code
Querrying data from the influxDB or writing new values is described in the documentation of the python API: [influxDB API](https://docs.influxdata.com/influxdb/cloud/api-guide/client-libraries/python/)

The scripts rely on an environment file containing the following fields:
```
INFLUXDB_URL
INFLUXDB_TOKEN
INFLUXDB_ORG
INFLUXDB_BUCKET
```

Timezones are am important detail. Grafana can show local values in local time and UTC, but it asumes the data source uses UTC. Therefore it is recommended to upload the values to influxDB in UTC. 

When showing images with the `business media/Base64 plugin` it is a little hidden that settings on of the plugin must also be set corretly as describe in the [plugins documentation](https://grafana.com/grafana/plugins/volkovlabs-image-panel/)

![Businessmedia plugin](https://github.com/JTvD/infl_graph_example/blob/main/grafana_show_image.png)