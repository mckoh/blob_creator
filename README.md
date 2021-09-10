# Blob Dataset Creator

[![Publish to PyPI](https://github.com/mckoh/blob_creator/actions/workflows/pypi.yml/badge.svg)](https://github.com/mckoh/blob_creator/actions/workflows/pypi.yml) [![Lint with PyLint](https://github.com/mckoh/blob_creator/actions/workflows/pylint.yml/badge.svg)](https://github.com/mckoh/blob_creator/actions/workflows/pylint.yml) [![Test with Pytest](https://github.com/mckoh/blob_creator/actions/workflows/pytest.yml/badge.svg)](https://github.com/mckoh/blob_creator/actions/workflows/pytest.yml)

Blobs are little monsters that you can use to demonstrate data analysis procedures. They have a size, a weight, a color and a cuteness level. As you can see, a blob dataset contains all types of variables that you can find in the wild (nominal, ordinal and metric).

## Generator Output

This generator creates a population of blobs. It delivers (a) an Excel data frame with every blob's properties, (b) a population plot that visualizes all blobs for presentation purposes and (c) a set of visualizations of the population data.

![Dataframe](https://github.com/mckoh/blob_creator/raw/main/static/dataframe.png)

The **population plot** displays all blobs with color and size. In addition to that, it shows blob names. There are three different kinds of base images that can be used to visualize blobs.

![Blob population](https://github.com/mckoh/blob_creator/raw/main/static/population_alien.png)

The **visualization plot** inklude a histogram of blob size and blob weights, as well as a bar chart with cuteness level counts and a scatter plot of size and weight.

![Blob population analysis](https://github.com/mckoh/blob_creator/raw/main/static/histograms.png)

## Use the Generator

Blob populations can either have large (12) or small (1) **variability**, determined by the population's scatter index. Moreover, they can consist of a large **number** of monsters or can also be small, determined by the population's n.

You can **generate a new population** by calling:

```python
from blob_creator.core import BlobFactory

# This instantiates a new blob factory
blob_factory = BlobFactory(n=20, scatter=12, kind="monster")

# This will create the blobs
blob_factory.create_blobs()

# This will export your dataset and your population plot to disk
blob_factory.export_data()

# Upload the csv file of the popoulation to share
# it with your students
blob_factory.upload_dataset()

# Finally, the output directory can be cleaned-up
blob_factory.delete_individual_pngs()
```

## Package Installation

This package can be installed using Python's package index. Use the following command to do this:

```shell
pip install blob-creator
```
