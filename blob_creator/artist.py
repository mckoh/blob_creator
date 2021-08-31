import sys
import os

# Add current path to path to allow dependency import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))
from _const import COLORS

class Artist:

    def __init__(self, n=5, scatter=12, export_png=True) -> None:
        """Artist class that is used to generate a blob data set.
        
        :param n: The size of the dataset
        :param scatter: The variability of the data that are generated
        :param export_png: A switch that lets you export the original pngs
        """

        assert scatter <= 12, ValueError("Scatter cannot be larger than 12")
        self._n = n
        self._scatter = scatter
        self._export_png = export_png
        self._blobs = list()
        self._sizes = list()
        self._scales = list()

        from os import mkdir
        from os.path import isdir

        # create repo for new population
        if not isdir(self._get_population_str()):
            mkdir(self._get_population_str())


    def create_blobs(self) -> None:
        """Can be called to create a random set of blobs."""

        from numpy.random import normal, randint
        from names import get_first_name
        from os.path import join

        for i in range(self._n):

            # Constants for normal size
            s = 0.5*self._scatter
            m = 20

            # create the blob
            size = round(normal(loc=m, scale=s), 2)
            weight = round(size*2+size*normal(loc=0, scale=1), 2)
            
            # determin color based on size
            # as 12 is the largest scatter,
            # 6 is the reference deviation here
            s = 6
            if size < m-2*s:
                c = 0
            elif size < m-s:
                c = 1
            elif size < m-0.3*s:
                c = 2
            elif size < m+0.3*s:
                c = 3
            elif size < m+s:
                c = 4
            elif size < m+2*s:
                c = 5
            else:
                c = 6

            color = COLORS[c]
            color_html = color[1]
            color_string = color[0]

            cuteness = int(normal(loc=self._scatter, scale=0.2*self._scatter))
            name = get_first_name() + " " + str(i)

            # save the blob             
            blob = (name, size, weight, color_string, cuteness)
            self._blobs.append(blob)
            self._sizes.append(size)

            # draw the blob
            self._draw_blob(color=color_html, filename=f"blob_{name}")

        img_name = join(
            self._get_population_str(),
            "population.png"
        )

        self._size_drawings()
        self._plot_population(img_name=img_name)
        if not self._export_png:
            self._delete_drawings()

    def _get_population_str(self):
        return f"blob_population_n{self._n}_s{self._scatter}"

    def _draw_blob(self, filename, color="#000000") -> None:
        """Can be used to generate a blob image as png
        
        :param filename: The name of the final png file
        :param color: The HTML color that the blob should have
        """

        from _const import MONSTER, REPLACE_STRING
        from svglib.svglib import svg2rlg
        from reportlab.graphics import renderPM
        from os import remove
        from os.path import join

        path = join(self._get_population_str(), "temp.svg")

        with open(path, "w", encoding="utf8") as temp_file:
            temp_file.write(
                MONSTER.replace(REPLACE_STRING, color)
            )
        
        drawing = svg2rlg(path)
        renderPM.drawToFile(
            drawing,
            join(self._get_population_str(), f"{filename}.png"),
            fmt="PNG"
        )

        remove(path)

    def _delete_drawings(self):
        """Can be called to remove all blob png files saved to disk."""

        from os import remove
        from os.path import join

        for blob in self._blobs:
            name = blob[0]
            remove(join(self._get_population_str(), f"blob_{name}.png"))
            
    def _size_drawings(self):
        """Is used to scale the image size of the temporary png images"""
        
        from PIL import Image
        from os.path import join
        
        max_size = max(self._sizes)
        
        for size in self._sizes:
            self._scales.append(size/max_size)
        
        for i, blob in enumerate(self._blobs):
            img_name = join(self._get_population_str(), f"blob_{blob[0]}.png")
            image = Image.open(img_name)
            width, height = image.size
            width, height = int(width*self._scales[i]), int(height*self._scales[i])
            image = image.resize((width,height),Image.ANTIALIAS)
            image.save(fp=img_name)
            
    def _plot_population(self, img_name) -> None:
        """Can be used to plot a population chart
        
        :param img_name: The name of the final image that is saved on disk
        """

        from matplotlib import pyplot as plt
        from numpy import ceil
        from os.path import join

        nrows = int(ceil(len(self._blobs)/4))
        ncols = 4

        fig, ax = plt.subplots(
            ncols=ncols,
            nrows=nrows,
            figsize=(15,15*nrows/ncols),
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
                img_path = join(self._get_population_str(), f"blob_{name}.png")
                image = plt.imread(img_path)
                ax[row, col].set_title(name, loc="left")
                ax[row, col].imshow(image)
                
                ax[row, col].set_ylim([476,0])
                ax[row, col].set_xlim([0,417])
                
                i += 1

        for col in range(ncols):
            for row in range(nrows):
                ax[row, col].axis('off')
        
        plt.savefig(img_name)

    def export_data(self, sep="\t"):
        """Can be used to export a dataframe with the generated blob specs.
        
        :param sep: Used separator for csv export (default Tab)
        """

        from pandas import DataFrame
        from os.path import join

        df = DataFrame(
            self._blobs,
            columns=[
                "name", 
                "size",
                "weight",
                "color",
                "cuteness"
            ]
        )
        df.index = df.name
        df.drop("name", axis=1, inplace=True)
        df.to_excel(join(self._get_population_str(), "population.xlsx"))