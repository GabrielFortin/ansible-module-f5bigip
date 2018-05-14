#!/usr/bin/python
#
# Copyright 2016-2017, Eric Jacob <erjac77@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: f5bigip_gtm_monitor_gateway_icmp
short_description: BIG-IP gtm monitor gateway-icmp monitor module
description:
    - Configures a Gateway Internet Control Message Protocol (ICMP) monitor.
version_added: "2.4"
author:
    - "Gabriel Fortin (@GabrielFortin)"
options:
    defaults_from:
        description:
            - Specifies the name of the monitor from which you want your custom monitor to inherit settings.
        default: gateway_icmp
    description:
        description:
            - User defined description.
    destination:
        description:
            - Specifies the IP address and service port of the resource that is the destination of this monitor.
        default: *:*
    ignore_down_response:
        description:
            - Specifies whether the monitor ignores a down response from the system it is monitoring.
        default: disabled
        choices: ['enabled', 'disabled']
    interval:
        description:
            - Specifies, in seconds, the frequency at which the system issues the monitor check when either the resource
              is down or the status of the resource is unknown.
        default: 30
    name:
        description:
            - Specifies a unique name for the component.
        required: true
    partition:
        description:
            - Specifies the administrative partition in which the component object resides.
        default: Common
    probe_attempts:
        description:
            - Specifies the number of times the BIG-IP system attempts to probe the host server, after which the
              BIG-IP system considers the host server down or unavailable.
        default: 3
    probe_interval:
        description:
            - Specifies the frequency at which the BIG-IP system probes the host server.
        default: 1
    probe_timeout:
        description:
            - Specifies the number of seconds after which the BIG-IP system times out the probe request to the BIG-IP system.
        default: 5
    state:
        description:
            - Specifies the state of the component on the BIG-IP system.
        default: present
        choices: ['absent', 'present']
    timeout:
        description:
            - Specifies the number of seconds the target has in which to respond to the monitor request.
        default: 120
    transparent:
        description:
            - Specifies whether the monitor operates in transparent mode.
        default: disabled
        choices: ['enabled', 'disabled']
notes:
    - Requires BIG-IP software version >= 11.6
requirements:
    - ansible-common-f5
    - f5-sdk
'''

EXAMPLES = '''
- name: Create GTM Gateway ICMP Monitor
  f5bigip_gtm_monitor_gateway_icmp:
    f5_hostname: 172.16.227.35
    f5_username: admin
    f5_password: admin
    f5_port: 443
    name: my_gateway_icmp_monitor
    partition: Common
    state: present
  delegate_to: localhost
'''

RETURN = '''
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_common_f5.f5_bigip import *

BIGIP_GTM_MONITOR_GATEWAY_ICMP_ARGS = dict(
    defaults_from=dict(type='str'),
    description=dict(type='str'),
    destination=dict(type='str'),
    ignore_down_response=dict(type='str', choices=F5_ACTIVATION_CHOICES),
    interval=dict(type='int'),
    probe_attemps=dict(type='int'),
    probe_interval=dict(type='int'),
    probe_timeout=dict(type='int'),
    timeout=dict(type='int'),
    transparent=dict(type='str', choices=F5_ACTIVATION_CHOICES)
)


class F5BigIpGtmMonitorGatewayIcmp(F5BigIpNamedObject):
    def set_crud_methods(self):
        self.methods = {
            'create': self.mgmt_root.tm.gtm.monitor.gateway_icmps.gateway_icmp.create,
            'read': self.mgmt_root.tm.gtm.monitor.gateway_icmps.gateway_icmp.load,
            'update': self.mgmt_root.tm.gtm.monitor.gateway_icmps.gateway_icmp.update,
            'delete': self.mgmt_root.tm.gtm.monitor.gateway_icmps.gateway_icmp.delete,
            'exists': self.mgmt_root.tm.gtm.monitor.gateway_icmps.gateway_icmp.exists
        }


def main():
    module = AnsibleModuleF5BigIpNamedObject(argument_spec=BIGIP_GTM_MONITOR_GATEWAY_ICMP_ARGS, supports_check_mode=False)

    try:
        obj = F5BigIpGtmMonitorGatewayIcmp(check_mode=module.supports_check_mode, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))


if __name__ == '__main__':
    main()
