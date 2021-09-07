from os import error, removedirs, scandir
from src.blob_creator.core import BlobFactory
from pytest import raises
from shutil import rmtree


def test_n():
    error_message = "n was not correctly stored"
    test_factory = BlobFactory(n=12, scatter=12)
    assert test_factory._n == 12, error_message
    test_factory = BlobFactory(n=13, scatter=12)
    assert test_factory._n == 13, error_message
    rmtree("blob_population_n12_s12")
    rmtree("blob_population_n13_s12")

def test_scatter():
    error_message = "scatter was not correctly storeds"
    for s in range(1,13):
        try:
            test_factory = BlobFactory(n=5, scatter=s)
            assert test_factory._scatter == s, error_message
        except ValueError:
            assert False, error_message
        rmtree(f"blob_population_n5_s{s}")
    
def test_img_dims():
    error_message = "Blob image width/height not correct"
    test_factory = BlobFactory(n=5, scatter=3, kind="monster")
    assert test_factory._kind_w == 512 and test_factory._kind_h == 512, error_message
    rmtree(f"blob_population_n5_s3")
    test_factory = BlobFactory(n=5, scatter=3, kind="alien")
    assert test_factory._kind_w == 417 and test_factory._kind_h == 476, error_message
    rmtree(f"blob_population_n5_s3")
    test_factory = BlobFactory(n=5, scatter=3, kind="boy")
    assert test_factory._kind_w == 600 and test_factory._kind_h == 600, error_message
    rmtree(f"blob_population_n5_s3")
    test_factory = BlobFactory(n=5, scatter=3, kind="marsian")
    assert test_factory._kind_w == 600 and test_factory._kind_h == 600, error_message
    rmtree(f"blob_population_n5_s3")


def test_monster_type():
    error_message = "Monster Type C was allowed though it is not supported"
    with raises(AssertionError):
        test_factory = BlobFactory(n=5, scatter=3, monster="C")
        rmtree(f"blob_population_n5_s3")
        assert False, error_message


def test_scatter_range_low():
    error_message = "Factory allowed too small scatter range"
    with raises(AssertionError):
        test_factory = BlobFactory(n=5, scatter=0)
        rmtree(f"blob_population_n5_s0")
        assert False, error_message


def test_scatter_range_high():
    error_message = "Factory allowed too large scatter range"
    with raises(AssertionError):
        test_factory = BlobFactory(n=5, scatter=13)
        rmtree(f"blob_population_n5_s13")
        assert False, error_message


def test_population_string():
    error_message = "Population string was not correctly generated"
    test_factory = BlobFactory(n=5, scatter=1)
    population_string = test_factory._get_population_str()
    assert population_string == "blob_population_n5_s1", error_message
    rmtree(f"blob_population_n5_s1")


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
    rmtree(f"blob_population_n{n}_s2")


def test_image_keeping():
    from os import listdir
    error_message = "Images have not been kept correctly"
    n=8
    test_factory = BlobFactory(n=n, scatter=3, export_png=True)
    test_factory.create_blobs()
    test_factory.export_data()
    dir_path = test_factory._get_population_str()
    assert len(listdir(dir_path)) == n+3, error_message
    rmtree(f"blob_population_n{n}_s3")


def test_image_deletion():
    from os import listdir
    error_message = "Images have not been correctly created"
    n=9
    test_factory = BlobFactory(n=n, scatter=4, export_png=False)
    test_factory.create_blobs()
    test_factory.export_data()
    dir_path = test_factory._get_population_str()
    assert len(listdir(dir_path)) == 3, error_message
    rmtree(f"blob_population_n{n}_s4")


def test_negative_n():
    error_message = "Negative n not correctly detected"
    with raises(AssertionError):
        test_factory = BlobFactory(n=-1, scatter=12)
        assert False, error_message


def test_zero_n():
    error_message = "Zero n not correctly detected"
    with raises(AssertionError):
        test_factory = BlobFactory(n=0, scatter=12)
        assert False, error_message


def test_int_n():
    error_message = "n must be integer"
    with raises(AssertionError):
        test_factory = BlobFactory(n=5.0)
        assert False, error_message


    def test_int_scatter():
    error_message = "scatter must be integer"
    with raises(AssertionError):
        test_factory = BlobFactory(scatter=12.0)
        assert False, error_message


def test_int_cols():
    error_message = "cols must be integer"
    with raises(AssertionError):
        test_factory = BlobFactory(cols=2.0)
        assert False, error_message


def test_negative_cols():
    error_message = "cols must be positive"
    with raises(AssertionError):
        test_factory = BlobFactory(cols=0)
        assert False, error_message


def test_export_return():
    from os import listdir
    error_message = "Export did not return flag"
    test_factory = BlobFactory(n=5, scatter=4, export_png=False)
    test_factory.create_blobs()
    response = test_factory.export_data()
    dir_path = test_factory._get_population_str()
    assert type(response) == bool, error_message
    rmtree(dir_path)
