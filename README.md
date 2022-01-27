# Kinvolk Docs

A static website for simple pages and documentation, based in Hugo.

## Quickstart

Clone the project and enter its directory.
Use the [project-docs-config-sample.yaml](./project-docs-config-sample.yaml) as
a base for starting your own project's configuration. This will be where things
like the site name, menus, and documents will be configured.

Assuming you create a config file in project project like "myproject/docs/config.yaml", then run:

```bash
./tools/setup.sh /path/to/myproject/docs/config.yaml
```

This will also clone the documentation repos you have set up.
Once the setup is finished, run:

```bash
make run
```

## Preview documentation

It's nice to edit your docs and see how they will be rendered in this website, so
for that we have a preview tool.

```bash
./tools/preview-docs.sh /path/to/myproject/docs/ my-new-version-name
```

And then run the website as usual:

```bash
make run
```

## Deploy on CI

If you want to be build the website and deploy it to Github Pages, you can
reuse the Github Action provided by this project for that purpose.

Here is an example configuration for the Github Action (to set up in the
project whose Github Pages you want to deploy to):

```yaml
name: Build & Publish docs site
on:
  push:
    branches:
    - main
    - master
    paths:
    - 'docs/**'
    - '.github/**'
  workflow_dispatch:
jobs:
  call-build-and-publish-workflow:
    uses: kinvolk/docs/.github/workflows/build-and-publish-to-gh-pages.yaml@main
    with:
      config: ./docs/config.yaml
```

## Code of Conduct

Please refer to the Kinvolk [Code of Conduct](https://github.com/kinvolk/contribution/blob/master/CODE_OF_CONDUCT.md) when participating in this project.

## Contribution practices

The Kinvolk Docs project follows the [Kinvolk Contribution Guidelines](https://github.com/kinvolk/contribution)
which promotes good and consistent contribution practises across Kinvolk's
projects. Before start contributing, please read those guidelines.

# License

Any contributions to the project are accepted under the terms of the project's
license ([Apache 2.0](../LICENSE)).
