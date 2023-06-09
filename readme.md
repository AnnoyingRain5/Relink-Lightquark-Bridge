# Lightquark <-> Relink Bridge
[![forthebadge](https://forthebadge.com/images/badges/powered-by-electricity.svg)](https://forthebadge.com) [![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com) [![forthebadge](https://forthebadge.com/images/badges/you-didnt-ask-for-this.svg)](https://forthebadge.com)

This is a bridge between the Lightquark chat service and the Relink chat service. 

## Configuration:
This bridge can be configured by providing the environment variables documented in the `.env.example` file. You can either provide these in the environment directly, or by providing a `.env` file, such as by modifying and renaming the example file.

## Proxy Support:
Due to [WS#364](https://github.com/python-websockets/websockets/issues/364) and [WS#475](https://github.com/python-websockets/websockets/issues/475),
connecting to a server over a proxy is not supported.

## Submodule note:
This repository has git submodules, to clone them, use the `--recurse-submodules` flag, or run `git submodule update --init --recursive` after cloning.

## Setup:
You will need python 3.10 or newer to run this bridge.

You can then install the required dependencies by running `pip install -r requirements.txt`.
