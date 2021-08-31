# %%
from blob_creator.artist import Artist

a = Artist(n=20, scatter=12)
a.create_blobs()
a.export_data()

