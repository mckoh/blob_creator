"""
Core module of Blob Creator

Author: Michael Kohlegger
Date: 2021-09
"""

from shutil import rmtree
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
from matplotlib import use

from .const import REPLACE_STRING
from .const import MONSTER, WIDTH_MONSTER, HEIGHT_MONSTER
from .const import ALIEN, WIDTH_ALIEN, HEIGHT_ALIEN
from .const import BOY, WIDTH_BOY, HEIGHT_BOY
from .const import MARSIAN, WIDTH_MARSIAN, HEIGHT_MARSIAN
from .const import COLORS
from .functions import dictionary_filter
from .uploader import upload_file

# Switch matplotlib backend
use("agg")

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
        self._population = None
        self._png_created = False

        if kind == "alien":
            self._kind = (kind, ALIEN)
            self._kind_w = WIDTH_ALIEN
            self._kind_h = HEIGHT_ALIEN

        elif kind == "monster":
            self._kind = (kind, MONSTER)
            self._kind_w = WIDTH_MONSTER
            self._kind_h = HEIGHT_MONSTER

        elif kind == "boy":
            self._kind = (kind, BOY)
            self._kind_w = WIDTH_BOY
            self._kind_h = HEIGHT_BOY

        elif kind == "marsian":
            self._kind = (kind, MARSIAN)
            self._kind_w = WIDTH_MARSIAN
            self._kind_h = HEIGHT_MARSIAN

    def create_blobs(self) -> None:
        """Can be called to create a random set of blobs."""

        if isdir(self.get_population_string()):
            rmtree(self.get_population_string())
        mkdir(self.get_population_string())

        self._population = {
            "names": [],
            "sizes": [],
            "weights": [],
            "colors": [],
            "cuteness_levels": [],
            "scales": [],
        }

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

            self._population["names"].append(name)
            self._population["sizes"].append(size)
            self._population["weights"].append(weight)
            self._population["colors"].append(color_string)
            self._population["cuteness_levels"].append(cuteness)

            self._draw_blob(color=color_html, filename=f"blob_{name}")

        self._size_drawings()

        self._png_created = True

    def _create_dataframe(self) -> DataFrame:
        """Can be used to return a dataframe of the population"""

        data = dictionary_filter(
            self._population,
            ["names", "sizes", "weights", "colors", "cuteness_levels"]
        )

        dataframe = DataFrame(data)
        dataframe.index = dataframe["names"]
        dataframe.drop("names", axis=1, inplace=True)

        return dataframe

    def _draw_blob(self, filename, color="#000000") -> None:
        """Can be used to generate a blob image as png

        :param filename: The name of the final png file
        :param color: The HTML color that the blob should have
        """

        path = join(self.get_population_string(), "temp.svg")

        with open(path, "w", encoding="utf8") as temp_file:
            temp_file.write(
                self._kind[1].replace(REPLACE_STRING, color)
            )

        drawing = svg2rlg(path)
        renderPM.drawToFile(
            drawing,
            join(self.get_population_string(), f"{filename}.png"),
            fmt="PNG"
        )

        remove(path)

    def delete_individual_pngs(self) -> None:
        """Can be called to remove all blob png files saved to disk."""
        if not self._png_created:
            assert False, "No PNGs to delete."
        else:
            for name in self._population["names"]:
                remove(join(self.get_population_string(), f"blob_{name}.png"))
            self._png_created = False

    def _size_drawings(self) -> None:
        """Is used to scale the size of the temporary png images"""

        max_size = max(self._population["sizes"])

        for size in self._population["sizes"]:
            self._population["scales"].append(size/max_size)

        for i, name in enumerate(self._population["names"]):
            img_name = join(
                self.get_population_string(),
                f"blob_{name}.png"
            )
            image = Image.open(img_name)
            width, height = image.size
            width = max(int(width*self._population["scales"][i]), 1)
            height = max(int(height*self._population["scales"][i]), 1)
            image = image.resize((width, height), Image.ANTIALIAS)
            image.save(fp=img_name)

    def _plot_population(self, img_name, cols) -> None:
        """Can be used to plot a population chart

        :param img_name: The name of the final image saved
        """

        if not cols:
            cols = max(int(self._n/5), 2)

        nrows = int(ceil(len(self._population["names"])/cols))

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
                if i == len(self._population["names"]):
                    break
                name = self._population["names"][i]
                img_path = join(
                    self.get_population_string(),
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

        if not self._png_created:
            assert False, "No PNGs created that I could export"
        else:
            if cols:
                assert cols > 0, "Cols must be positive"
                assert isinstance(cols, int), "Cols must be int"
                assert cols < self._n, "Cols must be less than n"

            dataframe = self._create_dataframe()
            dataframe.to_csv(
                join(self.get_population_string(), "population.csv")
            )

            img_name = join(
                self.get_population_string(),
                "population.png"
            )

            self._plot_population(img_name=img_name, cols=cols)
            self._plot_data()

    def _plot_data(self) -> None:
        """Can be used to plot the data."""

        fig, axis = plt.subplots(nrows=1, ncols=4, figsize=(20, 5))

        dataframe = self._create_dataframe()

        axis[0].hist(dataframe["sizes"], label="data", color="k", bins=7)
        axis[1].hist(dataframe["weights"], label="data", color="k", bins=7)
        axis[2].bar(
            height=dataframe["cuteness_levels"].value_counts().values,
            x=dataframe["cuteness_levels"].value_counts().index,
            label="data",
            color="k"
        )
        axis[3].scatter(
            x=dataframe["sizes"],
            y=dataframe["weights"],
            label="data",
            color="k"
        )

        axis[0].plot(
            [dataframe["sizes"].mean()],
            [0.2],
            "vr",
            markersize=15,
            label="mean"
        )
        axis[1].plot(
            [dataframe["weights"].mean()],
            [0.2],
            "vr",
            markersize=15,
            label="mean"
        )

        axis[0].plot(
            [dataframe["sizes"].median()],
            [0.2],
            "v",
            color="orange",
            markersize=15,
            label="median"
        )

        axis[1].plot(
            [dataframe["weights"].median()],
            [0.2],
            "v",
            color="orange",
            markersize=15,
            label="median"
        )

        axis[2].plot(
            [dataframe["cuteness_levels"].median()],
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
            join(self.get_population_string(), "histograms.png")
        )

    def upload_dataset(self) -> str:
        """Can be used to make the dataset publicly available

        :return: URL of uploaded file
        """
        url = upload_file(
            join(
                self.get_population_string(),
                "population.csv"
            )
        )
        return url

    # GETTER METHODS
    def get_kind_parameters(self) -> tuple:
        """Returns the images height and width"""
        return self._kind[0], self._kind_h, self._kind_w

    def get_png_status(self) -> bool:
        """Returns the PNG creation status"""
        return self._png_created

    def get_base_parameters(self) -> tuple:
        """Returns n and scatter of an engine object"""
        return self._n, self._scatter

    def get_population_string(self) -> None:
        """Can be used to generate a population string."""
        return f"blob_population_{self._kind[0]}_n{self._n}_s{self._scatter}"

    def get_population(self) -> dict:
        """Can be used to get population object"""
        return self._population
