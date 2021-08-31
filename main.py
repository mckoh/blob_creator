# %%
from blob_creator.artist import Artist

a = Artist(n=20, scatter=12, export_png=True)
a.create_blobs()
a.export_data()

