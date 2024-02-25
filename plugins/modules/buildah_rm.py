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

import os
import platform
import tempfile
import shutil

ANSIBLE_METADATA = {'status': ['stableinterface'],
                    'supported_by': 'core',
                    'version': '1.0'}

DOCUMENTATION = '''
---
module: buildah_rm
version_added: 0.0.1
short_description: Removes one or more working containers, unmounting them if necessary.

description:
     - Removes one or more working containers, unmounting them if necessary.

options:
  name:
    description: containerID
    type: str
  all:
    description: remove all containers
    type: bool
    default: false

# informational: requirements for nodes
requirements: [ buildah ]
author:
    - Red Hat Consulting (NAPS) (!UNKNOWN)
    - Lester Claudio (@claudiol)
'''

EXAMPLES = '''
- name: BUILDAH | Test output of "buildah rm <image_name>" command
  buildah_rm:
    name: CONTAINER-ID-OR-NAME
  register: result

- debug: var=result.stdout_lines

- name: BUILDAH | Test output of "buildah rm --all" command
  buildah_rm:
    all: true
  register: result

- debug: var=result.stdout_lines
'''


def buildah_rm(module, name, all):

    if module.get_bin_path('buildah'):
        buildah_bin = module.get_bin_path('buildah')
        buildah_basecmd = [buildah_bin, 'rm']

    if all:
        r_cmd = ['--all']
        buildah_basecmd.extend(r_cmd)
    elif name:
        r_cmd = [name]
        buildah_basecmd.extend(r_cmd)

    return module.run_command(buildah_basecmd)


def main():

    module = AnsibleModule(
        argument_spec=dict(
            name=dict(required=False),
            all=dict(required=False, default="no", type="bool")
        ),
        supports_check_mode=True,
        mutually_exclusive=[['name', 'all']],
        required_one_of=[['name', 'all']],
    )

    params = module.params

    name = params.get('name', '')
    all = params.get('all', '')

    rc, out, err = buildah_rm(module, name, all)

    if rc == 0:
        module.exit_json(changed=True, rc=rc, stdout=out, err=err)
    else:
        module.fail_json(msg=err)


# import module snippets
from ansible.module_utils.basic import AnsibleModule
if __name__ == '__main__':
    main()
