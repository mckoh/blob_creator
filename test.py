"""
Test Module for Blob Creator

Author: Michael Kohlegger
Date: 2021-09
"""

from os import listdir
from os.path import isdir, join
from shutil import rmtree

from pytest import raises
from pytest import mark

from src.blob_creator.core import BlobFactory
from src.blob_creator.uploader import create_guid_named_file


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
    _, height, width = test_factory.get_kind_parameters()
    assert width == 512 and height == 512, message
    test_factory = BlobFactory(n=5, scatter=3, kind="alien")
    _, height, width = test_factory.get_kind_parameters()
    assert width == 417 and height == 476, message
    test_factory = BlobFactory(n=5, scatter=3, kind="boy")
    _, height, width = test_factory.get_kind_parameters()
    assert width == 600 and height == 600, message
    test_factory = BlobFactory(n=5, scatter=3, kind="marsian")
    _, height, width = test_factory.get_kind_parameters()
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
    size = 5
    scatter = 12
    kind = "monster"
    test_factory = BlobFactory(n=size, scatter=scatter, kind=kind)
    population_string = test_factory.get_population_string()
    test_value = f"blob_population_{kind}_n{size}_s{scatter}"
    assert population_string == test_value, message


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
    rmtree(dir_path)


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
    rmtree(dir_path)


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
    rmtree(dir_path)


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
        rmtree(test_factory.get_population_string())
        assert False, message


@mark.my_own
def test_negative_cols():
    """Test method"""
    message = "cols must be positive"
    with raises(AssertionError):
        test_factory = BlobFactory(n=5, scatter=12)
        test_factory.create_blobs()
        test_factory.export_data(cols=0)
        rmtree(test_factory.get_population_string())
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
    rmtree(test_factory.get_population_string())
    assert test_factory.get_png_status(), message


@mark.my_own
def test_png_switch_after_delete():
    """Test method"""
    message = "PNG switch must be False after deleting"
    test_factory = BlobFactory(n=5, scatter=12)
    test_factory.create_blobs()
    test_factory.delete_individual_pngs()
    rmtree(test_factory.get_population_string())
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
    rmtree(test_factory.get_population_string())
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
    rmtree(test_factory.get_population_string())
    assert count==size, message


@mark.my_own
def test_uuid_file_creation():
    """Test method"""
    message = "Filecopy with uuid name was not correctly created"
    test_factory = BlobFactory(n=5, scatter=2, kind="monster")
    test_factory.create_blobs()
    test_factory.export_data()
    dir_path = test_factory.get_population_string()
    file_name = "population.csv"
    new_file_name = create_guid_named_file(file=file_name, path=dir_path)
    dir_content = listdir(dir_path)
    rmtree(dir_path)
    assert new_file_name in dir_content, message


@mark.my_own
def test_cols_versus_n():
    """Test method"""
    message = "Software must not allow single-line population images"
    with raises(AssertionError):
        test_factory = BlobFactory(n=5, scatter=11, kind="monster")
        test_factory.create_blobs()
        test_factory.export_data(cols=5)
        rmtree(test_factory.get_population_string())
        assert False, message
