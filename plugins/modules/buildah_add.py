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
module: buildah_add
version_added: 0.0.1
short_description: Allows the creation of Open Container Initiative (OCI) containers using the buildah command
description:
  - Creates, removes, and lists OCI containers using the buildah container manager.
options:
  name:
    description: The buildah to add to
    type: str
    required: true
  chown:
    description: user and/or group
    type: str
    required: false
  quiet:
    description: quiet
    type: bool
    required: false
    default: false
  src:
    description: The source path
    type: str
    required: true
  dest:
    description: The destination path
    type: str
    required: true

# informational: requirements for nodes
requirements: [ buildah ]
author:
  - Red Hat Consulting (@NAPS)
  - Lester Claudio (@claudiol)
'''

EXAMPLES = '''
- name: BUILDAH | Test output of "buildah add <image_name>" command
  buildah_add:
    name: 32282b25dcb9
    src: HelloWorld.txt
    dest: /tmp/HelloWorld.txt
    chown: 'root:root'
  register: result

- debug: var=result.stdout_lines
'''


def buildah_add(module, name, chown, quiet, src, dest):

    if module.get_bin_path('buildah'):
        buildah_bin = module.get_bin_path('buildah')
        buildah_basecmd = [buildah_bin, 'add']

    if chown:
        r_cmd = ['--chown']
        buildah_basecmd.extend(r_cmd)
        r_cmd = [chown]
        buildah_basecmd.extend(r_cmd)

    if quiet:
        r_cmd = ['--quiet']
        buildah_basecmd.extend(r_cmd)

    if name:
        r_cmd = [name]
        buildah_basecmd.extend(r_cmd)

    if src:
        r_cmd = [src]
        buildah_basecmd.extend(r_cmd)

    if dest:
        r_cmd = [dest]
        buildah_basecmd.extend(r_cmd)

    return module.run_command(buildah_basecmd)


def main():

    module = AnsibleModule(
        argument_spec=dict(
            name=dict(required=True),
            chown=dict(required=False),
            quiet=dict(required=False, default=False, type="bool"),
            src=dict(required=True),
            dest=dict(required=True)
        ),
        supports_check_mode=True
    )

    params = module.params

    name = params.get('name', '')
    chown = params.get('chown', '')
    quiet = params.get('quiet', '')
    src = params.get('src', '')
    dest = params.get('dest', '')

    rc, out, err = buildah_add(module, name, chown, quiet, src, dest)

    if rc == 0:
        module.exit_json(changed=True, rc=rc, stdout=out, err=err)
    else:
        module.fail_json(msg=err)


# import module snippets
from ansible.module_utils.basic import AnsibleModule
# from ansible.module_utils.urls import *
if __name__ == '__main__':
    main()
