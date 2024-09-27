# Collector Inventory List

A collection of helpers for building an Ansible dynamic inventories.

## Current helpers

### ua-collector-inventory

Unified Assurance (UA) collectors known by a UA presentation server.

It needs to know the UA api endpoint to query. This can be passed as the first command line parameter, as an environment variable `UA_FQDN`, or you will be prompted to enter it manually.

```sh
export UA_INVENTORY_FILE="mycollectors.json"
export UA_COLLECTOR_NAME_FILTER="mycollectors.example.com"
export UA_API_USER=$(pass ASSURE1_API_USERNAME)
export UA_API_PASS=$(pass ASSURE1_API_PASSWORD)
export UA_PRESENTATION_URL="https://presentation01.example.com"
ua-collector-inventory
```

The presentation url is the api endpoint to discover the collectors. The collector name filter is an optional string filter to use excluding any non-collector servers.

## Inspecting the results

```sh
ansible-inventory -i inventory.json --graph
```
