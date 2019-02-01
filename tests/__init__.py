from numpy.testing import assert_array_equal, assert_allclose


def assert_df_equals(df1, df2):
    assert df1.columns == df2.columns
    for values1, values2 in zip(df1._data.values(), df2._data.values()):
        kind = values1.dtype.kind
        if kind == 'f':
            assert_allclose(values1, values2)
        else:
            assert_array_equal(values1, values2)