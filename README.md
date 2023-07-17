# act kaniko

This action builds and pushes a docker image using [kaniko](https://github.com/GoogleContainerTools/kaniko)

> This actions only tests on gitea, May not work on github


## Example

```yaml

name: CI
run-name: ${{ gitea.actor }} is running build

on:
  push:
    branches:
      - master

jobs:
  build-image:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v3
        with:
          fetch-depth: 1
          clean: true

      - name: Build image
        uses: yinheli/act-kaniko@v1
        with:
          image: harbor.example.com/app/demo

```
