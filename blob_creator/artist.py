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