# Blob Dataset Creator

Blobs are little monsters that you can use to demonstrate data analysis procedures. They have a size, a weight, a color and a cuteness level. As you can see, a blob dataset contains all types of variables that you can find in the wild (nominal, ordinal and metric). 

## Use the Generator

Blob populations can either have large (12) or small (1) **variability**, determined by the population's scatter index. Moreover, they can consist of a large **number** of monsters or can also be small, determined by the population's n.

You can **generate a new population** by calling:

```python
from blob_creator.artist import Artist

# This instantiates a new blob factory
a = Artist(n=20, scatter=12, export_png=True)

# This will create the blobs
a.create_blobs()

# This will export your dataset to disk
a.export_data()
```

## Installation

Make sure to install all required dependencies, given in [`requirements.txt`](requirements.txt).
