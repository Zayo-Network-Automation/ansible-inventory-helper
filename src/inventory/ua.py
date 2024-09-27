import logging
import json
from os import environ
from shake_that_assurance import UnifiedAssuranceAPI
import re

UA_PRESENTATION_URL = environ.get("UA_PRESENTATION_URL", "https://presentation01.example.com")
UA_COLLECTOR_NAME_FILTER = environ.get("UA_COLLECTOR_NAME_FILTER", ".corp-collectors.example.com")
UA_INVENTORY_FILE = environ.get("UA_INVENTORY_FILE", "inventory.json")
UA_ANSIBLE_USER = environ.get("UA_ANSIBLE_USER", "ec2-user")
UA_API_USER = environ.get("UA_API_USER")
UA_API_PASS = environ.get("UA_API_PASS")

log_level = environ.get("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=log_level
)
logger = logging.getLogger(__name__)

def save_ansible_inventory(broker_servers, ansible_user, inventory_file):
    """Dump the Ansible inventory to stdout"""

    host_vars = {"ansible_user": ansible_user}
    hostnames_dict = {server: host_vars for server in broker_servers}

    # https://www.jeffgeerling.com/blog/creating-custom-dynamic-inventories-ansible
    ansible_inventory = {
        'federos_collectors': {
            'hosts': hostnames_dict,
            'vars': {
#               "ansible_ssh_private_key_file": "",
#               "ansible_user": ""
            }
        },
        "_meta": {
            "hostvars": {}
        }
    }
    with open(inventory_file, 'w') as file:
        file.write(json.dumps(ansible_inventory, indent=4))
    logging.info(f"Dynamic Ansible inventory saved to {inventory_file}")

def is_url(s):
    """Check if the input string is a URL."""
    return bool(re.match(r'^https?://', s))

def should_include_collector(collector):
    if not UA_COLLECTOR_NAME_FILTER :
        return True
    return UA_COLLECTOR_NAME_FILTER in collector.get('ServerHostFQDN', '')

def collector_inventory():

    if not is_url(UA_PRESENTATION_URL):
        raise ValueError("UA_PRESENTATION_URL must be a valid URL")

    ua = UnifiedAssuranceAPI(UA_PRESENTATION_URL, UA_API_USER, UA_API_PASS, log_level=logger.getEffectiveLevel())

    collector_list = []
    broker_servers = ua.get_broker_servers()
    for collector in broker_servers:
        if should_include_collector(collector):
            collector_list.append(collector.get('ServerHostFQDN'))
    save_ansible_inventory(collector_list, UA_ANSIBLE_USER, UA_INVENTORY_FILE)
