# -*- coding: utf-8 -*-

import os
import subprocess

def get_var(name, default_val = '',):
    return os.environ.get(f'INPUT_{name}'.upper(), default_val)

cmd = f"docker run --rm -v {os.environ.get('JOB_CONTAINER_NAME')}:/workspace -v /data/cache:/cache"

dockerconfig_dir = get_var('dockerconfig-dir', '/.docker')
cmd += f" -v {dockerconfig_dir}:/kaniko/.docker"

cmd += f" gcr.io/kaniko-project/executor:v1.12.1"

context = os.path.join('/workspace', get_var('context'))
cmd += f" --context=dir://{context}"

cmd += f" --dockerfile={get_var('dockerfile', 'Dockerfile')}"

destination = get_var('destination').split(',')
image = get_var('image')
if image:
    destination = []
    ref_name = os.environ.get('GITHUB_REF_NAME')
    ref_type = os.environ.get('GITHUB_REF_TYPE')
    for i in image.split(','):
        i = i.strip()
        tag = ref_name
        if ref_type == 'branch':
            destination.append(f'{i}:latest')
            tag = ref_name.replace('/', '-')
            if len(tag) > 16:
                tag = tag[:16]
        tag = tag.strip('-')
        destination.append(f'{i}:{tag}')
for d in destination:
    if d:
        cmd += f" --destination={d}"

build_args = get_var('build-args')
if build_args:
    cmd += f" --build-arg={build_args}"

if get_var('insecure', 'false') == 'true':
    cmd += " --insecure"

if get_var('insecure-pull', 'false') == 'true':
    cmd += " --insecure-pull"

insecure_registry = get_var('insecure-registry')
if insecure_registry:
    for x in insecure_registry.split(','):
        cmd += f" --insecure-registry={x}"

label = get_var('label')
if label:
    for x in label.split(','):
        cmd += f" --label={x}"

if get_var('no-push', 'false') == 'true':
    cmd += " --no-push"

if get_var('skip-tls-verify', 'false') == 'true':
    cmd += " --skip-tls-verify"

if get_var('skip-tls-verify-pull', 'false') == 'true':
    cmd += " --skip-tls-verify-pull"

if get_var('skip-unused-stages', 'true') == 'true':
    cmd += " --skip-unused-stages"

if get_var('cache', 'false') == 'true':
    cmd += " --cache=true"
    cache_repo = get_var('cache-repo')
    if cache_repo:
        cmd += f" --cache-repo={cache_repo}"
        cmd += " --cache-copy-layers"
        cmd += " --cache-run-layers"
        cmd += " --compressed-caching=false"
else:
    cmd += " --cache=false"

registry_mirror = get_var('registry-mirror').split(',')
if registry_mirror:
    for r in registry_mirror:
        if r:
            cmd += f" --registry-mirror={r}"

cmd += " --image-fs-extract-retry=3"

print(cmd)

ret = subprocess.run(cmd, shell=True)
exit(ret.returncode)
