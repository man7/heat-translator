#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from translator.hot.syntax.hot_resource import HotResource

# Name used to dynamically load appropriate map class.
TARGET_CLASS_NAME = 'ToscaIpsec'
TOSCA_LINKS_TO = 'tosca.relationships.network.LinksTo'


class ToscaIpsec(HotResource):
    '''Translate TOSCA node type tosca.nodes.network.IPsecPolicy'''

    toscatype = 'tosca.nodes.network.IPsecPolicy'

    def __init__(self, nodetemplate, csar_dir=None):
        super(ToscaIpsec, self).__init__(nodetemplate	,
                                              type='OS::Neutron::IPsecPolicy',
                                              csar_dir=csar_dir)

    def handle_properties(self):
        tosca_props = self.get_tosca_props()
        print tosca_props
        ipsec_props = {}
        for key, value in tosca_props.items():
            ipsec_props[key] = value

        self.properties = ipsec_props
