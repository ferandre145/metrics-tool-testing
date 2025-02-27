# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class PyCython(PythonPackage):
    """The Cython compiler for writing C extensions for the Python language."""

    homepage = "https://github.com/cython/cython"
    pypi = "cython/Cython-0.29.21.tar.gz"

    version("3.0.0a9", sha256="23931c45877432097cef9de2db2dc66322cbc4fc3ebbb42c476bb2c768cecff0")
    version(
        "0.29.32",
        sha256="8733cf4758b79304f2a4e39ebfac5e92341bce47bcceb26c1254398b2f8c1af7",
        preferred=True,
    )
    version("0.29.30", sha256="2235b62da8fe6fa8b99422c8e583f2fb95e143867d337b5c75e4b9a1a865f9e3")
    version("0.29.24", sha256="cdf04d07c3600860e8c2ebaad4e8f52ac3feb212453c1764a49ac08c827e8443")
    version("0.29.23", sha256="6a0d31452f0245daacb14c979c77e093eb1a546c760816b5eed0047686baad8e")
    version("0.29.22", sha256="df6b83c7a6d1d967ea89a2903e4a931377634a297459652e4551734c48195406")
    version("0.29.21", sha256="e57acb89bd55943c8d8bf813763d20b9099cc7165c0f16b707631a7654be9cad")
    version("0.29.20", sha256="22d91af5fc2253f717a1b80b8bb45acb655f643611983fd6f782b9423f8171c7")
    version("0.29.16", sha256="232755284f942cbb3b43a06cd85974ef3c970a021aef19b5243c03ee2b08fa05")
    version("0.29.15", sha256="60d859e1efa5cc80436d58aecd3718ff2e74b987db0518376046adedba97ac30")
    version("0.29.14", sha256="e4d6bb8703d0319eb04b7319b12ea41580df44fd84d83ccda13ea463c6801414")
    version("0.29.13", sha256="c29d069a4a30f472482343c866f7486731ad638ef9af92bfe5fca9c7323d638e")
    version("0.29.10", sha256="26229570d6787ff3caa932fe9d802960f51a89239b990d275ae845405ce43857")
    version("0.29.7", sha256="55d081162191b7c11c7bfcb7c68e913827dfd5de6ecdbab1b99dab190586c1e8")
    version("0.29.5", sha256="9d5290d749099a8e446422adfb0aa2142c711284800fb1eb70f595101e32cbf1")
    version("0.29", sha256="94916d1ede67682638d3cc0feb10648ff14dc51fb7a7f147f4fedce78eaaea97")
    version("0.28.6", sha256="68aa3c00ef1deccf4dd50f0201d47c268462978c12c42943bc33dc9dc816ac1b")
    version("0.28.3", sha256="1aae6d6e9858888144cea147eb5e677830f45faaff3d305d77378c3cba55f526")
    version("0.28.1", sha256="152ee5f345012ca3bb7cc71da2d3736ee20f52cd8476e4d49e5e25c5a4102b12")
    version("0.25.2", sha256="f141d1f9c27a07b5a93f7dc5339472067e2d7140d1c5a9e20112a5665ca60306")
    version("0.23.5", sha256="0ae5a5451a190e03ee36922c4189ca2c88d1df40a89b4f224bc842d388a0d1b6")
    version("0.23.4", sha256="fec42fecee35d6cc02887f1eef4e4952c97402ed2800bfe41bbd9ed1a0730d8e")

    depends_on("python@2.7:2,3.4:", when="@3:", type=("build", "link", "run"))
    depends_on("python@2.6:2,3.3:", type=("build", "link", "run"))
    depends_on("py-setuptools", type=("build", "run"))
    depends_on("gdb@7.2:", type="test")

    @property
    def prefix(self):
        prefix = super(PyCython, self).prefix
        if os.path.isdir(os.path.join(prefix, "local", "bin")) and not os.path.isdir(
            os.path.join(prefix, "bin")
        ):
            prefix.bin = os.path.join(prefix, "local", "bin")
        if os.path.isdir(os.path.join(prefix, "local", "lib")) and not os.path.isdir(
            os.path.join(prefix, "lib")
        ):
            prefix.lib = os.path.join(prefix, "local", "lib")
        elif os.path.isdir(os.path.join(prefix, "local", "lib64")) and not os.path.isdir(
            os.path.join(prefix, "lib64")
        ):
            prefix.lib = os.path.join(prefix, "local", "lib64")
        return prefix

    @property
    def command(self):
        """Returns the Cython command"""
        return Executable(self.prefix.bin.cython)

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def build_test(self):
        # Warning: full suite of unit tests takes a very long time
        python("runtests.py", "-j", str(make_jobs))

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.prepend_path("PATH", self.prefix.bin)
        env.prepend_path("LD_LIBRARY_PATH", self.prefix.lib)
