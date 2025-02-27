# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os

from spack.package import *


class EcmwfAtlas(CMakePackage):
    """A library for numerical weather prediction and climate modelling."""

    homepage = "https://software.ecmwf.int/wiki/display/atlas"
    git = "https://github.com/ecmwf/atlas.git"
    url = "https://github.com/ecmwf/atlas/archive/0.22.1.tar.gz"

    maintainers = ["climbfuji", "srherbener"]

    version("master", branch="master")
    version("develop", branch="develop")
    version("0.33.0", sha256="a91fffe9cecb51c6ee8549cbc20f8279e7b1f67dd90448e6c04c1889281b0600")
    version("0.32.1", sha256="3d1a46cb7f50e1a6ae9e7627c158760e132cc9f568152358e5f78460f1aaf01b")
    version("0.31.1", sha256="fa9274c74c40c2115b9c6120a7040e357b0c7f37b20b601b684d2a83a479cdfb")
    version("0.31.0", sha256="fa4ff8665544b8e19f79d171c540a9ca8bfc4127f52a3c4d4d618a2fe23354d7")

    depends_on("ecbuild", type=("build"))
    depends_on("eckit")
    depends_on("boost cxxstd=14 visibility=hidden", when="@0.26.0:", type=("build", "run"))
    variant("fckit", default=True)
    depends_on("fckit", when="+fckit")
    depends_on("python")

    patch("clang_include_array.patch", when="%apple-clang")
    patch("clang_include_array.patch", when="%clang")
    patch("intel_vectorization.patch", when="%intel")

    variant(
        "build_type",
        default="RelWithDebInfo",
        description="CMake build type",
        values=("Debug", "Release", "RelWithDebInfo"),
    )

    variant('openmp', default=True, description='Use OpenMP?')
    depends_on("llvm-openmp", when="+openmp %apple-clang", type=("build", "run"))
    variant("shared", default=True)

    variant("trans", default=False)
    depends_on("ectrans@:1.0.0", when="@:0.30.0 +trans")
    depends_on("ectrans@1.1.0:", when="@0.31.0: +trans")
    # variant('cgal', default=False)
    # depends_on('cgal', when='+cgal')
    variant("eigen", default=True)
    depends_on("eigen", when="+eigen")
    variant("fftw", default=True)
    depends_on("fftw-api", when="+fftw")

    variant("fismahigh", default=False, description="Apply patching for FISMA-high compliance")

    def cmake_args(self):
        args = [
            self.define_from_variant('ENABLE_OMP', 'openmp'),
            self.define_from_variant("ENABLE_FCKIT", "fckit"),
            self.define_from_variant("ENABLE_TRANS", "trans"),
            self.define_from_variant("ENABLE_EIGEN", "eigen"),
            self.define_from_variant("ENABLE_FFTW", "fftw"),
            "-DPYTHON_EXECUTABLE:FILEPATH=" + self.spec["python"].command.path,
        ]
        if "~shared" in self.spec:
            args.append("-DBUILD_SHARED_LIBS=OFF")
        return args

    @when("+fismahigh")
    def patch(self):
        filter_file("http://www\.ecmwf\.int", "", "cmake/atlas-import.cmake.in")
        filter_file("int\.ecmwf", "", "cmake/atlas-import.cmake.in")
        filter_file('http[^"]+', "", "cmake/atlas_export.cmake")
        patterns = [".travis.yml", "tools/install*.sh", "tools/github-sha.sh"]
        for pattern in patterns:
            paths = glob.glob(pattern)
            for path in paths:
                os.remove(path)
