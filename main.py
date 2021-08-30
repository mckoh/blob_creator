# %%
from blob_creator.artist import Artist

# %%
a = Artist(n=6, scatter=1)
a._create_blobs()
a._blobs

# %%
a._delete_drawings()