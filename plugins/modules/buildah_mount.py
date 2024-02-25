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
module: buildah_mount
version_added: 0.0.1
short_description: Mount a working container's root filesystem
description:
     - Mount a working container's root filesystem.
options:
  name:
    description: containerID
    type: str
    required: true
  truncate:
    description: containerID
    type: bool
    default: false

# informational: requirements for nodes
requirements: [ buildah ]
author:
    - Red Hat Consulting (NAPS) (!UNKNOWN)
    - Lester Claudio (@claudiol)
'''

EXAMPLES = '''
- name: BUILDAH | Test output of "buildah add <image_name>" command
  buildah_mount:
    truncate: true
  register: result

- debug: var=result.stdout_lines
'''


def buildah_mount(module, name, truncate):

    if module.get_bin_path('buildah'):
        buildah_bin = module.get_bin_path('buildah')
        buildah_basecmd = [buildah_bin, 'mount']

    if truncate is not True:
        r_cmd = ['--notruncate']
        buildah_basecmd.extend(r_cmd)

    if name:
        r_cmd = [name]
        buildah_basecmd.extend(r_cmd)

    return module.run_command(buildah_basecmd)


def main():

    module = AnsibleModule(
        argument_spec=dict(
            name=dict(required=True),
            truncate=dict(required=False, default="no", type="bool")
        ),
        supports_check_mode=True
    )

    params = module.params

    name = params.get('name', '')
    truncate = params.get('truncate', '')

    rc, out, err = buildah_mount(module, name, truncate)

    if rc == 0:
        module.exit_json(changed=True, rc=rc, stdout=out, err=err)
    else:
        module.exit_json(changed=False, rc=rc, stdout=out, err=err)


# import module snippets
from ansible.module_utils.basic import AnsibleModule
if __name__ == '__main__':
    main()
