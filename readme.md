# LightQuark <-> Relink Bridge
This is a bridge between the LightQuark chat service and the Relink chat service.

## Configuration:
This bridge can be configured by providing the environment variables documented in the `.env.example` file. You can either provide these in the environment directly, or by providing a `.env` file, such as by modifying and renaming the example file.

## Submodule note:
This repository has git submodules, to clone them, use the `--recurse-submodules` flag, or run `git submodule update --init --recursive` after cloning.

## Setup:
You will need python 3.10 or newer to run this bridge.

You can then install the required dependencies by running `pip install -r requirements.txt`.
