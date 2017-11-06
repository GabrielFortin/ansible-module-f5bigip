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

DOCUMENTATION = '''
---
module: f5bigip_ltm_rule
short_description: BIG-IP ltm rule module
description:
    - Configures an iRule for traffic management system configuration.
version_added: 2.3
author:
    - "Eric Jacob, @erjac77"
notes:
    - Requires BIG-IP software version >= 11.6
requirements:
    - f5-sdk
options:
	app_service:
        description:
            - Specifies the application service that the object belongs to.
        required: false
        default: null
        choices: []
        aliases: []
        version_added: 2.3
    definition:
        description:
            - Specifies the iRule definition.
        required: true
        default: null
        choices: []
        aliases: []
        version_added: 2.3
    ignore_verification:
        description:
            - 
        required: false
        default: null
        choices: []
        aliases: []
        version_added: 2.3
    name:
        description:
            - Specifies unique name for the component.
        required: true
        default: null
        choices: []
        aliases: []
        version_added: 2.3
    partition:
        description:
            - Specifies the administrative partition in which the component object resides.
        required: false
        default: Common
        choices: []
        aliases: []
        version_added: 2.3
    state:
        description:
            - Specifies the state of the component on the BIG-IP system.
        required: false
        default: present
        choices: ['absent', 'present']
        aliases: []
        version_added: 2.3
'''

EXAMPLES = '''
- name: Create LTM Rule
  f5bigip_ltm_rule:
    f5_hostname: 172.16.227.35
    f5_username: admin
    f5_password: admin
    f5_port: 443
    name: my_rule
    partition: Common
    definition: 'when RULE_INIT {}'
    ignore_verification: True
    state: present
  delegate_to: localhost
'''

from ansible_common_f5.f5_bigip import *

BIGIP_LTM_RULE_ARGS = dict(
    definition          =   dict(type='str'),
    app_service         =   dict(type='str'),
    ignore_verification =   dict(type='bool')#,
    #metadata            =   dict(type='list')
)

class F5BigIpLtmRule(F5BigIpNamedObject):
    def set_crud_methods(self):
        self.methods = {
            'create':   self.mgmt_root.tm.ltm.rules.rule.create,
            'read':     self.mgmt_root.tm.ltm.rules.rule.load,
            'update':   self.mgmt_root.tm.ltm.rules.rule.update,
            'delete':   self.mgmt_root.tm.ltm.rules.rule.delete,
            'exists':   self.mgmt_root.tm.ltm.rules.rule.exists
        }

def main():
    # Translation list for conflictual params
    tr = { 'definition':'api_anonymous' }
    
    module = AnsibleModuleF5BigIpNamedObject(argument_spec=BIGIP_LTM_RULE_ARGS, supports_check_mode=False)
    
    try:
        obj = F5BigIpLtmRule(check_mode=module.supports_check_mode, tr=tr, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))

from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()