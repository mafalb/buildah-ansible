#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2019, Red Hat, Inc
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
module: buildah_containers
version_added: 0.0.1
short_description: buildah-containers - List the working containers and their base images.
description:
     - Lists  containers  which  appear to be Buildah working containers, their names and IDs, and
       the names and IDs of the images from which they were initialized.
options:
  json:
    description: output in JSON format
    type: bool
    default: false
  truncate:
    description: truncate
    type: bool
    default: true
  quiet:
    description: display only container IDs
    type: bool
    default: false
  format:
    description: pretty-print containers using a Go template
    type: str
  filter:
    description: filter output based on conditions provided
    type: str
  heading:
    description: do print column headings
    type: bool
    default: true

# informational: requirements for nodes
requirements: [ buildah ]
author:
    - Red Hat Consulting (NAPS) (!UNKNOWN)
    - Lester Claudio (@claudiol)
'''

EXAMPLES = '''
- name: BUILDAH | Test output of "buildah containers <image_name>" command
  buildah_containers:
    truncate: true
  register: result

- debug: var=result.stdout_lines

- name: BUILDAH | Test JSON output of "buildah containers --json <image_name>" command
  buildah_containers:
    json: true
  register: result

- debug: var=result.stdout_lines

- name: BUILDAH | Test output of "buildah containers --notruncate <image_name>" command
  buildah_containers:
    truncate: false
  register: result

- debug: var=result.stdout_lines

- name: BUILDAH | Test output of "buildah containers --noheading <image_name>" command
  buildah_containers:
    heading: false
  register: result

- debug: var=result.stdout_lines
'''


def buildah_list_containers(module, json, truncate, quiet, format, filter, heading):

    if module.get_bin_path('buildah'):
        buildah_bin = module.get_bin_path('buildah')
        buildah_basecmd = [buildah_bin, 'containers']

    if json:
        r_cmd = ['--json']
        buildah_basecmd.extend(r_cmd)

    if truncate is not True:
        r_cmd = ['--notruncate']
        buildah_basecmd.extend(r_cmd)

    if quiet:
        r_cmd = ['--quiet']
        buildah_basecmd.extend(r_cmd)

    if format != "":
        r_cmd = ['--format']
        buildah_basecmd.extend(r_cmd)
        r_cmd = [format]
        buildah_basecmd.extend(r_cmd)

    if filter != "":
        r_cmd = ['--filter']
        buildah_basecmd.extend(r_cmd)
        r_cmd = [filter]
        buildah_basecmd.extend(r_cmd)

    if heading:
        r_cmd = ['--noheading']
        buildah_basecmd.extend(r_cmd)

    return module.run_command(buildah_basecmd)


def main():

    module = AnsibleModule(
        argument_spec=dict(
            json=dict(required=False, default="no", type='bool'),
            truncate=dict(required=False, default="yes", type='bool'),
            quiet=dict(required=False, default="no", type='bool'),
            format=dict(required=False),
            filter=dict(required=False),
            heading=dict(required=False, type='bool', default=True)
        ),
        supports_check_mode=True
    )

    params = module.params

    json = params.get('json', '')
    truncate = params.get('truncate', '')
    quiet = params.get('quiet', '')
    format = params.get('format', '')
    filter = params.get('filter', '')
    heading = params.get('heading', '')

    rc, out, err = buildah_list_containers(module, json, truncate, quiet, format, filter, heading)

    if rc == 0:
        module.exit_json(changed=True, rc=rc, stdout=out, err=err)
    else:
        module.exit_json(changed=False, rc=rc, stdout=out, err=err)


# import module snippets
from ansible.module_utils.basic import AnsibleModule
if __name__ == '__main__':
    main()
