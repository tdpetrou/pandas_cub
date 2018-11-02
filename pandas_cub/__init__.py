import numpy as np

__version__ = '0.0.1'


DTYPE_NAME = {'O': 'string', 'i': 'int', 'f': 'float', 'b': 'bool'}


class DataFrame:

    def __init__(self, values):
        """
        Our DataFrame is constructed with a single parameter, `values`, a
        dictionary of column names as strings mapped to one-dimensional
        NumPy arrays. The DataFrame will hold four different data types
        with their single character **kind**:

        * bool (b)
        * int (i)
        * float (f)
        * string (O) (represented by NumPy object)

        Retrieve the `kind` of a NumPy array with `a.dype.kind`

        Steps
        * Verify that `values` is a dict
        * Verify that each key is a string
        * Verify that each value is a 1D NumPy array
        * If the array kind is 'U' change it to 'O'
        * Create a variable `_values` to store the data
        * Create another variable `_column_info` that maps the column name
        to the data type by converting the array kind with help from
        the constant dictionary `DTYPE_NAME`
        """

        # Check for correct input types
        if not isinstance(values, dict):
            raise TypeError("`data` must be a dictionary of 1-D NumPy arrays")
        else:
            for col_name, value in values.items():
                if not isinstance(col_name, str):
                    raise TypeError('All column names must be a string')
                if not isinstance(value, np.ndarray):
                    raise TypeError('All values must be a 1-D NumPy array')
                else:
                    if value.ndim != 1:
                        raise ValueError('Values must be a 1-D NumPy array')

        # Holds the data
        self._values = {}

        # maps the column name to its data type kind
        # b - bool, i - int, f - float, O - object
        self._column_info = {}

        # convert unicode array to object
        for i, (col_name, col_values) in enumerate(values.items()):
            if i == 0:
                length = len(col_values)
            if col_values.dtype.kind == 'U':
                self._values[col_name] = col_values.astype('O')
            else:
                self._values[col_name] = col_values

            if length != len(col_values):
                raise ValueError('All values must be the same length')

            # map the column name to its single char 'kind'
            self._column_info[col_name] = self._values[col_name].dtype.kind