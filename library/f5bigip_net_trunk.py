#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2016-2018, Eric Jacob <erjac77@gmail.com>
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
module: f5bigip_net_trunk
short_description: BIG-IP net trunk module
description:
    - Configures a trunk with link aggregation.
version_added: "2.4"
author:
    - "Gabriel Fortin (@gabrielfortin)"
options:
   app_service:
        description:
		    - Specifies the name of the application service to which the object belongs.
    bandwidth:
        description:
            - Specifies the operation bandwidth in bytes per second.
    description:
        description:
            - User defined description.
    distribution_hash:
        description:
            - Specifies the basis for the hash that the system uses as the framedistribution algorithm.
        choices: ['dst-mac', 'src-dst-ipport', 'src-dst-mac']
    interfaces:
        description:
            - Specifies the interfaces by name separated by spaces that you want to addto the trunk, delete from the trunk, or with which you want to replace all
              existing interfaces associated with the trunk.
    lacp:
        description:
            - Specifies, when enabled, that the system supports the link aggregationcontrol protocol (LACP), which monitors the trunk by exchanging
              control packets over the member links to determine the health of thelinks.
        default: disabled
        choices: ['enabled', 'disabled']
    lacp_mode:
        description:
            - Specifies the operation mode for LACP if the lacp option is enabled forthe trunk.
        choices: ['active', 'passive']
    lacp_timeout:
        description:
            - Specifies the rate at which the system sends the LACP control packets.
        default: long
        chocies: ['short', 'long']
    link_select_policy:
        description:
            - Sets the LACP policy that the trunk uses to determine which memberlink (interface) can handle new traffic.
        choices: ['auto', 'maximum-bandwidth']
    mac_address:
        description:
            - Specifies the media access control (MAC) address, which is associatedwith the trunk, in not case-sensitive hexadecimal colon notation, for
              example, 00:0b:09:88:00:9a.
    name:
        description:
            - Specifies unique name for the component.
        required: true
    partition:
        description:
            - Specifies the administrative partition in which the component object resides.
        default: common
    state:
        description:
            - Specifies the state of the component on the BIG-IP system.
        default: present
        choices: ['absent', 'present']
    stp:
        description:
            - Enables or disables spanning tree protocols (STP).
        default: enabled
        choices: ['enabled', 'disabled']
    stp_reset:
        description:
            - Resets STP, which forces a migration check.
    qinq_ethertype:
        description:
            - Specifies the ether-type value used for the packets handled on this trunk when it is a member in a QinQ
              vlan.
notes:
    - Requires BIG-IP software version >= 11.6
requirements:
    - ansible-common-f5
    - f5-sdk
'''

EXAMPLES = '''
- name: Create NET Trunk
  f5bigip_net_trunk:
    f5_hostname: 172.16.227.35
    f5_username: admin
    f5_password: admin
    f5_port: 443
    name: my_trunk
    partition: Common
    state: present
  delegate_to: localhost
'''

RETURN = ''' # '''

from ansible.module_utils.basic import AnsibleModule
from ansible_common_f5.base import F5_ACTIVATION_CHOICES
from ansible_common_f5.base import F5_NAMED_OBJ_ARGS
from ansible_common_f5.base import F5_PROVIDER_ARGS
from ansible_common_f5.bigip import F5BigIpNamedObject


class ModuleParams(object):
    @property
    def argument_spec(self):
        argument_spec = dict(
            app_service=dict(type='str'),
            bandwidth=dict(type='int'),
            description=dict(type='str'),
            distribution_hash=dict(type='str', choices=['dst-mac', 'src-dst-ipport', 'src-dst-mac']),
            interfaces=dict(type='list'),
            lacp=dict(type='str', choices=F5_ACTIVATION_CHOICES),
            lacp_mode=dict(type='str', choices=['active', 'passive']),
            lacp_timeout=dict(type='str', choices=['short', 'long']),
            link_select_policy=dict(type='str', choices=['auto', 'maximum-bandwidth']),
            mac_address=dict(type='str'),
            stp=dict(type='str', choices=F5_ACTIVATION_CHOICES),
            stp_reset=dict(type='str'),
            qinq_ethertype=dict(type='str')
        )
        argument_spec.update(F5_PROVIDER_ARGS)
        argument_spec.update(F5_NAMED_OBJ_ARGS)
        return argument_spec

    @property
    def supports_check_mode(self):
        return False

class F5BigIpNetTrunk(F5BigIpNamedObject):
    def _set_crud_methods(self):
        self._methods = {
            'create': self._api.tm.net.trunks.trunk.create,
            'read': self._api.tm.net.trunks.trunk.load,
            'update': self._api.tm.net.trunks.trunk.update,
            'delete': self._api.tm.net.trunks.trunk.delete,
            'exists': self._api.tm.net.trunks.trunk.exists
        }


def main():
    params = ModuleParams()
    module = AnsibleModule(argument_spec=params.argument_spec, supports_check_mode=params.supports_check_mode)

    try:
        obj = F5BigIpNetTrunk(check_mode=module.check_mode, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))


if __name__ == '__main__':
    main()
