#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import json
import os

from translator.common.utils import CompareUtils
from translator.hot.tosca_translator import TOSCATranslator
from translator.tests.base import TestCase
from translator.toscalib.tosca_template import ToscaTemplate
import translator.toscalib.utils.yamlparser


class ToscaNetworkTest(TestCase):
    parsed_params = {'network_name': 'net1'}

    def test_translate_single_network_single_server(self):
        '''TOSCA template with single Network and single Compute.'''
        tosca_tpl = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "../toscalib/tests/data/network/"
            "tosca_one_server_one_network.yaml")

        tosca = ToscaTemplate(tosca_tpl)
        translate = TOSCATranslator(tosca, self.parsed_params)
        output = translate.translate()

        expected_resource_1 = {'type': 'OS::Neutron::Net',
                               'properties':
                               {'name': {'get_param': 'network_name'}
                                }}

        expected_resource_2 = {'type': 'OS::Neutron::Subnet',
                               'properties':
                               {'cidr': '192.168.0.0/24',
                                'ip_version': 4,
                                'allocation_pools': [{'start': '192.168.0.50',
                                                     'end': '192.168.0.200'}],
                                'gateway_ip': '192.168.0.1',
                                'network': {'get_resource': 'my_network'}
                                }}

        expected_resource_3 = {'type': 'OS::Neutron::Port',
                               'properties':
                               {'network': {'get_resource': 'my_network'}
                                }}

        expected_resource_4 = [{'port': {'get_resource': 'my_port'}}]

        output_dict = translator.toscalib.utils.yamlparser.simple_parse(output)

        resources = output_dict.get('resources')

        self.assertIn('my_network', resources.keys())
        self.assertIn('my_network_subnet', resources.keys())
        self.assertIn('my_port', resources.keys())
        self.assertIn('my_server', resources.keys())

        self.assertEqual(resources.get('my_network'), expected_resource_1)
        self.assertEqual(resources.get('my_network_subnet'),
                         expected_resource_2)

        diff = CompareUtils.diff_dicts(resources.get('my_port'),
                                       expected_resource_3)
        self.assertEqual({}, diff, '<difference> : ' +
                         json.dumps(diff, indent=4, separators=(', ', ': ')))

        self.assertIn('properties', resources.get('my_server'))
        self.assertIn('networks', resources.get('my_server').get('properties'))
        translated_resource = resources.get('my_server').\
            get('properties').get('networks')
        self.assertEqual(translated_resource, expected_resource_4)

    def test_translate_single_network_two_computes(self):
        '''TOSCA template with single Network and two Computes.'''
        tosca_tpl = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "../toscalib/tests/data/network/"
            "tosca_two_servers_one_network.yaml")

        tosca = ToscaTemplate(tosca_tpl)
        translate = TOSCATranslator(tosca, self.parsed_params)
        output = translate.translate()

        expected_resource_1 = {'type': 'OS::Neutron::Net',
                               'properties':
                               {'name': {'get_param': 'network_name'}
                                }}

        expected_resource_2 = {'type': 'OS::Neutron::Subnet',
                               'properties':
                               {'cidr': {'get_param': 'network_cidr'},
                                'ip_version': 4,
                                'network': {'get_resource': 'my_network'},
                                'allocation_pools': [{'start':
                                                      {'get_param':
                                                       'network_start_ip'},
                                                      'end':
                                                      {'get_param':
                                                       'network_end_ip'
                                                       }}
                                                     ]
                                }}

        expected_resource_3 = {'type': 'OS::Neutron::Port',
                               'properties':
                               {'network': {'get_resource': 'my_network'}
                                }}

        expected_resource_4 = {'type': 'OS::Neutron::Port',
                               'properties':
                               {'network': {'get_resource': 'my_network'}
                                }}

        expected_resource_5 = [{'port': {'get_resource': 'my_port'}}]

        expected_resource_6 = [{'port': {'get_resource': 'my_port2'}}]

        output_dict = translator.toscalib.utils.yamlparser.simple_parse(output)

        resources = output_dict.get('resources')

        self.assertIn('my_network', resources.keys())
        self.assertIn('my_network_subnet', resources.keys())
        self.assertIn('my_port', resources.keys())
        self.assertIn('my_port2', resources.keys())
        self.assertIn('my_server', resources.keys())
        self.assertIn('my_server2', resources.keys())

        self.assertEqual(resources.get('my_network'), expected_resource_1)
        self.assertEqual(resources.get('my_network_subnet'),
                         expected_resource_2)

        diff = CompareUtils.diff_dicts(resources.get('my_port'),
                                       expected_resource_3)
        self.assertEqual({}, diff, '<difference> : ' +
                         json.dumps(diff, indent=4, separators=(', ', ': ')))

        diff = CompareUtils.diff_dicts(resources.get('my_port2'),
                                       expected_resource_4)
        self.assertEqual({}, diff, '<difference> : ' +
                         json.dumps(diff, indent=4, separators=(', ', ': ')))

        self.assertIn('properties', resources.get('my_server'))
        self.assertIn('networks', resources.get('my_server').get('properties'))
        translated_resource = resources.get('my_server').\
            get('properties').get('networks')
        self.assertEqual(translated_resource, expected_resource_5)

        self.assertIn('properties', resources.get('my_server2'))
        self.assertIn('networks', resources.get('my_server2').
                      get('properties'))
        translated_resource = resources.get('my_server2').\
            get('properties').get('networks')
        self.assertEqual(translated_resource, expected_resource_6)

    def test_translate_server_existing_network(self):
        '''TOSCA template with 1 server attached to existing network.'''
        tosca_tpl = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "../toscalib/tests/data/network/"
            "tosca_server_on_existing_network.yaml")

        tosca = ToscaTemplate(tosca_tpl)
        translate = TOSCATranslator(tosca, self.parsed_params)
        output = translate.translate()

        expected_resource_1 = {'type': 'OS::Neutron::Port',
                               'properties':
                               {'network': {'get_param': 'network_name'}
                                }}

        expected_resource_2 = [{'port': {'get_resource': 'my_port'}}]

        output_dict = translator.toscalib.utils.yamlparser.simple_parse(output)

        resources = output_dict.get('resources')

        self.assertItemsEqual(resources.keys(), ['my_server', 'my_port'])

        self.assertEqual(resources.get('my_port'), expected_resource_1)

        self.assertIn('properties', resources.get('my_server'))
        self.assertIn('networks', resources.get('my_server').get('properties'))
        translated_resource = resources.get('my_server').\
            get('properties').get('networks')
        self.assertEqual(translated_resource, expected_resource_2)

    def test_translate_three_networks_single_server(self):
        '''TOSCA template with three Networks and single Compute.'''
        tosca_tpl = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "../toscalib/tests/data/network/"
            "tosca_one_server_three_networks.yaml")

        tosca = ToscaTemplate(tosca_tpl)
        translate = TOSCATranslator(tosca, self.parsed_params)
        output = translate.translate()

        output_dict = translator.toscalib.utils.yamlparser.simple_parse(output)

        resources = output_dict.get('resources')

        for net_num in range(1, 4):
            net_name = 'my_network%d' % (net_num)
            subnet_name = '%s_subnet' % (net_name)
            port_name = 'my_port%d' % (net_num)

            expected_resource_net = {'type': 'OS::Neutron::Net',
                                     'properties':
                                     {'name': 'net%d' % (net_num)}}

            expected_resource_subnet = {'type': 'OS::Neutron::Subnet',
                                        'properties':
                                        {'cidr': '192.168.%d.0/24' % (net_num),
                                         'ip_version': 4,
                                         'network': {'get_resource': net_name}}
                                        }

            expected_resource_port = {'type': 'OS::Neutron::Port',
                                      'properties':
                                      {'network': {'get_resource': net_name}}}

            self.assertIn(net_name, resources.keys())
            self.assertIn(subnet_name, resources.keys())
            self.assertIn(port_name, resources.keys())

            self.assertEqual(resources.get(net_name), expected_resource_net)
            self.assertEqual(resources.get(subnet_name),
                             expected_resource_subnet)

            diff = CompareUtils.diff_dicts(resources.get(port_name),
                                           expected_resource_port)
            self.assertEqual({}, diff, '<difference> : ' +
                             json.dumps(diff, indent=4,
                                        separators=(', ', ': ')))

        self.assertIn('properties', resources.get('my_server'))
        self.assertIn('networks', resources.get('my_server').get('properties'))
        translated_resource = resources.get('my_server').\
            get('properties').get('networks')

        expected_srv_networks = [{'port': {'get_resource': 'my_port1'}},
                                 {'port': {'get_resource': 'my_port2'}},
                                 {'port': {'get_resource': 'my_port3'}}]
        self.assertEqual(translated_resource, expected_srv_networks)
