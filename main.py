from blob_creator._const import MONSTER
from blob_creator._const import COLORS
from blob_creator._const import REPLACE_STRING

color = COLORS[0]

monster = MONSTER.replace(REPLACE_STRING, color)


from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

drawing = svg2rlg("blob_creator/res/monster.svg")
renderPM.drawToFile(drawing, "file.png", fmt="PNG")