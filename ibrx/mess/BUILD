load("@rules_python//python:defs.bzl", "py_library")
load("@py_deps//:requirements.bzl", "requirement")

package(default_visibility = ["//ibrx:internal"])

py_library(
    name = "message",
    srcs = ["message.py"],
    srcs_version = "PY3",
)

py_library(
    name = "message_wrapper",
    srcs = ["message_wrapper.py"],
    srcs_version = "PY3",
    deps = [
        ":message",
        requirement("ibapi"),
        requirement("overrides"),
        requirement("rx"),
    ],
)
