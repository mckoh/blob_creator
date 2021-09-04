"""
Core module of Blob Creator

Author: Michael Kohlegger
Date: 2021-09
"""

import sys
from os import mkdir, remove
from os.path import isdir, abspath, dirname, join
from numpy import ceil
from numpy.random import normal, randint
from names import get_first_name
from pandas import DataFrame
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from PIL import Image
from matplotlib import pyplot as plt

sys.path.insert(0, abspath(join(dirname(__file__))))
from const import REPLACE_STRING
from const import MONSTER_A, WIDTH_A, HEIGHT_A
from const import MONSTER_B, WIDTH_B, HEIGHT_B
from const import COLORS

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
                 export_png=True,
                 cols=None,
                 monster="B") -> None:

        assert scatter <= 12, "Scatter cannot be larger than 12"
        assert n > 0, "n must be positive"
        assert monster in ["A", "B"], "Monster can only be A or B"
        assert isinstance(n, int), "n must be int"
        assert isinstance(scatter, int), "scatter must be int"

        if cols:
            assert cols > 0, "Cols must be positive"
            assert isinstance(cols, int), "Cols must be int"

        self._n = n
        self._scatter = scatter
        self._export_png = export_png
        self._blobs = []
        self._sizes = []
        self._scales = []
        self._df = None
        self._cols = cols

        if monster == "A":
            self._monster = MONSTER_A
            self._monster_w = WIDTH_A
            self._monster_h = HEIGHT_A

        elif monster == "B":
            self._monster = MONSTER_B
            self._monster_w = WIDTH_B
            self._monster_h = HEIGHT_B

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
            self._blobs.append(blob)
            self._sizes.append(size)

            # draw the blob
            self._draw_blob(color=color_html, filename=f"blob_{name}")

        # resize the blob images according to blob size
        self._size_drawings()

        # create a blob dataframe
        self._df = DataFrame(
            self._blobs,
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
                self._monster.replace(REPLACE_STRING, color)
            )

        drawing = svg2rlg(path)
        renderPM.drawToFile(
            drawing,
            join(self._get_population_str(), f"{filename}.png"),
            fmt="PNG"
        )

        remove(path)

    def _delete_drawings(self) -> None:
        """Can be called to remove all blob png files saved to disk."""

        for blob in self._blobs:
            name = blob[0]
            remove(join(self._get_population_str(), f"blob_{name}.png"))

    def _size_drawings(self) -> None:
        """Is used to scale the size of the temporary png images"""

        max_size = max(self._sizes)

        for size in self._sizes:
            self._scales.append(size/max_size)

        for i, blob in enumerate(self._blobs):
            img_name = join(
                self._get_population_str(),
                f"blob_{blob[0]}.png"
            )
            image = Image.open(img_name)
            width, height = image.size
            width = int(width*self._scales[i])
            height = int(height*self._scales[i])
            image = image.resize((width, height), Image.ANTIALIAS)
            image.save(fp=img_name)

    def _plot_population(self, img_name) -> None:
        """Can be used to plot a population chart

        :param img_name: The name of the final image saved
        """

        if not self._cols:
            ncols = max(int(self._n/8), 2)
        else:
            ncols = self._cols

        nrows = int(ceil(len(self._blobs)/ncols))

        _, axis = plt.subplots(
            ncols=ncols,
            nrows=nrows,
            figsize=(15, 15*nrows/ncols),
            sharex=True,
            sharey=True
        )

        i = 0
        for col in range(ncols):
            for row in range(nrows):
                if i == len(self._blobs):
                    break
                blob = self._blobs[i]
                name = blob[0]
                img_path = join(
                    self._get_population_str(),
                    f"blob_{name}.png"
                )
                image = plt.imread(img_path)
                axis[row, col].set_title(name, loc="left")
                axis[row, col].imshow(image)

                axis[row, col].set_ylim([self._monster_h, 0])
                axis[row, col].set_xlim([0, self._monster_w])

                i += 1

        for col in range(ncols):
            for row in range(nrows):
                axis[row, col].axis('off')

        plt.tight_layout()
        plt.savefig(img_name)

    def export_data(self) -> bool:
        """Can be used to export a dataframe with blob specs.

        :return: Boolean response
        """

        self._df.to_excel(
            join(self._get_population_str(), "population.xlsx")
        )

        img_name = join(
            self._get_population_str(),
            "population.png"
        )

        self._plot_population(img_name=img_name)
        self._plot_data()
        if not self._export_png:
            self._delete_drawings()

        return True

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
