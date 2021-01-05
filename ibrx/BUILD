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
        "//ibrx/mess:message",
        "//ibrx/mess:message_wrapper",
        "//ibrx/mess/messages:account_summary",
        "//ibrx/mess/messages:open_orders",
        "//ibrx/mess/messages:position",
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
