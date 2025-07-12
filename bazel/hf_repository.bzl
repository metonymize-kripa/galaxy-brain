"""Custom Bazel rules for Hugging Face model management."""

def _hf_model_impl(repository_ctx):
    """Implementation function for hf_model repository rule."""
    model_name = repository_ctx.attr.model_name
    model_revision = repository_ctx.attr.model_revision
    cache_dir = repository_ctx.attr.cache_dir or str(repository_ctx.path(".cache"))
    
    # Create the cache directory
    repository_ctx.execute(["mkdir", "-p", cache_dir])
    
    # Download the model using huggingface-hub
    download_script = """
import os
import sys
from huggingface_hub import snapshot_download

try:
    # Download model to cache
    snapshot_download(
        repo_id="{model_name}",
        revision="{model_revision}",
        cache_dir="{cache_dir}",
        local_files_only=False
    )
    print("✅ Downloaded {model_name}@{model_revision}")
except Exception as e:
    print(f"❌ Failed to download {model_name}: {{e}}")
    sys.exit(1)
""".format(
        model_name=model_name,
        model_revision=model_revision,
        cache_dir=cache_dir
    )
    
    # Execute the download
    result = repository_ctx.execute([
        "python3", "-c", download_script
    ])
    
    if result.return_code != 0:
        fail("Failed to download model {}: {}".format(model_name, result.stderr))
    
    # Create BUILD file
    build_content = '''
filegroup(
    name = "model_files",
    srcs = glob(["**/*"]),
    visibility = ["//visibility:public"],
)

py_library(
    name = "{model_name_safe}",
    data = [":model_files"],
    visibility = ["//visibility:public"],
)
'''.format(model_name_safe=model_name.replace("/", "_").replace("-", "_"))
    
    repository_ctx.file("BUILD.bazel", build_content)
    
    # Create a symlink to the actual model files in cache
    repository_ctx.symlink(cache_dir, "cache")

hf_model = repository_rule(
    implementation = _hf_model_impl,
    attrs = {
        "model_name": attr.string(mandatory = True, doc = "Hugging Face model name"),
        "model_revision": attr.string(default = "main", doc = "Model revision/branch"),
        "cache_dir": attr.string(doc = "Custom cache directory"),
    },
    doc = "Downloads and caches a Hugging Face model as a Bazel external repository"
)

def _hf_dataset_impl(repository_ctx):
    """Implementation function for hf_dataset repository rule."""
    dataset_name = repository_ctx.attr.dataset_name
    dataset_revision = repository_ctx.attr.dataset_revision
    cache_dir = repository_ctx.attr.cache_dir or str(repository_ctx.path(".cache"))
    
    # Create the cache directory
    repository_ctx.execute(["mkdir", "-p", cache_dir])
    
    # Download the dataset using datasets library
    download_script = """
import os
import sys
from datasets import load_dataset

try:
    # Download dataset to cache
    dataset = load_dataset(
        "{dataset_name}",
        revision="{dataset_revision}",
        cache_dir="{cache_dir}"
    )
    print("✅ Downloaded dataset {dataset_name}@{dataset_revision}")
except Exception as e:
    print(f"❌ Failed to download dataset {dataset_name}: {{e}}")
    sys.exit(1)
""".format(
        dataset_name=dataset_name,
        dataset_revision=dataset_revision,
        cache_dir=cache_dir
    )
    
    # Execute the download
    result = repository_ctx.execute([
        "python3", "-c", download_script
    ])
    
    if result.return_code != 0:
        fail("Failed to download dataset {}: {}".format(dataset_name, result.stderr))
    
    # Create BUILD file
    build_content = '''
filegroup(
    name = "dataset_files",
    srcs = glob(["**/*"]),
    visibility = ["//visibility:public"],
)

py_library(
    name = "{dataset_name_safe}",
    data = [":dataset_files"],
    visibility = ["//visibility:public"],
)
'''.format(dataset_name_safe=dataset_name.replace("/", "_").replace("-", "_"))
    
    repository_ctx.file("BUILD.bazel", build_content)
    
    # Create a symlink to the actual dataset files in cache
    repository_ctx.symlink(cache_dir, "cache")

hf_dataset = repository_rule(
    implementation = _hf_dataset_impl,
    attrs = {
        "dataset_name": attr.string(mandatory = True, doc = "Hugging Face dataset name"),
        "dataset_revision": attr.string(default = "main", doc = "Dataset revision/branch"),
        "cache_dir": attr.string(doc = "Custom cache directory"),
    },
    doc = "Downloads and caches a Hugging Face dataset as a Bazel external repository"
)