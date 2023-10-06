from hamcrest import assert_that, is_


def check_mapping_db_to_api(reference: dict, compared: dict) -> None:
    """Checking the mapping of data from database in the request API

    Args:
        reference:  reference data, usually data from a database;
        compared:   compared data, data from other source.
    """
    assert_that(
        float(reference["price"]),
        is_(float(compared["price"])),
        reason=f'"price" not equal expected',
    )
    for key in ["id", "name", "description", "quantity"]:
        assert_that(
            reference[key], is_(compared[key]), reason=f'"{key}" not equal expected'
        )
