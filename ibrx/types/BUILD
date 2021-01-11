load("@rules_python//python:defs.bzl", "py_library", "py_test")
load("@py_deps//:requirements.bzl", "requirement")

package(default_visibility = ["//ibrx:internal"])

py_library(
    name = "historical_data",
    srcs = ["historical_data.py"],
    srcs_version = "PY3",
)

py_test(
    name = "historical_data_test",
    srcs = ["historical_data_test.py"],
    srcs_version = "PY3",
    deps = [
        ":historical_data",
        requirement("pyhamcrest"),
    ],
)
