import sys
import os

# Add current path to path to allow dependency import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))
from _const import COLORS

class Artist:

    def __init__(self, n=5, scatter=12) -> None:
        """Artist class that is used to generate a blob data set.
        
        :param n: The size of the dataset
        :param scatter: The variability of the data that are generated
        """

        assert scatter <= 12, ValueError("Scatter cannot be larger than 12")
        self._n = n
        self._scatter = scatter
        self._blobs = list()
        self._sizes = list()
        self._scales = list()


    def create_blobs(self) -> None:
        """Can be called to create a random set of blobs."""

        from numpy.random import normal, randint
        from names import get_first_name

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

        img_name = f"blob_population_n{self._n}_s{self._scatter}.png"

        self._size_drawings()
        self._plot_population(img_name=img_name)
        self._delete_drawings()


    def _draw_blob(self, filename, color="#000000") -> None:
        """Can be used to generate a blob image as png
        
        :param filename: The name of the final png file
        :param color: The HTML color that the blob should have
        """

        from _const import MONSTER, REPLACE_STRING
        from svglib.svglib import svg2rlg
        from reportlab.graphics import renderPM
        from os import remove

        with open("temp.svg", "w", encoding="utf8") as temp_file:
            temp_file.write(
                MONSTER.replace(REPLACE_STRING, color)
            )
        
        drawing = svg2rlg("temp.svg")
        renderPM.drawToFile(drawing, f"{filename}.png", fmt="PNG")

        remove("temp.svg")

    def _delete_drawings(self):
        """Can be called to remove all blob png files saved to disk."""

        from os import remove
        for blob in self._blobs:
            name = blob[0]
            try:
                remove(f"blob_{name}.png")
            except:
                print("Name duplicate in Blob family  detected.")
            
    def _size_drawings(self):
        """Is used to scale the image size of the temporary png images"""
        
        from PIL import Image
        
        max_size = max(self._sizes)
        
        for size in self._sizes:
            self._scales.append(size/max_size)
        
        for i, blob in enumerate(self._blobs):
            img_name = f"blob_{blob[0]}.png"
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
                img_path = f"blob_{name}.png"
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

    def export_data(self):
        from pandas import DataFrame
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
        return df