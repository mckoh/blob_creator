from os import error, scandir
from src.blob_creator.core import BlobFactory
from pytest import raises


def test_n():
    error_message = "n was not correctly stored"
    test_factory = BlobFactory(n=12)
    assert test_factory._n == 12, error_message
    test_factory = BlobFactory(n=13)
    assert test_factory._n == 13, error_message
    

def test_scatter():
    error_message = "scatter was not correctly storeds"
    
    for s in range(1,13):
        try:
            test_factory = BlobFactory(scatter=s)
            assert test_factory._scatter == s, error_message
        except ValueError:
            assert False, error_message


def test_img_dims():
    error_message = "Blob image width/height not correct"
    test_factory = BlobFactory(monster="B")
    assert test_factory._monster_w == 512 and test_factory._monster_h ==512, error_message
    test_factory = BlobFactory(monster="A")
    assert test_factory._monster_w == 417 and test_factory._monster_h ==476, error_message


def test_monster_type():
    error_message = "Monster Type C was allowed though it is not supported"
    with raises(AssertionError):
        test_factory = BlobFactory(monster="C")
        assert False, error_message


def test_scatter_range_low():
    error_message = "Factory allowed too small scatter range"
    with raises(AssertionError):
        test_factory = BlobFactory(scatter=0)
        assert False, error_message
    
    
def test_scatter_range_high():
    error_message = "Factory allowed too large scatter range"
    with raises(AssertionError):
        test_factory = BlobFactory(scatter=13)
        assert False, error_message


def test_population_string():
    error_message = "Population string was not correctly generated"
    test_factory = BlobFactory(n=5, scatter=1)
    population_string = test_factory._get_population_str()
    assert population_string == "blob_population_n5_s1", error_message


def test_folder_creation():
    from os.path import isdir
    error_message = "Data folder has not been created correctly"
    test_factory = BlobFactory()
    dir_path = test_factory._get_population_str()
    assert isdir(dir_path), error_message


def test_image_creation():
    from os import listdir
    error_message = "Images have not been correctly created"
    n=7
    test_factory = BlobFactory(n=n, scatter=2, export_png=True)
    test_factory.create_blobs()
    dir_path = test_factory._get_population_str()
    assert len(listdir(dir_path)) == n, error_message


def test_image_keeping():
    from os import listdir
    error_message = "Images have not been kept correctly"
    n=7
    test_factory = BlobFactory(n=n, scatter=2, export_png=True)
    test_factory.create_blobs()
    test_factory.export_data()
    dir_path = test_factory._get_population_str()
    assert len(listdir(dir_path)) == n+3, error_message


def test_image_deletion():
    from os import listdir
    error_message = "Images have not been correctly created"
    n=7
    test_factory = BlobFactory(n=n, scatter=2, export_png=False)
    test_factory.create_blobs()
    test_factory.export_data()
    dir_path = test_factory._get_population_str()
    assert len(listdir(dir_path)) == 3, error_message