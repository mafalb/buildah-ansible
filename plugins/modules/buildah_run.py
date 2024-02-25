#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2012, Red Hat, Inc
# Based on yum module written by Seth Vidal <skvidal at fedoraproject.org>
# (c) 2014, Epic Games, Inc.
# Written by Lester Claudio <claudiol at redhat.com>
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

ANSIBLE_METADATA = {'status': ['stableinterface'],
                    'supported_by': 'core',
                    'version': '1.0'}

DOCUMENTATION = '''
---
module: buildah_run
version_added: 0.0.1
short_description: Runs a specified command using the container's root
                   filesystem as a root filesystem, using configuration
                   settings inherited from the container's image or as
                   specified using previous calls to the config command.


description:
     - Runs a specified command using the container's root filesystem

options:
  name:
    description: containerID
    required: true
    type: str
  command:
    description: command
    required: true
    type: str
  args:
    description: command arguments
    type: list
    elements: str
  cap_add:
    description: add the specified capability
    type: str
  cap_drop:
    description: drop the specified capability
    type: str
  cni_config_dir:
    description: cni_config_dir
    type: path
  cni_plugin_path:
    description: cni_plugin_path
    type: path
  ipc:
    description: path of IPC namespace to join
    type: str
  isolation:
    description: type of process isolation to use
    type: str
  net:
    description: network
    type: str
  pivot:
    description: pivot
    type: bool
    default: false
  pid:
    description: pid
    type: str
  runtime:
    description: path to an alternate OCI runtime
    type: str
  runtime_flag:
    description: add global flags for the container runtime
    type: str
  user:
    description: user[:group] to run the command as
    type: str
  uts:
    description: private, :path of UTS namespace to join, or 'host'
    type: str
  volume:
    description: bind mount a host location into the container while running the command
    type: str

# informational: requirements for nodes
requirements: [ buildah ]
author:
    - Red Hat Consulting (NAPS) (!UNKNOWN)
    - Lester Claudio (@claudiol)
'''

EXAMPLES = '''
- name: BUILDAH | Test output of "buildah run <image_name> <command>" command
  buildah_run:
    name: CONTAINER-ID-OR-NAME
    command: ls
  register: result

- debug: var=result.stdout_lines
'''


def buildah_run(module, name, command, args, cap_add, cap_drop, cni_config_dir,
                cni_plugin_path, hostname, ipc, isolation, network, pivot, pid,
                runtime, runtime_flag, security_options, user, uts, volume):

    if module.get_bin_path('buildah'):
        buildah_bin = module.get_bin_path('buildah')
        buildah_basecmd = [buildah_bin, 'run']

    # REVISIT - Multiple Entries
    if cap_add:
        r_cmd = ['--cap_add']
        buildah_basecmd.extend(r_cmd)
        r_cmd = [cap_add]
        buildah_basecmd.extend(r_cmd)

    # REVISIT - Multiple Entries
    if cap_drop:
        r_cmd = ['--cap_drop']
        buildah_basecmd.extend(r_cmd)
        r_cmd = [cap_drop]
        buildah_basecmd.extend(r_cmd)

    if cni_config_dir:
        r_cmd = ['--cni_config_dir']
        buildah_basecmd.extend(r_cmd)
        r_cmd = [cni_config_dir]
        buildah_basecmd.extend(r_cmd)

    if cni_plugin_path:
        r_cmd = ['--cni_plugin_path']
        buildah_basecmd.extend(r_cmd)
        r_cmd = [cni_plugin_path]
        buildah_basecmd.extend(r_cmd)

    if hostname:
        r_cmd = ['--hostname']
        buildah_basecmd.extend(r_cmd)
        r_cmd = [hostname]
        buildah_basecmd.extend(r_cmd)

    if ipc:
        r_cmd = ['--ipc']
        buildah_basecmd.extend(r_cmd)
        r_cmd = [ipc]
        buildah_basecmd.extend(r_cmd)

    if isolation:
        r_cmd = ['--isolation']
        buildah_basecmd.extend(r_cmd)
        r_cmd = [isolation]
        buildah_basecmd.extend(r_cmd)

    if network:
        r_cmd = ['--net']
        buildah_basecmd.extend(r_cmd)
        r_cmd = [network]
        buildah_basecmd.extend(r_cmd)

    if pivot:
        r_cmd = ['--no-pivot']
        buildah_basecmd.extend(r_cmd)

    if pid:
        r_cmd = ['--pid']
        buildah_basecmd.extend(r_cmd)
        r_cmd = [pid]
        buildah_basecmd.extend(r_cmd)

    if runtime:
        r_cmd = ['--runtime']
        buildah_basecmd.extend(r_cmd)
        r_cmd = [runtime_flag]
        buildah_basecmd.extend(r_cmd)

    if runtime_flag:
        r_cmd = ['--runtime_flag']
        buildah_basecmd.extend(r_cmd)
        r_cmd = [runtime_flag]
        buildah_basecmd.extend(r_cmd)

    if security_options:
        r_cmd = ['--security_opt']
        buildah_basecmd.extend(r_cmd)
        r_cmd = [security_options]
        buildah_basecmd.extend(r_cmd)

    if user:
        r_cmd = ['--user']
        buildah_basecmd.extend(r_cmd)
        r_cmd = [user]
        buildah_basecmd.extend(r_cmd)

    if uts:
        r_cmd = ['--uts']
        buildah_basecmd.extend(r_cmd)
        r_cmd = [uts]
        buildah_basecmd.extend(r_cmd)

    if volume:
        r_cmd = ['--volume']
        buildah_basecmd.extend(r_cmd)
        r_cmd = [volume]
        buildah_basecmd.extend(r_cmd)

    if name:
        r_cmd = [name]
        buildah_basecmd.extend(r_cmd)

    if command:
        r_cmd = [command]
        buildah_basecmd.extend(r_cmd)

    if args:
        if len(args) == 1:
            r_cmd = args
            buildah_basecmd.extend(r_cmd)
        else:
            for arg in args:
                r_cmd = [arg]
                buildah_basecmd.extend(r_cmd)

    return module.run_command(buildah_basecmd)


def main():

    module = AnsibleModule(
        argument_spec=dict(
            name=dict(required=True),
            command=dict(required=True),
            args=dict(required=False, type='list', elements='str'),
            cap_add=dict(required=False),
            cap_drop=dict(required=False),
            cni_config_dir=dict(type='path', required=False),
            cni_plugin_path=dict(type='path', required=False),
            ipc=dict(required=False),
            isolation=dict(required=False),
            net=dict(required=False),
            pivot=dict(required=False, default="no", type="bool"),
            pid=dict(required=False),
            runtime=dict(required=False),
            runtime_flag=dict(required=False),
            user=dict(required=False),
            uts=dict(required=False),
            volume=dict(required=False)
        ),
        supports_check_mode=True
    )

    params = module.params

    command = params.get('command', '')
    args = params.get('args', '')
    name = params.get('name', '')
    cap_add = params.get('cap_add', '')
    cap_drop = params.get('cap_drop', '')
    cni_config_dir = params.get('cni_config_dir', '')
    cni_plugin_path = params.get('cni_plugin_path', '')
    hostname = params.get('hostname', '')
    ipc = params.get('ipc', '')
    isolation = params.get('isolation', '')
    network = params.get('network', '')
    pivot = params.get('pivot', '')
    pid = params.get('pid', '')
    runtime = params.get('runtime', '')
    runtime_flag = params.get('runtime_flag', '')
    security_options = params.get('security_options', '')
    user = params.get('user', '')
    uts = params.get('uts', '')
    volume = params.get('volume', '')

    rc, out, err = buildah_run(
        module, name, command, args, cap_add, cap_drop, cni_config_dir,
        cni_plugin_path, hostname, ipc, isolation, network, pivot, pid,
        runtime, runtime_flag, security_options, user, uts, volume)

    if rc == 0:
        module.exit_json(changed=True, rc=rc, stdout=out, err=err)
    else:
        module.fail_json(msg=err)


# import module snippets
from ansible.module_utils.basic import AnsibleModule
if __name__ == '__main__':
    main()
