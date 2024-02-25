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
module: buildah_push
version_added: 0.0.1
short_description: Pushes an image from local storage to a specified destination, decompressing and recompessing layers as needed.
description:
     - Pushes an image from local storage to a specified destination, decompressing and recompessing layers as needed.

options:
  name:
    description: imageID
    type: str
    required: true
  dest:
    description: destination
    type: str
  authfile:
    description: path of the authentication file
    type: path
  cert_dir:
    description: use certificates at the specified path to access the registry
    type: path
  creds:
    description: use [username[:password]] for accessing the registry
    type: str
  quiet:
    description: don't output progress information when pushing images
    type: bool
    default: false
  tls_verify:
    description: require HTTPS and verify certificates when accessing the registry
    type: bool
    default: false

# informational: requirements for nodes
requirements: [ buildah ]
author:
  - Red Hat Consulting (NAPS) (!UNKNOWN)
  - Lester Claudio (@claudiol)
'''

EXAMPLES = '''
- name: BUILDAH | Test output of "buildah push <image_name>" command
  buildah_push:
    name: IMAGE
    quiet: true
  register: result

- debug: var=result.stdout_lines
'''


def buildah_push(module, name, dest, authfile, cert_dir, creds, quiet, signature_policy, tls_verify):

    if module.get_bin_path('buildah'):
        buildah_bin = module.get_bin_path('buildah')
        buildah_basecmd = [buildah_bin, 'push']

    if authfile:
        r_cmd = ['--authfile']
        buildah_basecmd.extend(r_cmd)
        r_cmd = [authfile]
        buildah_basecmd.extend(r_cmd)

    if cert_dir:
        r_cmd = ['--cert_dir']
        buildah_basecmd.extend(r_cmd)
        r_cmd = [cert_dir]
        buildah_basecmd.extend(r_cmd)

    if creds:
        r_cmd = ['--creds']
        buildah_basecmd.extend(r_cmd)
        r_cmd = [creds]
        buildah_basecmd.extend(r_cmd)

    if signature_policy:
        r_cmd = ['--signature_policy']
        buildah_basecmd.extend(r_cmd)
        r_cmd = [signature_policy]
        buildah_basecmd.extend(r_cmd)

    if tls_verify:
        r_cmd = ['--tls_verify']
        buildah_basecmd.extend(r_cmd)

    if quiet:
        r_cmd = ['--quiet']
        buildah_basecmd.extend(r_cmd)

    if name:
        r_cmd = [name]
        buildah_basecmd.extend(r_cmd)

    if dest:
        r_cmd = [dest]
        buildah_basecmd.extend(r_cmd)

    return module.run_command(buildah_basecmd)


def main():

    module = AnsibleModule(
        argument_spec=dict(
            name=dict(required=True),
            dest=dict(required=False),
            authfile=dict(required=False, type='path'),
            cert_dir=dict(required=False, type='path'),
            creds=dict(required=False),
            quiet=dict(required=False, default="no", type="bool"),
            tls_verify=dict(required=False, default="no", type="bool")
        ),
        supports_check_mode=True
    )

    params = module.params

    name = params.get('name', '')
    dest = params.get('dest', '')
    authfile = params.get('authfile', '')
    cert_dir = params.get('cert_dir', '')
    creds = params.get('creds', '')
    quiet = params.get('creds', '')
    signature_policy = params.get('signature_policy', '')
    tls_verify = params.get('tls_verify', '')

    rc, out, err = buildah_push(module, name, dest, authfile, cert_dir, creds, quiet, signature_policy, tls_verify)

    if rc == 0:
        module.exit_json(changed=True, rc=rc, stdout=out, err=err)
    else:
        module.fail_json(msg=err)


# import module snippets
from ansible.module_utils.basic import AnsibleModule
if __name__ == '__main__':
    main()
