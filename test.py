"""
Test Module for Blob Creator

Author: Michael Kohlegger
Date: 2021-09
"""

from os import listdir
from os.path import isdir
from shutil import rmtree

from pytest import raises
from pytest import mark

from src.blob_creator.core import BlobFactory


@mark.my_own
def test_n():
    """Test method"""
    message = "n was not correctly stored"
    test_factory = BlobFactory(n=12, scatter=12)
    assert test_factory.get_base_parameters()[0] == 12, message
    test_factory = BlobFactory(n=13, scatter=12)
    assert test_factory.get_base_parameters()[0] == 13, message


@mark.my_own
def test_scatter():
    """Test method"""
    message = "scatter was not correctly storeds"
    for scatter in range(1,13):
        try:
            test_factory = BlobFactory(n=5, scatter=scatter)
            assert test_factory.get_base_parameters()[1] == scatter, message
        except ValueError:
            assert False, message


@mark.my_own
def test_img_dims():
    """Test method"""
    message = "Blob image width/height not correct"
    test_factory = BlobFactory(n=5, scatter=3, kind="monster")
    height, width = test_factory.get_image_dimensions()
    assert width == 512 and height == 512, message
    test_factory = BlobFactory(n=5, scatter=3, kind="alien")
    height, width = test_factory.get_image_dimensions()
    assert width == 417 and height == 476, message
    test_factory = BlobFactory(n=5, scatter=3, kind="boy")
    height, width = test_factory.get_image_dimensions()
    assert width == 600 and height == 600, message
    test_factory = BlobFactory(n=5, scatter=3, kind="marsian")
    height, width = test_factory.get_image_dimensions()
    assert width == 600 and height == 600, message


@mark.my_own
def test_monster_type():
    """Test method"""
    message = "Monster Type C was allowed though it is not supported"
    with raises(AssertionError):
        _ = BlobFactory(n=5, scatter=3, kind="C")
        assert False, message


@mark.my_own
def test_scatter_range_low():
    """Test method"""
    message = "Factory allowed too small scatter range"
    with raises(AssertionError):
        _ = BlobFactory(n=5, scatter=0)
        assert False, message


@mark.my_own
def test_scatter_range_high():
    """Test method"""
    message = "Factory allowed too large scatter range"
    with raises(AssertionError):
        _ = BlobFactory(n=5, scatter=13)
        assert False, message


@mark.my_own
def test_population_string():
    """Test method"""
    message = "Population string was not correctly generated"
    test_factory = BlobFactory(n=5, scatter=1)
    population_string = test_factory.get_population_string()
    assert population_string == "blob_population_n5_s1", message


@mark.my_own
def test_folder_creation():
    """Test method"""
    message = "Data folder has not been created correctly"
    test_factory = BlobFactory()
    test_factory.create_blobs()
    dir_path = test_factory.get_population_string()
    assert isdir(dir_path), message
    rmtree(dir_path)


@mark.my_own
def test_image_creation():
    """Test method"""
    message = "Images have not been correctly created"
    size = 7
    test_factory = BlobFactory(n=size, scatter=2)
    test_factory.create_blobs()
    dir_path = test_factory.get_population_string()
    assert len(listdir(dir_path)) == size, message
    rmtree(f"blob_population_n{size}_s2")


@mark.my_own
def test_image_keeping():
    """Test method"""
    message = "Images have not been kept correctly"
    size = 8
    test_factory = BlobFactory(n=size, scatter=3)
    test_factory.create_blobs()
    test_factory.export_data()
    dir_path = test_factory.get_population_string()
    assert len(listdir(dir_path)) == size+3, message
    rmtree(f"blob_population_n{size}_s3")


@mark.my_own
def test_image_deletion():
    """Test method"""
    message = "Images have not been correctly created"
    size = 9
    test_factory = BlobFactory(n=size, scatter=4)
    test_factory.create_blobs()
    test_factory.export_data()
    test_factory.delete_individual_pngs()
    dir_path = test_factory.get_population_string()
    assert len(listdir(dir_path)) == 3, message
    rmtree(f"blob_population_n{size}_s4")


@mark.my_own
def test_negative_n():
    """Test method"""
    message = "Negative n not correctly detected"
    with raises(AssertionError):
        _ = BlobFactory(n=-1, scatter=12)
        assert False, message


@mark.my_own
def test_zero_n():
    """Test method"""
    message = "Zero n not correctly detected"
    with raises(AssertionError):
        _ = BlobFactory(n=0, scatter=12)
        assert False, message


@mark.my_own
def test_int_n():
    """Test method"""
    message = "n must be integer"
    with raises(AssertionError):
        _ = BlobFactory(n=5.0)
        assert False, message


@mark.my_own
def test_int_scatter():
    """Test method"""
    message = "scatter must be integer"
    with raises(AssertionError):
        _ = BlobFactory(scatter=12.0)
        assert False, message


@mark.my_own
def test_int_cols():
    """Test method"""
    message = "cols must be integer"
    with raises(AssertionError):
        test_factory = BlobFactory(n=5, scatter=12)
        test_factory.create_blobs()
        test_factory.export_data(cols=2.0)
        rmtree("blob_population_n5_s12")
        assert False, message


@mark.my_own
def test_negative_cols():
    """Test method"""
    message = "cols must be positive"
    with raises(AssertionError):
        test_factory = BlobFactory(n=5, scatter=12)
        test_factory.create_blobs()
        test_factory.export_data(cols=0)
        rmtree("blob_population_n5_s12")
        assert False, message


@mark.my_own
def test_png_switch_before_creation():
    """Test method"""
    message = "PNG switch must be False before Creation"
    test_factory = BlobFactory(n=5, scatter=12)
    assert not test_factory.get_png_status(), message


@mark.my_own
def test_png_switch_after_creation():
    """Test method"""
    message = "PNG switch must be True after Creation"
    test_factory = BlobFactory(n=5, scatter=12)
    test_factory.create_blobs()
    rmtree("blob_population_n5_s12")
    assert test_factory.get_png_status(), message


@mark.my_own
def test_png_switch_after_delete():
    """Test method"""
    message = "PNG switch must be False after deleting"
    test_factory = BlobFactory(n=5, scatter=12)
    test_factory.create_blobs()
    test_factory.delete_individual_pngs()
    rmtree("blob_population_n5_s12")
    assert not test_factory.get_png_status(), message


@mark.my_own
def test_abbort_delete_if_none_created():
    """Test method"""
    message = "PNG must be created before they can be deleted"
    with raises(AssertionError):
        test_factory = BlobFactory(n=5, scatter=12)
        test_factory.delete_individual_pngs()
        assert False, message


@mark.my_own
def test_allow_multiple_creation():
    """Test method"""
    message = "Population must be re-creatable"
    size = 6
    test_factory = BlobFactory(n=size, scatter=12)
    test_factory.create_blobs()
    test_factory.create_blobs()
    rmtree(f"blob_population_n{size}_s12")
    assert len(test_factory.get_population()["names"])==size, message


@mark.my_own
def test_reset_population_dir_on_recreation():
    """Test method"""
    message = "Population dir must be emptied before new creation"
    size = 6
    test_factory = BlobFactory(n=size, scatter=12)
    test_factory.create_blobs()
    test_factory.create_blobs()
    count = len(listdir(test_factory.get_population_string()))
    rmtree(f"blob_population_n{size}_s12")
    assert count==size, message
