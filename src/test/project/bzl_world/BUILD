load("@rules_cc//cc:defs.bzl", "cc_library")

cc_library(
    name = "world",
    srcs = ["src/world.cpp"],
    hdrs = [
        "include/world/world.hpp",
    ],
    includes = ["include"],
    linkstatic = True,
    visibility = ["//visibility:public"],
    deps = [
        "@boost.container",
    ],
)
