load("@rules_python//python:defs.bzl", "py_library", "py_test")
load("@py_deps//:requirements.bzl", "requirement")

package(default_visibility = ["//ibrx:internal"])

py_library(
    name = "account_summary",
    srcs = ["account_summary.py"],
    srcs_version = "PY3",
    deps = [
        "//ibrx/mess:message",
        requirement("ibapi"),
        requirement("rx"),
    ],
)

py_test(
    name = "account_summary_test",
    srcs = ["account_summary_test.py"],
    srcs_version = "PY3",
    deps = [
        ":account_summary",
        requirement("ibapi"),
        requirement("pyhamcrest"),
        requirement("rx"),
    ],
)

py_library(
    name = "position",
    srcs = ["position.py"],
    srcs_version = "PY3",
    deps = [
        "//ibrx/mess:message",
        requirement("ibapi"),
        requirement("rx"),
    ],
)

py_test(
    name = "position_test",
    srcs = ["position_test.py"],
    srcs_version = "PY3",
    deps = [
        ":position",
        requirement("ibapi"),
        requirement("pyhamcrest"),
        requirement("rx"),
    ],
)
