import operator
from collections import Counter
import numpy as np

__version__ = '0.0.1'


DTYPE_NAME = {'O': 'string', 'i': 'int', 'f': 'float', 'b': 'bool'}


class DataFrame:

    def __init__(self, values):
        """
        A DataFrame holds two dimensional heterogeneous data. Create it by
        passing a dictionary of NumPy arrays to the values parameter

        Parameters
        ----------
        values: dict
            A dictionary of strings mapped to NumPy arrays. The key will
            become the column name.
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
            if length != len(col_values):
                raise ValueError('All values must be the same length')

            if col_values.dtype.kind == 'U':
                col_values = col_values.astype('O')
            self._values[col_name] = col_values

            # map the column name to its single char 'kind'
            self._column_info[col_name] = col_values.dtype.kind

        # Allow for special methods for strings
        self.str = StringMethods(self)
        self._add_docs()

    def __len__(self):
        """
        Make the builtin len function work with our dataframe

        Returns
        -------
        int: the number of rows in the dataframe
        """
        for _, values in self._values.items():
            return len(values)

    @property
    def columns(self):
        """
        _values holds column names mapped to arrays
        take advantage of internal ordering of dictionaries to
        put columns in correct order in list. Only works in 3.6+

        Returns
        -------
        list of column names
        """
        return list(self._values)

    @columns.setter
    def columns(self, columns):
        """
        Must supply a list of columns as strings the same length
        as the current DataFrame

        Parameters
        ----------
        columns: list of strings

        Returns
        -------
        Nones
        """
        if not isinstance(columns, list):
            raise TypeError('New columns must be a list')
        if len(columns) != len(self.columns):
            raise ValueError(f'New column length must be {len(self.columns)}')
        else:
            for col in columns:
                if not isinstance(col, str):
                    raise TypeError('New column names must be strings')
        if len(columns) != len(set(columns)):
            raise ValueError('Column names must be unique')

        new_values = {}
        new_column_info = {}
        # code here
        for col, col_values in zip(columns, self._values.values()):
            new_values[col] = col_values
            new_column_info[col] = col_values.dtype.kind

        self._values = new_values
        self._column_info = new_column_info

    @property
    def shape(self):
        """

        Returns
        -------
        two-item tuple of number of rows and columns
        """
        return len(self), len(self.columns)

    def _repr_html_(self):
        """
        Used to create a string of HTML to nicely display the DataFrame
        in a Jupyter Notebook. Different string formatting is used for
        different data types.

        The structure of the HTML is as follows:
        <table>
            <thead>
                <tr>
                    <th>data</th>
                    ...
                    <th>data</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>{i}</strong></td>
                    <td>data</td>
                    ...
                    <td>data</td>
                </tr>
                ...
                <tr>
                    <td><strong>{i}</strong></td>
                    <td>data</td>
                    ...
                    <td>data</td>
                </tr>
            </tbody>
        <table>
        """
        html = '<table><thead><tr><th></th>'
        for col in self.columns:
            html += f"<th>{col:10}</th>"

        html += '</tr></thead>'
        html += "<tbody>"

        only_head = False
        num_head = 10
        num_tail = 10
        if len(self) <= 20:
            only_head = True
            num_head = len(self)

        for i in range(num_head):
            html += f'<tr><td><strong>{i}</strong></td>'
            for j, (col, values) in enumerate(self._values.items()):
                if self._column_info[col] == 'f':
                    html += f'<td>{values[i]:10.3f}</td>'
                elif self._column_info[col] == 'b':
                    html += f'<td>{values[i]}</td>'
                elif self._column_info[col] == 'O':
                    v = values[i]
                    if v is None:
                        v = 'None'
                    html += f'<td>{v:10}</td>'
                else:
                    html += f'<td>{values[i]:10}</td>'
            html += '</tr>'

        if not only_head:
            html += '<tr><strong><td>...</td></strong>'
            for i in range(len(self.columns)):
                html += '<td>...</td>'
            html += '</tr>'
            for i in range(-num_tail, 0):
                html += f'<tr><td><strong>{len(self) + i}</strong></td>'
                for j, (col, values) in enumerate(self._values.items()):
                    if self._column_info[col] == 'f':
                        html += f'<td>{values[i]:10.3f}</td>'
                    elif self._column_info[col] == 'b':
                        html += f'<td>{values[i]}</td>'
                    elif self._column_info[col] == 'O':
                        v = values[i]
                        if v is None:
                            v = 'None'
                        html += f'<td>{v:10}</td>'
                    else:
                        html += f'<td>{values[i]:10}</td>'
                html += '</tr>'

            html += '</tbody></table>'
        return html

    @property
    def values(self):
        """
        Returns
        -------
        A single 2D NumPy array (or 1D if 1 column) of the underlying data
        """
        vals = list(self._values.values())
        if len(vals) == 1:
            return vals[0]
        return np.column_stack(vals)

    @property
    def dtypes(self):
        """
        Returns
        -------
        A two-column DataFrame of column names in a column and
        their data type in the other
        """
        col_arr = np.array(self.columns)
        dtypes = np.array([DTYPE_NAME[dtype] for dtype in self._column_info.values()])
        return DataFrame({'Column Name': col_arr, 'Data Type': dtypes})

    def __getitem__(self, item):
        """
        Use the brackets operator to simultaneously select rows and columns

        A single string selects one column -> df['colname']
        A list of strings selects multiple columns -> df[['colname1', 'colname2']]
        A one column DataFrame of booleans that filters rows -> df[df_bool]

        Row and column selection simultaneously -> df[rs, cs]
            where cs and rs can be integers, slices, or a list of integers
            rs can also be a one-column boolean DataFrame

        Returns
        -------
        A subset of the original DataFrame
        """
        if isinstance(item, str):
            # select a single column -> df['colname']
            return DataFrame({item: self._values[item]})

        if isinstance(item, list):
            # select multiple columns -> df[['colname1', 'colname2']]
            return DataFrame({col: self._values[col] for col in item})

        if isinstance(item, DataFrame):
            if item.shape[1] != 1:
                raise ValueError('Can only pass a one column DataFrame for selection')
            elif item.values.dtype.kind != 'b':
                raise TypeError('DataFrame must be a boolean')

            new_values = {}
            arr = item.values
            for col, values in self._values.items():
                new_values[col] = values[arr]
            return DataFrame(new_values)

        if isinstance(item, tuple):
            # simultaneous selection of rows and cols -> df[rs, cs]
            if len(item) == 1:
                return self[item[0]]
            elif len(item) != 2:
                raise ValueError('Pass either a single string or a two-item tuple inside the '
                                 'selection operator.')
            row_selection = item[0]
            col_selection = item[1]
            if isinstance(row_selection, int):
                row_selection = [row_selection]
            elif isinstance(row_selection, DataFrame):
                row_selection = row_selection.values
            elif not isinstance(row_selection, (list, slice)):
                raise TypeError('Row selection must be either an int, slice, list, or DataFrame')

            if isinstance(col_selection, int):
                col_selection = [self.columns[col_selection]]
            elif isinstance(col_selection, list):
                new_col_selction = []
                for col in col_selection:
                    if isinstance(col, int):
                        new_col_selction.append(self.columns[col])
                    else:
                        new_col_selction.append(col)
                col_selection = new_col_selction
            elif isinstance(col_selection, slice):
                start = col_selection.start
                stop = col_selection.stop
                step = col_selection.step
                if isinstance(col_selection.start, str):
                    start = self.columns.index(col_selection.start)
                if isinstance(col_selection.stop, str):
                    stop = self.columns.index(col_selection.stop) + 1

                col_selection = self.columns[start:stop:step]
            elif isinstance(col_selection, str):
                col_selection = [col_selection]
            else:
                raise TypeError('Column selection must be either an int, list, slice, or string')

            new_values = {}
            for col in col_selection:
                if col not in self.columns:
                    raise KeyError(f'Column {col} does not exist')
                new_values[col] = self._values[col][row_selection]
            return DataFrame(new_values)
        else:
            raise TypeError('Select with either a string, a list, or a row and column '
                            'simultaneous selection')

    def _ipython_key_completions_(self):
        # allows for tab completion when doing df['c
        return self.columns

    def __setitem__(self, key, value):
        # adds a new column or a overwrites an old column
        if not isinstance(key, str):
            raise NotImplementedError('Only able to set a single column')
        else:
            if not isinstance(value, np.ndarray) or value.ndim != 1:
                raise TypeError('Can only set with a 1D NumPy array')
            elif len(value) != len(self):
                raise ValueError('Setting array must be same length as DataFrame')
            self._values[key] = value
            self._column_info[key] = value.dtype.kind

    def head(self, n=5):
        """
        Return the first n rows

        Parameters
        ----------
        n: int

        Returns
        -------
        DataFrame
        """

        return self[:n, :]

    def tail(self, n=5):
        """
        Return the last n rows

        Parameters
        ----------
        n: int

        Returns
        -------
        DataFrame
        """
        return self[-n:, :]

    #### AGGREGATION FUNCTIONS ####

    def min(self):
        return self._agg('min')

    def max(self):
        return self._agg('max')

    def mean(self):
        return self._agg('mean')

    def median(self):
        return self._agg('median')

    def sum(self):
        return self._agg('sum')

    def var(self):
        return self._agg('var')

    def std(self):
        return self._agg('std')

    def all(self):
        return self._agg('all')

    def any(self):
        return self._agg('any')

    def argmax(self):
        return self._agg('argmax')

    def argmin(self):
        return self._agg('argmin')

    def _agg(self, aggfunc):
        """
        Generic aggregation function that applies the
        aggregation to each column

        Parameters
        ----------
        aggfunc: str of the aggregation function name in NumPy

        Returns
        -------
        A DataFrame
        """
        new_values = {}
        func = getattr(np, aggfunc)
        for col, values in self._values.items():
            try:
                val = func(values)
            except TypeError:
                continue
            new_values[col] = np.array([val])
        return DataFrame(new_values)

    def isna(self):
        """
        Determines whether each value in the DataFrame is missing or not

        Returns
        -------
        A DataFrame of booleans the same size as the calling DataFrame
        """
        new_values = {}
        for col, values in self._values.items():
            if self._column_info[col] == 'O':
                new_values[col] = values == None
            else:
                new_values[col] = np.isnan(values)
        return DataFrame(new_values)

    def count(self):
        """
        Counts the number of non-missing values per column

        Returns
        -------
        A DataFrame
        """
        new_values = {}
        df = self.isna()
        length = len(self)
        for col, values in df._values.items():
            val = length - values.sum()
            new_values[col] = np.array([val])
        return DataFrame(new_values)

    def unique(self):
        """
        Finds the unique values of each column

        Returns
        -------
        A list of one-column DataFrames
        """
        dfs = []
        for col, values in self._values.items():
            new_values = np.unique(values)
            dfs.append(DataFrame({col: new_values}))
        if len(dfs) == 1:
            return dfs[0]
        return dfs

    def nunique(self):
        """
        Find the number of unique values in each column

        Returns
        -------
        A DataFrame
        """
        dfs = self.unique()
        if isinstance(dfs, DataFrame):
            return DataFrame({dfs.columns[0]: np.array([len(dfs)])})
        else:
            new_values = {}
            for df, col in zip(dfs, self.columns):
                new_values[col] = np.array([len(df)])

        return DataFrame(new_values)

    def value_counts(self, normalize=False):
        """
        Returns the frequency of each unique value for each column

        Parameters
        ----------
        normalize: bool
            If True, returns the relative frequencies (percent)

        Returns
        -------
        A list of DataFrames or a single DataFrame if one column
        """
        dfs = []
        for col, values in self._values.items():
            counts = Counter(values)

            keys = np.array(list(counts.keys()))
            raw_counts = np.array(list(counts.values()))
            if normalize:
                raw_counts = raw_counts / raw_counts.sum()
            df = DataFrame({col: keys, 'count': raw_counts}).sort_values('count', asc=False)
            dfs.append(df)
        if len(dfs) == 1:
            return dfs[0]
        return dfs

    def rename(self, columns):
        """
        Renames columns in the DataFrame

        Parameters
        ----------
        columns: dict
            A dictionary mapping the old column name to the new column name

        Returns
        -------
        A DataFrame

        """
        if not isinstance(columns, dict):
            raise TypeError('`columns` must be a dictionary')

        new_values = {}
        for col, values in self._values.items():
            if col in columns:
                new_values[columns[col]] = values
            else:
                new_values[col] = values
        return DataFrame(new_values)

    def drop(self, columns):
        """
        Drops one or more columns from a DataFrame

        Parameters
        ----------
        columns: str or list of strings

        Returns
        -------
        A DataFrame
        """
        if isinstance(columns, str):
            columns = [columns]
        elif not isinstance(columns, list):
            raise TypeError('`columns` must be either a string or a list')
        new_values = {}
        for col, values in self._values.items():
            if col not in columns:
                new_values[col] = values
        return DataFrame(new_values)

    ### non-aggregation methods

    def abs(self):
        """
        Takes the absolute value of each value in the DataFrame

        Returns
        -------
        A DataFrame
        """
        return self._non_agg('abs')

    def cummin(self):
        """
        Finds cumulative minimum by column

        Returns
        -------
        A DataFrame
        """

        return self._non_agg('minimum.accumulate')

    def cummax(self):
        """
        Finds cumulative maximum by column

        Returns
        -------
        A DataFrame
        """
        return self._non_agg('maximum.accumulate')

    def cumsum(self):
        """
        Finds cumulative sum by column

        Returns
        -------
        A DataFrame
        """
        return self._non_agg('cumsum')

    def clip(self, lower=None, upper=None):
        """
        All values less than lower will be set to lower
        All values greater than upper will be set to upper

        Parameters
        ----------
        lower: number or None
        upper: number or None

        Returns
        -------
        A DataFrame
        """
        return self._non_agg('clip', lower, upper)

    def round(self, n):
        """
        Rounds values to the nearest n decimals

        Returns
        -------
        A DataFrame
        """
        return self._non_agg('round', n)

    def copy(self):
        """
        Copies the DataFrame

        Returns
        -------
        A DataFrame
        """
        return self._non_agg('copy')

    def _non_agg(self, funcname, *args):
        """
        Generic non-aggregation function that applies
        each

        Parameters
        ----------
        funcname: str of NumPy name
        args: extra arguments for certain functions

        Returns
        -------
        A DataFrame
        """
        new_values = {}
        func = operator.attrgetter(funcname)(np)
        for col, values in self._values.items():
            try:
                val = func(values, *args)
            except TypeError:
                continue
            new_values[col] = val
        return DataFrame(new_values)

    def diff(self, n=1):
        """
        Take the difference between the current value and
        the nth value below it. The top n rows of the DataFrame
        are not returned

        Parameters
        ----------
        n: int

        Returns
        -------
        A DataFrame
        """
        new_values = {}
        for col, values in self._values.items():
            try:
                val = values[n:] - values[:-n]
            except TypeError:
                continue
            new_values[col] = val
        return DataFrame(new_values)

    def pct_change(self, n):
        """
        Take the percentage difference between the current value and
        the nth value below it. The top n rows of the DataFrame
        are not returned

        Parameters
        ----------
        n: int

        Returns
        -------
        A DataFrame
        """
        new_values = {}
        for col, values in self._values.items():
            try:
                val = (values[n:] - values[:-n]) / values[:-n]
            except TypeError:
                continue
            new_values[col] = val
        return DataFrame(new_values)

    #### ARITHMETIC AND COMPARISON OPERATORS ####

    def __add__(self, other):
        return self._oper('__add__', other)

    def __radd__(self, other):
        return self._oper('__radd__', other)

    def __sub__(self, other):
        return self._oper('__sub__', other)

    def __rsub__(self, other):
        return self._oper('__rsub__', other)

    def __mul__(self, other):
        return self._oper('__mul__', other)

    def __rmul__(self, other):
        return self._oper('__rmul__', other)

    def __truediv__(self, other):
        return self._oper('__truediv__', other)

    def __rtruediv__(self, other):
        return self._oper('__rtruediv__', other)

    def __floordiv__(self, other):
        return self._oper('__floordiv__', other)

    def __rfloordiv__(self, other):
        return self._oper('__rfloordiv__', other)

    def __pow__(self, other):
        return self._oper('__pow__', other)

    def __rpow__(self, other):
        return self._oper('__rpow__', other)

    def __gt__(self, other):
        return self._oper('__gt__', other)

    def __lt__(self, other):
        return self._oper('__lt__', other)

    def __ge__(self, other):
        return self._oper('__ge__', other)

    def __le__(self, other):
        return self._oper('__le__', other)

    def __ne__(self, other):
        return self._oper('__ne__', other)

    def __eq__(self, other):
        return self._oper('__eq__', other)

    def _oper(self, op, other):
        """
        Generic operator function

        Parameters
        ----------
        op: str name of special method
        other: the other object being operated on

        Returns
        -------
        A DataFrame
        """
        if isinstance(other, DataFrame):
            other = other.values
        new_values = {}
        for col, values in self._values.items():
            new_values[col] = getattr(values, op)(other)
        return DataFrame(new_values)

    def sort_values(self, by, asc=True):
        """
        Sort the DataFrame by one or more values

        Parameters
        ----------
        by: str or list of column names
        asc: boolean of sorting order

        Returns
        -------
        A DataFrame
        """
        if isinstance(by, str):
            order = np.argsort(self._values[by]).tolist()
        elif isinstance(by, list):
            cols = [self._values[col] for col in by[::-1]]
            order = np.lexsort(cols).tolist()
        else:
            raise TypeError('`by` must be a str or a list')

        if not asc:
            order = order[::-1]
        return self[order, :]

    def sample(self, n=None, frac=None, replace=False, seed=None):
        """
        Randomly samples rows the DataFrame

        Parameters
        ----------
        n: int
            number of rows to return
        frac: float
            Proportion of the data to sample
        replace: bool
            Whether or not to sample with replacement

        Returns
        -------
        A DataFrame
        """
        if seed:
            np.random.seed(seed)
        if frac is not None:
            if frac <= 0:
                raise ValueError('frac must be positive')
            n = int(frac * len(self))
        if n is not None:
            if not isinstance(n, int):
                raise TypeError('`n` must be an int')
            rows = np.random.choice(np.arange(len(self)), size=n, replace=replace).tolist()
        return self[rows, :]

    def pivot_table(self, rows=None, columns=None, values=None, aggfunc=None):
        """
        Grouping

        Parameters
        ----------
        rows: str of column name to group by
            Optional
        columns: str of column name to group by
            Optional
        values: str of column name to aggregate
            Required
        aggfunc: str of aggregation function

        Returns
        -------
        A DataFrame
        """
        if values is None:
            aggfunc = 'size'
        if rows is None and columns is None:
            raise ValueError('At least one of `rows` or `columns` must not be None')
        aggfunc_name = aggfunc
        if aggfunc in [None, 'size']:
            aggfunc = '__len__'
            aggfunc_name = 'size'

        def get_groups_one(group_values):
            group_values = np.sort(self._values[group_values])
            diff = group_values != np.roll(group_values, 1)

            # always keep first value as a group
            diff[0] = True
            groups = group_values[diff]

            # Use the diff variable as the group number, so the first value is always 0
            diff[0] = False
            group_labels = diff.cumsum()
            return groups, group_labels

        def group_multiple(rows, columns):
            row_values = self._values[rows]
            col_values = self._values[columns]
            order = np.lexsort([col_values, row_values])
            values_sorted = np.column_stack([row_values[order], col_values[order]])
            diff = values_sorted != np.roll(values_sorted, 1, axis=0)
            diff_final = np.any(diff, axis=1)
            diff_final[0] = True
            groups = values_sorted[diff_final]

            diff_final[0] = False
            group_labels = diff_final.cumsum()
            return groups, group_labels, order

        if values:
            agg_col = self._values[values]
        else:
            agg_col = np.empty(len(self))

        # group by one variable
        if columns is None:
            groups, group_labels = get_groups_one(rows)
            new_values = {rows: np.array(groups)}
            agg_values = []
            for i, group in enumerate(groups):
                agg_values.append(getattr(agg_col[group_labels == i], aggfunc)())
            new_values[aggfunc_name] = np.array(agg_values)

        elif rows is None:
            groups, group_labels = get_groups_one(columns)
            new_values = {}
            for i, group in enumerate(groups):
                new_val = getattr(agg_col[group_labels == i], aggfunc)()
                new_values[group] = np.array([new_val])
        else:
            groups, group_labels, order = group_multiple(rows, columns)
            num_groups = len(groups)
            unique_rows = np.unique(groups[:, 0])
            unique_cols = np.unique(groups[:, 1])
            new_values = {rows: unique_rows}
            for col in unique_cols:
                new_values[columns + '_' + col] = np.full(len(unique_rows), np.nan)
            row_position = {}
            for i, row in enumerate(unique_rows):
                row_position[row] = i

            agg_col = agg_col[order]
            for i in range(num_groups):
                cur_row, cur_col = groups[i, 0], groups[i, 1]
                cur_agg = getattr(agg_col[group_labels == i], aggfunc)()
                cur_row_pos = row_position[cur_row]
                new_values[columns + '_' + cur_col][cur_row_pos] = cur_agg

        return DataFrame(new_values)

    def _add_docs(self):
        agg_names = ['min', 'max', 'mean', 'median', 'sum', 'var',
                     'std', 'any', 'all', 'argmax', 'argmin']
        agg_doc = \
        """
        Find the {} of each column

        Returns
        -------
        DataFrame
        """
        for name in agg_names:
            getattr(DataFrame, name).__doc__ = agg_doc.format(name)


class StringMethods:

    def __init__(self, df):
        self._df = df

    def capitalize(self, col):
        return self._str_method('capitalize', col)

    def center(self, col, width, fillchar=None):
        if fillchar is None:
            fillchar = ' '
        return self._str_method('center', col, width, fillchar)

    def count(self, col, sub, start=None, stop=None):
        return self._str_method('count', col, sub, start, stop)

    def endswith(self, col, suffix, start=None, stop=None):
        return self._str_method('endswith', col, suffix, start, stop)

    def startswith(self, col, suffix, start=None, stop=None):
        return self._str_method('startswith', col, suffix, start, stop)

    def find(self, col, sub, start=None, stop=None):
        return self._str_method('find', col, sub, start, stop)

    def len(self, col):
        return self._str_method('__len__', col)

    def get(self, col, item):
        return self._str_method('__getitem__', col, item)

    def index(self, col, sub, start=None, stop=None):
        return self._str_method('index', col, sub, start, stop)

    def isalnum(self, col):
        return self._str_method('isalnum', col)

    def isalpha(self, col):
        return self._str_method('isalpha', col)

    def isdecimal(self, col):
        return self._str_method('isdecimal', col)

    def islower(self, col):
        return self._str_method('islower', col)

    def isnumeric(self, col):
        return self._str_method('isnumeric', col)

    def isspace(self, col):
        return self._str_method('isspace', col)

    def istitle(self, col):
        return self._str_method('istitle', col)

    def isupper(self, col):
        return self._str_method('isupper', col)

    def lstrip(self, col, chars):
        return self._str_method('lstrip', col, chars)

    def rstrip(self, col, chars):
        return self._str_method('rstrip', col, chars)

    def strip(self, col, chars):
        return self._str_method('strip', col, chars)

    def replace(self, col, old, new, count=None):
        if count is None:
            count = -1
        return self._str_method('replace', col, old, new, count)

    def swapcase(self, col):
        return self._str_method('swapcase', col)

    def title(self, col):
        return self._str_method('title', col)

    def upper(self, col):
        return self._str_method('upper', col)

    def zfill(self, col, width):
        return self._str_method('zfill', col, width)

    def encode(self, col, encoding='utf-8', errors='strict'):
        return self._str_method(col, encoding, errors)

    def _str_method(self, method, col, *args):
        old_values = self._df._values[col]
        new_values = []
        for val in old_values:
            if val is None:
                new_values.append(val)
            else:
                new_val = getattr(val, method)(*args)
                new_values.append(new_val)
        arr = np.array(new_values)
        if arr.dtype.kind == 'U':
            arr = arr.astype('O')
        return DataFrame({col: arr})


def read_csv(fn):
    values = {}
    with open(fn) as f:
        header = f.readline()
        column_names = header.strip('\n').split(',')
        for name in column_names:
            values[name] = []
        for line in f.readlines():
            for val, name in zip(line.strip('\n').split(','), column_names):
                values[name].append(val)
    new_values = {}
    for col, vals in values.items():
        try:
            new_values[col] = np.array(vals, dtype='int')
        except ValueError:
            try:
                new_values[col] = np.array(vals, dtype='float')
            except ValueError:
                new_values[col] = np.array(vals, dtype='O')
    return DataFrame(new_values)
