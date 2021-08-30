# %%
blobs = [('Andree', 18.86, 18.73, 'red', 9),
 ('Carlos', 19.09, 45.81, 'blue', 10),
 ('Alisha', 21.69, 28.41, 'orange', 10),
 ('Carey', 21.13, 36.12, 'light orange', 7),
 ('Ty', 20.13, 44.84, 'orange', 11),
 ('Cleo', 20.64, 17.44, 'light orange', 15)]

from matplotlib import pyplot as plt
from numpy import ceil

nrows = int(ceil(len(blobs)/4))
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
        if i == len(blobs):
            break
        blob = blobs[i]
        name = blob[0]
        img_path = f"blob_{name}.png"
        image = plt.imread(img_path)
        ax[row, col].set_title(name)
        ax[row, col].imshow(image)
        i += 1

for col in range(ncols):
    for row in range(nrows):
        ax[row, col].axis('off')

# %%
a.