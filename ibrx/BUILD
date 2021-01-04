load("@rules_python//python:defs.bzl", "py_binary", "py_library")
load("@py_deps//:requirements.bzl", "requirement")

package(default_visibility = ["//ibrx:internal"])

package_group(
    name = "internal",
    packages = [
        "//ibrx/...",
    ],
)

py_library(
    name = "client",
    srcs = ["client.py"],
    srcs_version = "PY3",
    deps = [
        "//ibrx/mess:message_client",
        "//ibrx/mess:message_wrapper",
        requirement("ibapi"),
        requirement("rx"),
    ],
)

py_binary(
    name = "test_app",
    srcs = ["test_app.py"],
    srcs_version = "PY3",
    deps = [
        ":client",
    ],
)
