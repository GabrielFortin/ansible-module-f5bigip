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
module: f5bigip_gtm_monitor_postgresql
short_description: BIG-IP gtm monitor postgresql module
description:
    - Configures a PostgreSQL monitor.
version_added: "2.4"
author:
    - "Gabriel Fortin (@GabrielFortin)"
options:
    count:
        description:
            - Specifies the number of monitor probes after which the connection to the database will be terminated.
        default: 0
    database:
        description:
            - Specifies the name of the database with which the monitor attempts to communicate
    debug:
        description:
            - Specifies whether the monitor sends error messages and additional information to a log file created and
              labeled specifically for this monitor.
        default: no
        choices: ['no', 'yes']
    defaults_from:
        description:
            - Specifies the name of the monitor from which you want your custom monitor to inherit settings.
        default: postgresql
    description:
        description:
            - User defined description.
    destination:
        description:
            - Specifies the IP address and service port of the resource that is the destination of this monitor.
        default: '*:*'
    ignore_down_response:
        description:
            - Specifies whether the monitor ignores a down response from the system it is monitoring.
        default: disabled
        choices: ['disabled', 'enabled']
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
    password:
        description:
            - Specifies the password if the monitored target requires authentication.
        required: none
    probe_timeout:
        description:
            - Specifies the number of seconds after which the BIG-IP(r) system times out the probe request to the
              BIG-IP system.
        default: 5
    recv:
        description:
            - Specifies the text string that the monitor looks for in the returned resource
    recv_column:
        description:
            - Specifies the column in the database where the system expects the specified Receive String to be located
    recv_row:
        description:
            - Specifies the row in the database where the system expects the specified Receive String to be located
    send:
        description:
            - Specifies the SQL query that the monitor sends to the target database, for example, SELECT count(*) FROM
              mytable.
    state:
        description:
            - Specifies the state of the component on the BIG-IP system.
        default: present
        choices: ['absent', 'present']
    timeout:
        description:
            - Specifies the number of seconds the target has in which to respond to the monitor request.
        default: 91
    username:
        description:
            - Specifies the username, if the monitored target requires authentication
requirements:
    - BIG-IP >= 12.0
    - ansible-common-f5
    - f5-sdk
'''

EXAMPLES = '''
- name: Create GTM Monitor PostgreSQL
  f5bigip_gtm_monitor_postgresql:
    f5_hostname: 172.16.227.35
    f5_username: admin
    f5_password: admin
    f5_port: 443
    name: my_postgresql_monitor
    partition: Common
    description: My postgresql monitor
    state: present
  delegate_to: localhost
'''

RETURN = ''' # '''

from ansible.module_utils.basic import AnsibleModule
from ansible_common_f5.base import F5_ACTIVATION_CHOICES
from ansible_common_f5.base import F5_POLAR_CHOICES
from ansible_common_f5.base import F5_NAMED_OBJ_ARGS
from ansible_common_f5.base import F5_PROVIDER_ARGS
from ansible_common_f5.bigip import F5BigIpNamedObject


class ModuleParams(object):
    @property
    def argument_spec(self):
        argument_spec = dict(
            count=dict(type='int'),
            database=dict(type='str'),
            debug=dict(type='str', choices=F5_POLAR_CHOICES),
            defaults_from=dict(type='str'),
            description=dict(type='str'),
            destination=dict(type='str'),
            ignore_down_response=dict(type='str', choices=F5_ACTIVATION_CHOICES),
            interval=dict(type='int'),
            password=dict(type='str', no_log=True),
            recv=dict(type='str'),
            recv_column=dict(type='str'),
            recv_row=dict(type='str'),
            send=dict(type='str'),
            timeout=dict(type='int'),
            username=dict(type='str')
        )
        argument_spec.update(F5_PROVIDER_ARGS)
        argument_spec.update(F5_NAMED_OBJ_ARGS)
        return argument_spec

    @property
    def supports_check_mode(self):
        return False


class F5BigIpGtmMonitorPostgresql(F5BigIpNamedObject):
    def _set_crud_methods(self):
        self._methods = {
            'create': self._api.tm.gtm.monitor.postgresqls.postgresql.create,
            'read': self._api.tm.gtm.monitor.postgresqls.postgresql.load,
            'update': self._api.tm.gtm.monitor.postgresqls.postgresql.update,
            'delete': self._api.tm.gtm.monitor.postgresqls.postgresql.delete,
            'exists': self._api.tm.gtm.monitor.postgresqls.postgresql.exists
        }


def main():
    params = ModuleParams()
    module = AnsibleModule(argument_spec=params.argument_spec, supports_check_mode=params.supports_check_mode)

    try:
        obj = F5BigIpGtmMonitorPostgresql(check_mode=module.supports_check_mode, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))


if __name__ == '__main__':
    main()
