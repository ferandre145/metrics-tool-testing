# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

import os


class Ewok(PythonPackage):
    """Experiments and Workflows Orchestration Kit (EWOK) - DH* NEED TO FILL IN THE DETAILS
    """

    homepage = "https://github.com/JCSDA/ewok"
    git = "https://github.com/JCSDA/ewok.git"
    url = "https://github.com/JCSDA/ewok/archive/refs/tags/1.0.0.tar.gz"

    maintainers = ['climbfuji', 'ericlingerfelt']

    version('develop', branch='develop', no_cache=True)
    version('0.0.1', commit='69fff0f460fdb639db4fd38574dee8262b8a1f84', preferred=True)

    depends_on('python@3.7:',         type=('build', 'run'))
    depends_on('py-pyyaml',           type=('build', 'run'))
    depends_on('py-jinja2',           type=('build', 'run'))
    depends_on('py-ruamel-yaml',      type=('build', 'run'))
    depends_on('py-ruamel-yaml-clib', type=('build', 'run'))
    depends_on('py-shapely@1.8.0',    type=('build', 'run'))
    depends_on('py-cartopy+plotting', type=('build', 'run'))
