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
module: buildah_commit
version_added: 0.0.1
short_description:  buildah-commit - Create an image from a working container.

description: >
  Create an image from a working container. Writes a new image using the specified
  container's read-write layer and if it is based on an image, the layers of that
  image. If image does not begin with a registry name component, localhost will be
  added to the name.

options:
  container:
    description: container ID
    type: str
    required: true
  imgname:
    description: newImageName
    type: str
    required: true
  authfile:
    description: path of the authentication file.
    type: path
    required: false
  certdir:
    description: use certificates at the specified path to access the registry.
    type: path
    required: false
  creds:
    description: use [username[:password]] for accessing the registry.
    type: str
    required: false
  compression:
    description: use compression.
    type: bool
    default: false
  format:
    description: format of the image manifest and metadata (default "oci")
    type: str
    default: oci
    choices:
      - oci
      - docker
  iidfile:
    description: write the image ID to the file
    type: path
    required: false
  quiet:
    description: don't output progress information when writing images
    type: bool
    default: false
  rm:
    description: remove the container and its content after committing it to an image.
    type: bool
    default: false
  squash:
    description: produce an image with only one layer.
    type: bool
    default: false
  tls_verify:
    description: require HTTPS and verify certificates when accessing the registry.
    type: bool
    default: false

# informational: requirements for nodes
requirements: [ buildah ]

author:
  - Red Hat Consulting (NAPS) (!UNKNOWN)
  - Lester Claudio (@claudiol)
'''

EXAMPLES = '''
- name: BUILDAH | Test output of "buildah add --noheading <image_name>" command
  buildah_commit:
    container: fedora-working-container
    imgname: docker://localhost:5000/fedora-claudiol
    creds: username:password
    heading: false
  register: result

- debug: var=result.stdout_lines
'''


def buildah_commit(module, container, imgname, authfile, certdir,
                   creds, compression, format, iidfile, quiet, rm,
                   squash, tls_verify):

    if module.get_bin_path('buildah'):
        buildah_bin = module.get_bin_path('buildah')
        buildah_basecmd = [buildah_bin, 'commit']

    if authfile:
        r_cmd = ['--authfile']
        buildah_basecmd.extend(r_cmd)
        r_cmd = [authfile]
        buildah_basecmd.extend(r_cmd)

    if certdir:
        r_cmd = ['--cert-dir']
        buildah_basecmd.extend(r_cmd)
        r_cmd = [certdir]
        buildah_basecmd.extend(r_cmd)

    if creds:
        r_cmd = ['--creds']
        buildah_basecmd.extend(r_cmd)
        r_cmd = [creds]
        buildah_basecmd.extend(r_cmd)

    if compression:
        r_cmd = ['--disable-compression']
        buildah_basecmd.extend(r_cmd)

    if format:
        r_cmd = ['--format']
        buildah_basecmd.extend(r_cmd)
        r_cmd = [format]
        buildah_basecmd.extend(r_cmd)

    if iidfile:
        r_cmd = ['--iidfile']
        buildah_basecmd.extend(r_cmd)
        r_cmd = [iidfile]
        buildah_basecmd.extend(r_cmd)

    if quiet:
        r_cmd = ['--quiet']
        buildah_basecmd.extend(r_cmd)

    if rm:
        r_cmd = ['--rm']
        buildah_basecmd.extend(r_cmd)

    if container:
        r_cmd = [container]
        buildah_basecmd.extend(r_cmd)

    if imgname:
        r_cmd = [imgname]
        buildah_basecmd.extend(r_cmd)

    return module.run_command(buildah_basecmd)


def main():

    module = AnsibleModule(
        argument_spec=dict(
            container=dict(required=True),
            imgname=dict(required=True),
            authfile=dict(required=False, type='path'),
            certdir=dict(required=False, type='path'),
            creds=dict(required=False),
            compression=dict(required=False, default='no', type='bool'),
            format=dict(required=False, default='oci', choices=['oci', 'docker']),
            iidfile=dict(required=False, type='path'),
            quiet=dict(required=False, default="no", type="bool"),
            rm=dict(required=False, default="no", type="bool"),
            squash=dict(required=False, default="no", type="bool"),
            tls_verify=dict(required=False, default="no", type="bool")
        ),
        supports_check_mode=True
    )

    params = module.params

    container = params.get('container', '')
    imgname = params.get('imgname', '')
    authfile = params.get('authfile', '')
    certdir = params.get('certdir', '')
    creds = params.get('creds', '')
    compression = params.get('compression', '')
    format = params.get('format', '')
    iidfile = params.get('iidfile', '')
    quiet = params.get('quiet', '')
    rm = params.get('rm', '')
    signature_policy = params.get('signature_policy', '')
    squash = params.get('squash', '')
    tls_verify = params.get('tls_verify', '')

    rc, out, err = buildah_commit(module, container, imgname, authfile, certdir, creds,
                                  compression, format, iidfile, quiet, rm, signature_policy,
                                  squash, tls_verify)

    if rc == 0:
        module.exit_json(changed=True, rc=rc, stdout=out, err=err)
    else:
        module.fail_json(msg=err)  # changed=False, rc=rc, stdout=out, err=err)


# import module snippets
from ansible.module_utils.basic import AnsibleModule
# from ansible.module_utils.urls import *
if __name__ == '__main__':
    main()
