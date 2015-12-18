# Copyright 2015 FUJITSU LIMITED
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from neutron.extensions import portbindings
from neutron.i18n import _LE
from neutron.i18n import _LI
from neutron.plugins.ml2.common import exceptions as ml2_exc
from neutron.plugins.ml2 import driver_api
from oslo_log import log as logging

LOG = logging.getLogger(__name__)


def get_network_info(context, net_id):
    segments = context.network.network_segments
    segment = segments[0]
    network_type = segment[driver_api.NETWORK_TYPE]
    segmentation_id = segment[driver_api.SEGMENTATION_ID]
    LOG.info(_LI("network_type = %s") % network_type)
    LOG.info(_LI("segmentation_id = %s") % segmentation_id)
    return network_type, segmentation_id


def get_physical_connectivity(port):
    # TODO(yushiro) replace following characters to constant value
    binding_profile = port['binding:profile']
    local_link_information = binding_profile.get("local_link_information", [])
    return local_link_information


def is_baremetal_deploy(port):
    vnic_type = port.get(portbindings.VNIC_TYPE, portbindings.VNIC_NORMAL)
    if (vnic_type != portbindings.VNIC_BAREMETAL):
        LOG.warn("This plugin is doing nothing before ironic-neutron\
                  integration will be merged.")
        return False
    elif get_physical_connectivity(port):
        return True
    else:
        LOG.warn("local_link_information is not specified.")
        return False


def _validate_network_type(network_type, method="_validate_network_type"):
    if network_type != 'vlan':
        LOG.error(
            _LE("Fujitsu Mechanism: only network type vlan is supported"))
        raise ml2_exc.MechanismDriverError(method=method)


def is_lag(local_link_information):
    return True if len(local_link_information) > 1 else False
