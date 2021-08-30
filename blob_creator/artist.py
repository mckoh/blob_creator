import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
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
        self._scatter = 10
        self._blobs = list()
        self._sizes = list()
        self._scales = list()


    def _create_blobs(self) -> None:
        """Can be called to create a random set of blobs."""

        from numpy.random import normal, randint
        from names import get_first_name

        for i in range(self._n):

            # create the blob
            size = round(normal(loc=20, scale=0.1*self._scatter), 2)
            weight = round(size*2+size*normal(loc=0, scale=0.1*self._scatter), 2)
            color = COLORS[randint(low=0, high=self._scatter)]
            color_html = color[1]
            color_string = color[0]
            cuteness = int(normal(loc=self._scatter, scale=0.2*self._scatter))
            name = get_first_name()

            # save the blob             
            blob = (name, size, weight, color_string, cuteness)
            self._blobs.append(blob)
            self._sizes.append(size)

            # draw the blob
            self._draw_blob(color=color_html, filename=f"blob_{name}")


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
            remove(f"blob_{name}.png")
            
    def _size_drawings(self):
        
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
            
    def plot_population(self):
        from matplotlib import pyplot as plt
        from numpy import ceil

        nrows = int(ceil(len(self._blobs)/4))
        ncols = 4

        fig, ax = plt.subplots(
            ncols=ncols,
            nrows=nrows,
            figsize=(20,10),
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
                ax[row, col].set_title(name)
                ax[row, col].imshow(image)
                
                ax[row, col].set_ylim([476,0])
                ax[row, col].set_xlim([0,417])
                
                i += 1

        for col in range(ncols):
            for row in range(nrows):
                ax[row, col].axis('off')