# Blob Dataset Creator

Blobs are little monsters that you can use to demonstrate data analysis procedures. They have a size, a weight, a color and a cuteness level. As you can see, a blob dataset contains all types of variables that you can find in the wild (nominal, ordinal and metric).

## Generator Output

This generator creates a population of blobs. It delivers (a) an Excel data frame with every blob's properties, (b) a population plot that visualizes all blobs for presentation purposes and (c) a set of visualizations of the population data.

![Dataframe](https://owncloud.fh-kufstein.ac.at/index.php/s/tUSlgP74rTe20JV/download)

The **population plot** displays all blobs with color and size. In addition to that, it shows blob names.

![Blob population](https://owncloud.fh-kufstein.ac.at/index.php/s/3T1tRme3H5YO9pM/download)

The **visualization plot** inklude a histogram of blob size and blob weights, as well as a bar chart with cuteness level counts and a scatter plot of size and weight.

![Blob population analysis](https://owncloud.fh-kufstein.ac.at/index.php/s/3jyvqYHLZbnhre6/download)

## Use the Generator

Blob populations can either have large (12) or small (1) **variability**, determined by the population's scatter index. Moreover, they can consist of a large **number** of monsters or can also be small, determined by the population's n.

You can **generate a new population** by calling:

```python
from blob_creator.core import BlobFactory

# This instantiates a new blob factory
blob_factory = BlobFactory(n=20, scatter=12, export_png=True)

# This will create the blobs
blob_factory.create_blobs()

# This will export your dataset and your population plot to disk
blob_factory.export_data()
```

## Package Installation

This package can be installed using Python's package index. Use the following command to do this:

```shell
pip install blob-creator
```