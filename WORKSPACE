workspace(name = "ibrx")

load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

http_archive(
    name = "rules_python",
    sha256 = "140630a11671b4a5b5e3f1031ff6a8e63c0740dded9c38af9fad49cf6fad00c1",
    strip_prefix = "rules_python-a16432752ef33b98530f05ca86375b42059b23c0",
    urls = [
        "https://github.com/bazelbuild/rules_python/archive/a16432752ef33b98530f05ca86375b42059b23c0.zip",
    ],
)

register_toolchains("//:py_toolchain")

# ================================================================
# Python extensions
# ================================================================
load("@rules_python//python:pip.bzl", "pip_install")

pip_install(
    name = "py_deps",
    requirements = "//:requirements.txt",
)

