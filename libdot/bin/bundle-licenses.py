#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2018 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Produce a bundle of the license files of all NPM prod dependencies.

The output contains both escaped and real line breaks, which makes it suitable
for use by libdot/bin/concat. A warning is emitted if a package does not provide
one of the common types of license files.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from html import escape
import json
import os
import subprocess
import sys

LICENSE_FILES = ['LICENSE', 'license', 'LICENCE', 'licence',
                 'LICENSE-MIT', 'LICENCE-MIT', 'COPYING', 'copying']


def get_paths():
    """Use npm ls to get the paths of all production dependencies."""
    npm = os.path.abspath(os.path.join(os.path.dirname(__file__), 'npm'))
    pathsBytes = subprocess.run(
        [npm, 'ls', '--prod', '--parse'],
        stdout=subprocess.PIPE,
        cwd=os.path.dirname(__file__)).stdout
    lines = pathsBytes.decode('utf-8').splitlines()
    return [line for line in lines if line]


def scan_package(path, licenses):
    """Add a license file for a package under a given path to the bundle."""
    info_path = os.path.join(path, 'package.json')
    if not os.path.isfile(info_path):
        print('\033[91mERROR: Directory is not a node package: {}\033[0m'
              .format(path))
        sys.exit(1)
    package_info = {}
    with open(info_path, 'r') as package_file:
        package_info = json.load(package_file)
    identifier = '{}@{}'.format(package_info['name'], package_info['version'])
    if identifier not in licenses:
        license_text = find_license(path)
        if not license_text:
            print('\033[93mWARNING: Does not provide a license file: {}\033[0m'
                  .format(identifier))
        else:
            licenses[identifier] = license_text


def find_license(path):
    """Try to find a license file with a common name in a given path."""
    for license_file in LICENSE_FILES:
        license_path = os.path.join(path, license_file)
        if os.path.isfile(license_path):
            with open(license_path, 'r') as file:
                return file.read()
    return None


def scan_paths(paths, licenses):
    for path in paths:
        scan_package(path, licenses)


def bundle_licenses(licenses, out_file):
    """Bundle up all licenses in an HTML file."""
    output = ('<!DOCTYPE html>\n'
              '<html>\n'
              '<head>\n'
              '<title>Secure Shell - Open Source Licenses</title>\n'
              '</head>\n'
              '<body>\n'
              '<h1>Secure Shell - Open Source Licenses</h1>\n')
    for identifier in sorted(licenses):
        output += '<h2>{}</h2>\n'.format(escape(identifier))
        output += ('<pre>\n{}</pre>\n'
                   .format(escape(licenses[identifier])))
    output += ('</body>\n'
               '</html>')
    with open(out_file, 'w') as out:
        out.write(output)


def usage():
    print('Bundle license files for all NPM dependencies.')
    print('')
    print('Usage:')
    print('        {} licenses.txt'.format(sys.argv[0]))


def main():
    if len(sys.argv) != 2:
        usage()
        return

    paths = get_paths()
    licenses = {}
    scan_paths(paths, licenses)
    bundle_licenses(licenses, sys.argv[1])


if __name__ == '__main__':
    main()
