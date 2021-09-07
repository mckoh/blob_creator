"""
Core module of Blob Creator

Author: Michael Kohlegger
Date: 2021-09
"""

from os import mkdir, remove
from os.path import isdir, join
from numpy import ceil
from numpy.random import normal, randint
from names import get_first_name
from pandas import DataFrame
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from PIL import Image
from matplotlib import pyplot as plt
from .const import REPLACE_STRING
from .const import MONSTER, WIDTH_MONSTER, HEIGHT_MONSTER
from .const import ALIEN, WIDTH_ALIEN, HEIGHT_ALIEN
from .const import BOY, WIDTH_BOY, HEIGHT_BOY
from .const import MARSIAN, WIDTH_MARSIAN, HEIGHT_MARSIAN
from .const import COLORS

class BlobFactory:
    """BlobFactory class that is used to generate a blob data set.

    Blobs are little monsters that are intended to help you  explaining
    statistical concepts around sampling. A blob population can be large
    or small. The size is adjustable by the parameter n (default is 5).
    You can also adjust the population's variability by adjusting the
    parameter scatter (default is 12; possible values are 1 to 12).

    :param n: The size of the dataset
    :param scatter: The variability of the data that are generated
    :param export_png: A switch that lets you export the original pngs
    :param cols: The number of columns to be used for plotting
    :param monster: Lets you select a monster template
    """

    def __init__(self,
                 n=5,
                 scatter=12,
                 kind="alien") -> None:

        allowed = ["alien", "monster", "boy", "marsian"]

        assert scatter <= 12, "Scatter cannot be larger than 12"
        assert n > 0, "n must be positive"
        assert kind in allowed, "Kind can only be " + "/".join(allowed)
        assert isinstance(n, int), "n must be int"
        assert isinstance(scatter, int), "scatter must be int"

        self._n = n
        self._scatter = scatter
        self._population = {
            "blobs": [],
            "sizes": [],
            "scales": []
        }
        self._df = None

        if kind == "alien":
            self._kind = ALIEN
            self._kind_w = WIDTH_ALIEN
            self._kind_h = HEIGHT_ALIEN

        elif kind == "monster":
            self._kind = MONSTER
            self._kind_w = WIDTH_MONSTER
            self._kind_h = HEIGHT_MONSTER

        elif kind == "boy":
            self._kind = BOY
            self._kind_w = WIDTH_BOY
            self._kind_h = HEIGHT_BOY

        elif kind == "marsian":
            self._kind = MARSIAN
            self._kind_w = WIDTH_MARSIAN
            self._kind_h = HEIGHT_MARSIAN

        # create repo for new population
        if not isdir(self._get_population_str()):
            mkdir(self._get_population_str())

    def create_blobs(self) -> None:
        """Can be called to create a random set of blobs."""

        for i in range(self._n):

            # Constants for normal size
            std = 0.5 * self._scatter
            mean = 20

            # create the blob
            size = round(normal(loc=mean, scale=std), 2)
            weight = round(size*2+3*normal(loc=0, scale=1), 2)

            # determin color based on size
            # as 12 is the largest scatter,
            # 6 is the reference deviation here
            std = 6
            if size < mean-2*std:
                color = 0
            elif size < mean-std:
                color = 1
            elif size < mean-0.3*std:
                color = 2
            elif size < mean+0.3*std:
                color = 3
            elif size < mean+std:
                color = 4
            elif size < mean+2*std:
                color = 5
            else:
                color = 6

            color_html = COLORS[color][1]
            color_string = COLORS[color][0]

            cuteness = randint(low=1, high=6)
            name = get_first_name() + " " + str(i)

            # save the blob
            blob = (name, size, weight, color_string, cuteness)
            self._population["blobs"].append(blob)
            self._population["sizes"].append(size)

            # draw the blob
            self._draw_blob(color=color_html, filename=f"blob_{name}")

        # resize the blob images according to blob size
        self._size_drawings()

        # create a blob dataframe
        self._df = DataFrame(
            self._population["blobs"],
            columns=[
                "name",
                "size",
                "weight",
                "color",
                "cuteness"
            ]
        )
        self._df.index = self._df.name
        self._df.drop("name", axis=1, inplace=True)

    def _get_population_str(self) -> None:
        """Can be used to generate a population string."""

        return f"blob_population_n{self._n}_s{self._scatter}"

    def _draw_blob(self, filename, color="#000000") -> None:
        """Can be used to generate a blob image as png

        :param filename: The name of the final png file
        :param color: The HTML color that the blob should have
        """

        path = join(self._get_population_str(), "temp.svg")

        with open(path, "w", encoding="utf8") as temp_file:
            temp_file.write(
                self._kind.replace(REPLACE_STRING, color)
            )

        drawing = svg2rlg(path)
        renderPM.drawToFile(
            drawing,
            join(self._get_population_str(), f"{filename}.png"),
            fmt="PNG"
        )

        remove(path)

    def delete_individual_pngs(self) -> None:
        """Can be called to remove all blob png files saved to disk."""

        for blob in self._population["blobs"]:
            name = blob[0]
            remove(join(self._get_population_str(), f"blob_{name}.png"))

    def _size_drawings(self) -> None:
        """Is used to scale the size of the temporary png images"""

        max_size = max(self._population["sizes"])

        for size in self._population["sizes"]:
            self._population["scales"].append(size/max_size)

        for i, blob in enumerate(self._population["blobs"]):
            img_name = join(
                self._get_population_str(),
                f"blob_{blob[0]}.png"
            )
            image = Image.open(img_name)
            width, height = image.size
            width = int(width*self._population["scales"][i])
            height = int(height*self._population["scales"][i])
            image = image.resize((width, height), Image.ANTIALIAS)
            image.save(fp=img_name)

    def _plot_population(self, img_name, cols) -> None:
        """Can be used to plot a population chart

        :param img_name: The name of the final image saved
        """

        if not cols:
            cols = max(int(self._n/5), 2)

        nrows = int(ceil(len(self._population["blobs"])/cols))

        _, axis = plt.subplots(
            ncols=cols,
            nrows=nrows,
            figsize=(15, 15*nrows/cols),
            sharex=True,
            sharey=True
        )

        i = 0
        for col in range(cols):
            for row in range(nrows):
                if i == len(self._population["blobs"]):
                    break
                blob = self._population["blobs"][i]
                name = blob[0]
                img_path = join(
                    self._get_population_str(),
                    f"blob_{name}.png"
                )
                image = plt.imread(img_path)
                axis[row, col].set_title(name, loc="left")
                axis[row, col].imshow(image)

                axis[row, col].set_ylim([self._kind_h, 0])
                axis[row, col].set_xlim([0, self._kind_w])

                i += 1

        for col in range(cols):
            for row in range(nrows):
                axis[row, col].axis('off')

        plt.tight_layout()
        plt.savefig(img_name)

    def export_data(self, cols=None) -> bool:
        """Can be used to export a dataframe with blob specs."""

        if cols:
            assert cols > 0, "Cols must be positive"
            assert isinstance(cols, int), "Cols must be int"

        self._df.to_excel(
            join(self._get_population_str(), "population.xlsx")
        )

        img_name = join(
            self._get_population_str(),
            "population.png"
        )

        self._plot_population(img_name=img_name, cols=cols)
        self._plot_data()

    def _plot_data(self) -> None:
        """Can be used to plot the data."""

        fig, axis = plt.subplots(nrows=1, ncols=4, figsize=(20, 5))

        axis[0].hist(self._df["size"], label="data", color="k", bins=7)
        axis[1].hist(self._df["weight"], label="data", color="k", bins=7)
        axis[2].bar(
            height=self._df["cuteness"].value_counts().values,
            x=self._df["cuteness"].value_counts().index,
            label="data",
            color="k"
        )
        axis[3].scatter(
            x=self._df["size"],
            y=self._df["weight"],
            label="data",
            color="k"
        )

        axis[0].plot(
            [self._df["size"].mean()],
            [0.2],
            "vr",
            markersize=15,
            label="mean"
        )
        axis[1].plot(
            [self._df["weight"].mean()],
            [0.2],
            "vr",
            markersize=15,
            label="mean"
        )

        axis[0].plot(
            [self._df["size"].median()],
            [0.2],
            "v",
            color="orange",
            markersize=15,
            label="median"
        )

        axis[1].plot(
            [self._df["weight"].median()],
            [0.2],
            "v",
            color="orange",
            markersize=15,
            label="median"
        )

        axis[2].plot(
            [self._df["cuteness"].median()],
            [0.2],
            "v",
            color="orange",
            markersize=15,
            label="median"
        )

        axis[0].legend(loc=0)
        axis[1].legend(loc=0)
        axis[2].legend(loc=0)
        axis[3].legend(loc=0)

        axis[0].set_title("Size Histogram")
        axis[1].set_title("Weight Histogram")
        axis[2].set_title("Cuteness Barchart")
        axis[3].set_title("Weight over Size Scatter Plot")

        axis[0].set_xlabel("size class")
        axis[0].set_ylabel("abs. frequency")
        axis[1].set_xlabel("weight class")
        axis[1].set_ylabel("abs. frequency")
        axis[2].set_xlabel("cuteness class")
        axis[2].set_ylabel("abs. frequency")
        axis[3].set_xlabel("size")
        axis[3].set_ylabel("weight")
        fig.suptitle("Analysis of Population")

        plt.savefig(
            join(self._get_population_str(), "histograms.png")
        )
