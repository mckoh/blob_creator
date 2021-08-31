from sys import argv
from blob_creator.artist import Artist

if __name__ == "__main__":

    assert len(argv)==4, ValueError("To few arguments passed. Make sure you provide n, scatter and cols.")

    n = int(argv[1])
    s = int(argv[2])
    c = int(argv[3])

    a = Artist(n=n, scatter=s, cols=c, export_png=False)
    a.create_blobs()
    a.export_data()
