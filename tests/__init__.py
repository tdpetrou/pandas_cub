from numpy.testing import assert_array_equal, assert_allclose


def assert_df_equals(df1, df2):
    assert df1.columns == df2.columns
    for col in df1.columns:
        if df1._column_info[col] == 'f':
            assert_allclose(df1[col].values, df2[col].values)
        else:
            assert_array_equal(df1[col].values, df2[col].values)