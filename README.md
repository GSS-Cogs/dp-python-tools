# dpytools

Simple reusable python resources for digital publishing.

## Installation

Follow these steps to install the package on your local machine:

1. **Install the package**

    Open your terminal and run the following command:

    ```bash
    pip install git+https://github.com/GSS-Cogs/dp-python-tools.git
    ```


## Usage

The following clients, helpers etc are availible upon installation of this package.

| Name | Description |
| ----- | ---------------- |
| [Config](./dpytools/config/README.md) | A simple validating configuration class |
**TODO** - all helpers and clients to appear in this list.

The usage instructions please see the readme in the appropriate sub directory, this can also be access by clicking the link in the "name" column above.

## Development

All commits that make it to PR should have black and ruff already ran against them, you can do this via `make fmt` and you can lint via `make lint`.

For a full list of functionality provided by the makefile just run a naked `make`.

### Repository Organization

Each client, helper etc should be a sub directory of `./dpytools`. Separation between these sub codebases should be maintained as much as possible aginst the day where we want to break some or all of these tools out into separate repositories.