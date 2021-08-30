
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

drawing = svg2rlg("blob_creator/res/monster.svg")
renderPM.drawToFile(drawing, "file.png", fmt="PNG")