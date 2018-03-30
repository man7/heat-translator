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
TARGET_CLASS_NAME = 'ToscaIPsecSiteCon'
TOSCA_LINKS_TO = 'tosca.relationships.network.LinksTo'


class ToscaIPsecSiteCon(HotResource):
    '''Translate TOSCA node type tosca.nodes.network.IPsecSiteConnection'''

    toscatype = 'tosca.nodes.network.IPsecSiteConnection'

    def __init__(self, nodetemplate, csar_dir=None):
        super(ToscaIPsecSiteCon, self).__init__(nodetemplate,
                                              type='OS::Neutron::IPsecSiteConnection',
                                              csar_dir=csar_dir)

    def handle_properties(self):
        tosca_props = self.get_tosca_props()
        ipsecsitecon_props = {}
        for key, value in tosca_props.items():
            ipsecsitecon_props[key] = value

        links_to = None
        for rel, node in self.nodetemplate.relationships.items():
            if not links_to and rel.is_derived_from(TOSCA_LINKS_TO):
                links_to = node
                for hot_resource in self.depends_on_nodes:
                    if 'OS::Neutron::IPsecPolicy' == hot_resource.type:
                        ipsecsitecon_props['ipsecpolicy_id'] =\
                            '{ get_resource: %s }' % (hot_resource.name)
                    elif 'OS::Neutron::IKEPolicy' == hot_resource.type:
                          ipsecsitecon_props['ikepolicy_id'] =\
                              '{ get_resource: %s }' % (hot_resource.name)
                    elif 'OS::Neutron::VPNService' == hot_resource.type:
                          ipsecsitecon_props['vpnservice_id'] =\
                              '{ get_resource: %s }' % (hot_resource.name)

        self.properties = ipsecsitecon_props
