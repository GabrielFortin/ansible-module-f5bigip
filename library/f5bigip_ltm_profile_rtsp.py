#!/usr/bin/python
#
# Copyright 2016, Eric Jacob <erjac77@gmail.com>
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
module: f5bigip_ltm_profile_rtsp
short_description: BIG-IP ltm profile rtsp module
description:
    - Configures an RTSP (realtime streaming protocol) profile.
version_added: 2.3
author:
    - "Gabriel Fortin"
notes:
    - Requires BIG-IP software version >= 11.6
requirements:
    - f5-sdk
options:
    app_service:
        description:
            - Specifies the name of the application service to which the profile belongs.
        required: false
        default: none
        choices: []
        aliases: []
    check_source:
        description:
            - When enabled the system uses the source attribute in the transport header to establish the target address of the RTP stream, and before the response is forwarded to the client, updates the value of the source attribute to be the virtual address of the BIG-IP system.
        required: false
        default: enabled
        choices: ['disabled', 'enabled']
        aliases: []
    defaults_from:
        description:
            - Specifies the profile that you want to use as the parent profile.
        required: false
        default: rtsp
        choices: []
        aliases: []
    description:
        description:
            - User defined description.
        required: false
        default: null
        choices: []
        aliases: []
    idle_timeout:
        description:
            - Specifies the number of seconds that a connection is idle before the connection is eligible for deletion.
        required: false
        default: 300
        choices: []
        aliases: []
    log_profile:
        description:
            - Specify the name of the ALG log profile which controls the logging of ALG .
        required: false
        default: null
        choices: []
        aliases: []
    log_publisher:
        description:
            - Specify the name of the log publisher which logs translation events.
        required: false
        default: null
        choices: []
        aliases: []
    max_header_size:
        description:
            - Specifies the maximum size of an RTSP request or response header that the RTSP filter accepts before dropping the connection.
        required: false
        default: 4096
        choices: []
        aliases: []
    max_queued_data:
        description:
            - Specifies the maximum amount of data that the RTSP filter buffers before dropping the connection.
        required: false
        default: 32768
        choices: []
        aliases: []
    multicast_redirect:
        description:
            - Specifies whether to enable or disable multicast redirect.
        required: false
        default: disabled
        choices: ['disabled', 'enabled']
        aliases: []
    name:
        description:
            - Specifies a unique name for the component.
        required: true
        default: none
        choices: []
        aliases: []
    partition:
        description:
            - Displays the administrative partition within which the component resides.
        required: false
        default: null
        choices: []
        aliases: []
    proxy:
        description:
            - When the proxy option is set, specifies the name of the header in the RTSP proxy configuration that is passed from the client-side virtual server to the server-side virtual server.
        required: false
        default: none
        choices: []
        aliases: []
    proxy_header:
        description:
            - When the proxy option is set, specifies the name of the header in the RTSP proxy configuration that is passed from the client-side virtual server to the server-side virtual server.
        required: false
        default: none
        choices: []
        aliases: []
    real_http_persistence:
        description:
            - Specifies whether to enable or disable real HTTP persistence.
        required: false
        default: enabled
        choices: ['disabled', 'enabled']
        aliases: []
    rtcp_port:
        description:
            - Specifies the number of the port to use for the Real Time Control Protocol (RTCP) service.
        required: false
        default: 0
        choices: []
        aliases: []
    rtp_port:
        description:
            - Specifies the number of the port to use for the RTP service.
        required: false
        default: null
        choices: []
        aliases: []
    session_reconnect:
        description:
            - Specifies whether to enable or disable session reconnect.
        required: false
        default: disabled
        choices: ['disabled', 'enabled']
        aliases: []
    state:
        description:
            - Specifies the state of the component on the BIG-IP system.
        required: false
        default: present
        choices: ['absent', 'present']
        aliases: []
    unicast_redirect:
        description:
            - Specifies whether to enable or disable unicast redirect.
        required: false
        default: disabled
        choices: ['disabled', 'enabled']
        aliases: []
'''

EXAMPLES = '''
- name: Create LTM Profile RTSP
  f5bigip_ltm_profile_rtsp:
    f5_hostname: 172.16.227.35
    f5_username: admin
    f5_password: admin
    f5_port: 443
    name: my_rtsp_profile
    partition: Common
    description: My rtsp profile
    state: present
  delegate_to: localhost
'''

from ansible_common_f5.f5_bigip import *

BIGIP_LTM_PROFILE_RTSP_ARGS = dict(
    app_service              =    dict(type='str'),
    check_source             =    dict(type='str', choices=F5_ACTIVATION_CHOICES),
    defaults_from            =    dict(type='str'),
    description              =    dict(type='str'),
    idle_timeout             =    dict(type='int'),
    log_profile              =    dict(type='str'),
    log_publisher            =    dict(type='str'),
    max_header_size          =    dict(type='int'),
    max_queued_data          =    dict(type='int'),
    multicast_redirect       =    dict(type='str', choices=F5_ACTIVATION_CHOICES),
    proxy                    =    dict(type='str'),
    proxy_header             =    dict(type='str'),
    real_http_persistence    =    dict(type='str', choices=F5_ACTIVATION_CHOICES),
    rtcp_port                =    dict(type='int'),
    rtp_port                 =    dict(type='int'),
    session_reconnect        =    dict(type='str', choices=F5_ACTIVATION_CHOICES),
    unicast_redirect         =    dict(type='str', choices=F5_ACTIVATION_CHOICES)
)

class F5BigIpLtmProfileRtsp(F5BigIpNamedObject):
    def set_crud_methods(self):
        self.methods = {
            'create':   self.mgmt_root.tm.ltm.profile.rtsps.rtsp.create,
            'read':     self.mgmt_root.tm.ltm.profile.rtsps.rtsp.load,
            'update':   self.mgmt_root.tm.ltm.profile.rtsps.rtsp.update,
            'delete':   self.mgmt_root.tm.ltm.profile.rtsps.rtsp.delete,
            'exists':   self.mgmt_root.tm.ltm.profile.rtsps.rtsp.exists
        }

def main():
    # Translation list for conflictual params
    tr = {}

    module = AnsibleModuleF5BigIpNamedObject(argument_spec=BIGIP_LTM_PROFILE_RTSP_ARGS, supports_check_mode=False)

    try:
        obj = F5BigIpLtmProfileRtsp(check_mode=module.supports_check_mode, tr=tr, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))

from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()