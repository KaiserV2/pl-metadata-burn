#
# metadata_burn ds ChRIS plugin app
#
# (c) 2022 Fetal-Neonatal Neuroimaging & Developmental Science Center
#                   Boston Children's Hospital
#
#              http://childrenshospital.org/FNNDSC/
#                        dev@babyMRI.org
#

from chrisapp.base import ChrisApp
import csv
import json
import os
from PIL import Image
from PIL import ImageColor
from PIL import ImageDraw
from PIL import ImageFont
import subprocess

Gstr_title = r"""
                _            _       _          _
               | |          | |     | |        | |
 _ __ ___   ___| |_ __ _  __| | __ _| |_ __ _  | |__  _   _ _ __ _ __
| '_ ` _ \ / _ \ __/ _` |/ _` |/ _` | __/ _` | | '_ \| | | | '__| '_ \
| | | | | |  __/ || (_| | (_| | (_| | || (_| | | |_) | |_| | |  | | | |
|_| |_| |_|\___|\__\__,_|\__,_|\__,_|\__\__,_| |_.__/ \__,_|_|  |_| |_|
                                           ______
                                          |______|
"""

Gstr_synopsis = """

(Edit this in-line help for app specifics. At a minimum, the
flags below are supported -- in the case of DS apps, both
positional arguments <inputDir> and <outputDir>; for FS and TS apps
only <outputDir> -- and similarly for <in> <out> directories
where necessary.)

    NAME

       metadata_burn

    SYNOPSIS

        docker run --rm fnndsc/pl-metadata-burn metadata_burn                     \\
            [-h] [--help]                                               \\
            [--json]                                                    \\
            [--man]                                                     \\
            [--meta]                                                    \\
            [--savejson <DIR>]                                          \\
            [-v <level>] [--verbosity <level>]                          \\
            [--version]                                                 \\
            <inputDir>                                                  \\
            <outputDir>

    BRIEF EXAMPLE

        * Bare bones execution

            docker run --rm -u $(id -u)                             \
                -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing      \
                fnndsc/pl-metadata-burn metadata_burn                        \
                /incoming /outgoing

    DESCRIPTION

        `metadata_burn` ...

    ARGS

        [-h] [--help]
        If specified, show help message and exit.

        [--json]
        If specified, show json representation of app and exit.

        [--man]
        If specified, print (this) man page and exit.

        [--meta]
        If specified, print plugin meta data and exit.

        [--savejson <DIR>]
        If specified, save json representation file to DIR and exit.

        [-v <level>] [--verbosity <level>]
        Verbosity level for app. Not used currently.

        [--version]
        If specified, print version number and exit.
"""


class Metadata_burn(ChrisApp):
    """
    An app to add metadata to a PNG image
    """

    PACKAGE = __package__
    TITLE = "Metadata Burn"
    CATEGORY = ""
    TYPE = "ds"
    ICON = ""  # url of an icon image
    MIN_NUMBER_OF_WORKERS = 1  # Override with the minimum number of workers as int
    MAX_NUMBER_OF_WORKERS = 1  # Override with the maximum number of workers as int
    MIN_CPU_LIMIT = (
        2000  # Override with millicore value as int (1000 millicores == 1 CPU core)
    )
    MIN_MEMORY_LIMIT = 8000  # Override with memory MegaByte (MB) limit as int
    MIN_GPU_LIMIT = 0  # Override with the minimum number of GPUs as int
    MAX_GPU_LIMIT = 0  # Override with the maximum number of GPUs as int

    # Use this dictionary structure to provide key-value output descriptive information
    # that may be useful for the next downstream plugin. For example:
    #
    # {
    #   "finalOutputFile":  "final/file.out",
    #   "viewer":           "genericTextViewer",
    # }
    #
    # The above dictionary is saved when plugin is called with a ``--saveoutputmeta``
    # flag. Note also that all file paths are relative to the system specified
    # output directory.
    OUTPUT_META_DICT = {}

    def define_parameters(self):
        """
        Define the CLI arguments accepted by this plugin app.
        Use self.add_argument to specify a new app argument.
        """
        self.add_argument(
            "-a",
            "--align",
            dest="align",
            default="left",
            optional=True,
            type=str,
            help="Alignment of text lines",
        )
        self.add_argument(
            "-c",
            "--color",
            dest="color",
            default="white",
            optional=True,
            type=str,
            help="Color name of text to use",
        )
        self.add_argument(
            "-f",
            "--fields-to-burn",
            dest="fields",
            default="PatientName, PatientID, PatientBirthDate, PatientPosition",
            optional=True,
            type=str,
            help="Comma separated fields to burn into final PNG",
        )
        self.add_argument(
            "-o",
            "--opacity",
            dest="opacity",
            default=255,
            optional=True,
            type=int,
            help="Opacity of text. Full opacity is 255, lowering this number wil decrease text opacity",
        )
        self.add_argument(
            "-q",
            "--quadrant",
            dest="quadrant",
            default="bottom-right",
            choices=["top-right", "top-left", "bottom-right", "bottom-left"],
            optional=True,
            type=str,
            help="Quadrant to place text",
        )
        self.add_argument(
            "-t",
            "--text-size",
            dest="size",
            default=25,
            optional=True,
            type=int,
            help="Size of text as a percent of the image size",
        )

    def run(self, options):
        """
        Define the code to be run by this plugin app.
        """
        print(Gstr_title)
        print("Version: %s" % self.get_version())

        for file in os.listdir(options.inputdir):
            input_file = os.path.join(options.inputdir, file)
            subprocess.run(
                [
                    "med2image",
                    f"--inputFile={input_file}",
                    f"--outputDir=/tmp/{file}",
                    "--outputFileType=png",
                    f"--outputFileStem={file.rsplit('.', 1)[0]}",
                ],
                check=True,
            )
            print(f"Image {file} converted")

            subprocess.run(
                [
                    "pfdicom_tagExtract",
                    f"--inputDir={options.inputdir}",
                    f"--inputFile={file}",
                    f"--outputDir=/tmp/{file}",
                    "--outputFileStem=metadata",
                    "--outputFileType=json",
                ],
                check=True,
            )
            f = open(f"/tmp/{file}/metadata.json")
            metadata = json.load(f)
            f.close()
            print("Metadata processed")

            # Commence the burn
            for converted_file in os.listdir(f"/tmp/{file}"):
                if converted_file == "metadata.json":
                    break
                img = Image.open(f"/tmp/{file}/{converted_file}")
                burn_string = ""
                for field in options.fields.split(","):
                    burn_string = (
                        f"{burn_string}{field}: {metadata[field.strip()]}\n".strip(" ")
                    )
                draw = ImageDraw.Draw(img)
                fill = ImageColor.getrgb(options.color) + (options.opacity,)
                font_size: int = 4
                img_size = img.size
                font = ImageFont.truetype(
                    font="/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
                    size=font_size,
                )
                while draw.multiline_textsize(burn_string, font=font)[0] < (
                    (options.size / 100) * img_size[0]
                ):
                    font_size += 1
                    font = ImageFont.truetype(
                        font="/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
                        size=font_size,
                    )
                test = draw.multiline_textsize(burn_string, font=font)
                if options.quadrant == "bottom-right":
                    x = img_size[0] - test[0]
                    y = img_size[1] - test[1]
                elif options.quadrant == "top-right":
                    x = img_size[0] - test[0]
                    y = 2
                elif options.quadrant == "top-left":
                    x = 2
                    y = 2
                else:
                    x = 2
                    y = img_size[1] - test[1]
                draw.multiline_text(
                    (x, y), burn_string, fill=fill, font=font, align=options.align
                )
                img.save(os.path.join(options.outputdir, converted_file))
            print(f"File {file} successfully converted and marked")

    def show_man_page(self):
        """
        Print the app's man page.
        """
        print(Gstr_synopsis)
