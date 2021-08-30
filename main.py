# %%
from blob_creator.artist import Artist
a = Artist(n=6, scatter=12)
a._create_blobs()
a._size_drawings()
a.plot_population()
a._delete_drawings()