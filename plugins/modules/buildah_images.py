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
module: buildah_images
version_added: 0.0.1
short_description: Allows the creation of Open Container Initiative (OCI) containers using the buildah command
description:
     - Creates, removes, and lists OCI containers using the buildah container manager.
options:
  name:
    description: imageName
    type: str
  json:
    description: output in JSON format
    type: bool
    default: false
  truncate:
    description: do or do not truncate output
    type: bool
    default: true
  digests:
    description: show digests
    type: bool
    default: false
  format:
    description: pretty-print images using a Go template
    type: str
    default: ""
  filter:
    description: filter output based on conditions provided
    type: str
    default: ""
  heading:
    description: do not print column headings
    type: bool
    default: true

# informational: requirements for nodes
requirements: [ buildah ]
author:
    - Red Hat Consulting (NAPS) (!UNKNOWN)
    - Lester Claudio (@claudiol)
'''

EXAMPLES = '''
- name: BUILDAH | Test output of "buildah images <image_name>" command
  buildah_images:
    name: docker.io/library/fedora
    truncate: true
  register: result

- debug: var=result.stdout_lines

- name: BUILDAH | Test JSON output of "buildah images --json <image_name>" command
  buildah_images:
    name: docker.io/library/fedora
    json: true
  register: result

- debug: var=result.stdout_lines

- name: BUILDAH | Test output of "buildah images --no-trunc <image_name>" command
  buildah_images:
    name: docker.io/library/fedora
    truncate: false
  register: result

- debug: var=result.stdout_lines

- name: BUILDAH | Test output of "buildah images --noheading <image_name>" command
  buildah_images:
    name: docker.io/library/fedora
    heading: false
  register: result

- debug: var=result.stdout_lines
'''


def buildah_list_images(module, name, json, truncate, digests, format, filter, heading):

    if module.get_bin_path('buildah'):
        buildah_bin = module.get_bin_path('buildah')
        buildah_basecmd = [buildah_bin, 'images']

    if json:
        r_cmd = ['--json']
        buildah_basecmd.extend(r_cmd)

    if truncate is not True:
        r_cmd = ['--no-trunc']
        buildah_basecmd.extend(r_cmd)

    if format != "":
        r_cmd = ['--format']
        buildah_basecmd.extend(r_cmd)
        r_cmd = [format]
        buildah_basecmd.extend(r_cmd)

    if digests:
        r_cmd = ['--digests']
        buildah_basecmd.extend(r_cmd)

    if heading:
        r_cmd = ['--noheading']
        buildah_basecmd.extend(r_cmd)

    if name:
        r_cmd = [name]
        buildah_basecmd.extend(r_cmd)

    return module.run_command(buildah_basecmd)


def main():

    module = AnsibleModule(
        argument_spec=dict(
            name=dict(required=False),
            json=dict(required=False, default=False, type='bool'),
            truncate=dict(required=False, default=True, type='bool'),
            digests=dict(required=False, default=False, type='bool'),
            format=dict(required=False, default=""),
            filter=dict(required=False, default=""),
            heading=dict(required=False, default=True, type='bool')
        ),
        # required_one_of=[['name', 'str']],
        # mutually_exclusive=[['name', 'str']],
        supports_check_mode=True
    )

    params = module.params

    id = params.get('name', '')
    json = params.get('json', '')
    truncate = params.get('truncate', '')
    digests = params.get('digests', '')
    format = params.get('format', '')
    filter = params.get('filter', '')
    heading = params.get('heading', '')

    rc, out, err = buildah_list_images(module, id, json, truncate, digests, format, filter, heading)

    if rc == 0:
        module.exit_json(changed=True, rc=rc, stdout=out, err=err)
    else:
        module.exit_json(changed=False, rc=rc, stdout=out, err=err)


# import module snippets
from ansible.module_utils.basic import AnsibleModule
if __name__ == '__main__':
    main()
