load("@rules_python//python:defs.bzl", "py_library", "py_test")
load("@py_deps//:requirements.bzl", "requirement")

package(default_visibility = ["//ibrx:internal"])

py_library(
    name = "messages",
    srcs = ["__init__.py"],
    srcs_version = "PY3",
    deps = [
        ":account_summary",
        ":historical_data",
        ":open_orders",
        ":position",
    ],
)

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
    name = "historical_data",
    srcs = ["historical_data.py"],
    srcs_version = "PY3",
    deps = [
        "//ibrx/mess:message",
        "//ibrx/types:historical_data",
        requirement("ibapi"),
        requirement("rx"),
    ],
)

py_test(
    name = "historical_data_test",
    srcs = ["historical_data_test.py"],
    srcs_version = "PY3",
    deps = [
        ":historical_data",
        "//ibrx/types:historical_data",
        requirement("ibapi"),
        requirement("pyhamcrest"),
        requirement("rx"),
    ],
)

py_library(
    name = "open_orders",
    srcs = ["open_orders.py"],
    srcs_version = "PY3",
    deps = [
        "//ibrx/mess:message",
        requirement("ibapi"),
        requirement("rx"),
    ],
)

py_test(
    name = "open_orders_test",
    srcs = ["open_orders_test.py"],
    srcs_version = "PY3",
    deps = [
        ":open_orders",
        ":test_utils",
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
        ":test_utils",
        requirement("ibapi"),
        requirement("pyhamcrest"),
        requirement("rx"),
    ],
)

py_library(
    name = "test_utils",
    testonly = True,
    srcs = ["test_utils.py"],
    srcs_version = "PY3",
    deps = [
        requirement("ibapi"),
    ],
)
