pl-metadata-burn
================================

.. image:: https://img.shields.io/docker/v/fnndsc/pl-metadata-burn?sort=semver
    :target: https://hub.docker.com/r/fnndsc/pl-metadata-burn

.. image:: https://img.shields.io/github/license/fnndsc/pl-metadata-burn
    :target: https://github.com/FNNDSC/pl-metadata-burn/blob/master/LICENSE

.. image:: https://github.com/FNNDSC/pl-metadata-burn/workflows/ci/badge.svg
    :target: https://github.com/FNNDSC/pl-metadata-burn/actions


.. contents:: Table of Contents


Abstract
--------

An app to convert a DICOM image to PNGs and marking them with user selectable metadata


Description
-----------


``metadata_burn`` is a *ChRIS ds-type* application that takes in DICOM image files and produces a series of PNGs with a customizable selection of metadata from the DICOM burned in.


Usage
-----

The application is used like any ChRIS app.  You specify a folder holding the original DICOM image and a folder to output to.  You supply flags to change the fields that are burned in, the location and size of them as well as many more options.

.. code::

    podman run --rm -t fnndsc/pl-metadata-burn \
        -v $(pwd)/in:/incoming \
        -v $(pwd)/out:/outgoing \
        --privileged \
        metadata_burn /incoming /outgoing --text-size=15 --quadrant="bottom-left"

    podman run --rm fnndsc/pl-metadata-burn metadata_burn
        [-h|--help]
        [--json] [--man] [--meta]
        [--savejson <DIR>]
        [-v|--verbosity <level>]
        [--version]
        <inputDir> <outputDir>


Arguments
~~~~~~~~~

.. code::

    [-a] [--align]
    Alignment of lines of text in respect to each other.

    [-c] [--color]
    Name of color to use for text.

    [-f] [--fields-to-burn]
    Comma separated fields to burn into final PNG.  Each field is added to the PNGs in the order they are specified.

    [-h] [--help]
    If specified, show help message and exit.

    [--json]
    If specified, show json representation of app and exit.

    [-o] [--opacity]
    Opacity of text. Full opacity is 255, lowering this number wil decrease text opacity.

    [--man]
    If specified, print (this) man page and exit.

    [--meta]
    If specified, print plugin meta data and exit.

    [-q] [--quadrant]
    Where in the final PNGs to place the text.  Can choose from "top-right", "top-left", "bottom-right", "bottom-left".

    [--savejson <DIR>]
    If specified, save json representation file to DIR and exit.

    [-t] [--text-size]
    Size of text on the image as a percent of the final image size.

    [-v <level>] [--verbosity <level>]
    Verbosity level for app. Not used currently.

    [--version]
    If specified, print version number and exit.


Getting inline help is:

.. code:: bash

    podman run --rm fnndsc/pl-metadata-burn metadata_burn --man

Run
~~~

You need to specify input and output directories using the `-v` flag to `podman run`.


.. code:: bash

    podman run --rm -u $(id -u)                             \
        -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing      \
        fnndsc/pl-metadata-burn metadata_burn                        \
        /incoming /outgoing


Development
-----------

Build the podman container:

.. code:: bash

    podman build -t local/pl-metadata-burn .

Run unit tests:

.. code:: bash

    podman run --rm local/pl-metadata-burn nosetests

Examples
--------

.. code:: bash

    podman run --rm -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing --privileged -t local/metadata_burn metadata_burn /incoming /outgoing --text-size 15 -q "bottom-left"

    podman run --rm -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing --privileged -t local/metadata_burn metadata_burn /incoming /outgoing --color=green

    podman run --rm -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing --privileged -t local/metadata_burn metadata_burn /incoming /outgoing --fields-to-burn="PatientPosition"



.. image:: https://raw.githubusercontent.com/FNNDSC/cookiecutter-chrisapp/master/doc/assets/badge/light.png
    :target: https://chrisstore.co
