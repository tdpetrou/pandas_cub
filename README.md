# Build your own Pandas Cub

This repository contains a detailed project that teaches you how to build your own Python data analysis library.

## Target Audience

This project is targeted towards those who understand the fundamentals
of Python and wish to build their own DataFrame class from scratch.

## Pre-Requisites

* Intermediate knowledge of Python
* Helpful to have heard about special methods
* Helpful to have used NumPy and Pandas before

## Objectives

Most data scientists who use Python rely on Pandas. In this assignment, we will build Pandas Cub, a library that implements many of the most common and useful methods found in Pandas. Pandas Cub will:

* Have a DataFrame class with data stored in NumPy arrays
* Use special methods defined in the Python data model
* Have a nicely formatted display of the DataFrame in the notebook
* Select subsets of data with the brackets operator
* Implement aggregation methods - sum, min, max, mean, median, etc...
* Implement non-aggregation methods such as isna, unique, rename, drop
* Group by one or two columns
* Have methods specific to string columns

## Setting up the Development Environment

I recommend creating a new environment using the conda package manager. If you do not have conda, you can [download it here][0] along with the entire Anaconda distribution. Choose Python 3. When beginning development on a new library, it's a good idea to use a completely separate environment to write your code.

### Create the environment with the `environment.yml` file

Conda allows you to automate the environment creation by creating an `environment.yml` file. The contents of the file are minimal and are displayed below.

```yml
name: pandas_cub
dependencies:
- python=3.6
- pandas
- jupyter
- pytest
```

This file will be used to create a new environment named `pandas_cub`. It will install Python 3.6 in a completely separate folder in your file system along with pandas, jupyter, and pytest. There will actually be many more packages installed as those libraries have dependencies of their own.

Visit [this page][2] for more information on conda environments.

### Command to create new environment

In the top level directory of this repository, where the `environment.yml` file is located, run the following command from your command line.

`conda env create -f environment.yml`

The above command will take some time to complete. Once it completes, the environment will be created.

### List the environments

Run the command `conda env list` to show all the environments you have. There will be a `*` next to the active environment, which will likely be `base`, the default environment that everyone starts in.

### Activate the pandas_cub environment

Creating the environment does not mean it is active. You must activate in order to use it. Use the following command to activate it.

`conda activate pandas_cub`

You should see `pandas_cub` in parentheses preceding your command prompt. You can run the command `conda env list` to confirm that the `*` has moved to `pandas_cub`.

### Deactivate environment

You should only use the `pandas_cub` environment to develop this library. When you are done with this session, run the command `conda deactivate` to return to your default conda environment.

## Starting Pandas Cub

You will be editing a single file for this project - the `__init__.py` file
found in the `pandas_cub` directory. Each section of the tutorial is numbered below.

A completed version of the project can be found in the `pandas_cub_final` directory.

## Test-Driven Development with pytest

The completion of each part of this project is predicated upon passing the
tests written in the `test_dataframe.py` module inside the tests folder.

We will rely upon the [pytest library][1] to test our code. We installed it along with a command line tool with the same name during our environment creation.

[Test-Driven the development][3] is a popular approach for development. It involves writing tests first and then writing code that passes the tests.

### Testing

All the tests are located in the `test_dataframe.py` module found in the `tests` directory. To run all the tests in this file run the following on the command line.

`$ pytest tests/test_dataframe.py`

If you run this command right now, all the tests will fail. As you complete the steps in the project, you will start passing the tests. Once all the tests are passed, the project will be complete.

The pytest library has [rules for automated test discovery][4]. It isn't necessary to supply the path to the test module if your directories and module names follow those rules. You can simply run `pytest` to run all the tests in this library.

If you open up one of the test module `test_dataframe.py`, you will see the tests grouped under different classes. Each method of the classes represents exactly one test. To run all the tests within a single class, append two columns followed by the class name. The following is a concrete example:

`$ pytest tests/test_dataframe.py::TestDataFrameCreation`

It is possible to run just a single test by appending two more colons followed by the method name. Another concrete example follows:

`$ pytest tests/test_dataframe.py::TestDataFrameCreation::test_df_mix`

### Manually test in the Test Notebook

During development, it's good to have a place to manually experiment with your new code so you can see it in action. We will be using the Jupyter Notebook to quickly see how our DataFrame is changing.

## The answer is in pandas_cub_final

The `pandas_cub_final` directory contains the completed `__init__.py` file that contains the code that passes all the tests. Only look at this file after you have attempted to complete the section on your own.

## The `__init__.py` file

Open up the `__init__.py` file in the `pandas_cub` directory. This has the skeleton code of the entire project. You won't be defining your own classes or methods, but you will be filling out the bodies

### 1. DataFrame of NumPy arrays

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

* modify the `__init__` method
* Verify that `values` is a dict
* Verify that each key is a string
* Verify that each value is a 1D NumPy array
* Verify that each NumPy array is the same length
* If the array kind is 'U' change it to 'O'
* Create an instance variable `_values` to store the data as a dictionary
* Create another instance variable `_column_info`, a dictionary that maps the column name to the data type `kind` character.

Verify results with:  
`$ pytest tests/test_dataframe.py::TestDataFrameCreation::test_df_mix`  
`$ pytest tests/test_dataframe.py::TestDataFrameCreation::test_column_info`

### 2. Implement `__len__`

The special method `__len__` is used to make an object work with the builtin
`len` function. Have it return the number of rows in your DataFrame.

`$ pytest tests/test_dataframe.py::TestDataFrameCreation::test_len`

### 3. Return columns as a list

Use the property decorator to make a `columns` attribute that returns the 
names of the columns as a list.

`$ pytest tests/test_dataframe.py::TestDataFrameCreation::test_columns`

### 4. Set new column names

Use the property decorator `columns.setter` to set new columns. Assign it a list of strings.

Keep running tests. They should come in order.

### 5. The `shape` attribute

Use the property decorator to create a `shape` attribute that 
returns a two-item tuple of ints (rows, columns)

### 6. Uncomment `_repr_html_` method

This is a method specifically used by IPython to represent your object
in the Jupyter Notebook. You must return a string from this method.
This is already implemented. Just uncomment it and test the output in the
notebook and move on.

### 7. The `values` attribute

This is a public attribute that returns a single 2D NumPy array 
of all the columns. If there is just a single column, return a 
one dimensional array. The NumPy `column_stack` function can be helpful here.

### 8. The `dtypes` attribute

Return a two-column DataFrame. Put the column names under the 'Column Name'
column and the data type (bool, int, string, or float) under the 
column name 'Data Type'.

### 9. Subset selection with `__getitem__`

Python provides the `__getitem__` special method so that your object can
work with the brackets operator. This method gets passed a single
argument when it is called. Depending on the type of object passed
to it, use the following rules to determine what to do:

* A single string selects one column -> `df['colname']`
* A list of strings selects multiple columns -> `df[['colname1', 'colname2']]`
* A one column DataFrame of booleans that filters rows -> `df[df_bool]`
* Row and column selection simultaneously -> `df[rs, cs]`
* cs and rs can be integers, slices, or a list of integers
* rs can also be a one-column boolean DataFrame

Implement the first two items in the list and then copy and paste all
the code from pandas_cub_final.

### 10. Tab Completion

IPython helps us again by providing us with the `_ipython_key_completions_`
method. Return a list of the tab completions you would like to have 
available when inside the brackets operator.

### 11. Create or overwrite a column

To make an assignment with the brackets operator, Python makes the `__setitem__` method which accepts two values, the `key` and the `value`. We will only implement the simple case of adding a new column or overwriting an old one.

### 12. `head` and `tail` methods
Have these methods accept a single parameter `n` and return 
the first/last n rows.

### 13. Generic aggregation methods
Aggregation methods return a single value for each column. We will only 
implement column-wise aggregations and not row-wise.

Write a generic method `_agg` that accepts an aggregation function as a 
string. Use the  `getattr` function to get the actual NumPy function.

String columns with missing values will not work. Except this error and don't return columns where the aggregation cannot be found.

Defining the `_agg` method will make all the other aggregation methods work.

### 14. `isna` method
Return a DataFrame of the same shape that has a boolean for every 
single value in the DataFrame. Use `np.isnan` except in the case 
for strings which you can use a vectorized equality expression to `None`

### 15. `count` method
Return the number of non-missing values for each column

### 16. `unique` method
Return a list of one-column dataframes of unique values in 
each column. If there is a single column. Return just the DataFrame

### 17. `nunique` method
Return the number of unique values for each column

### 18. `value_counts` method
Return a list of two-column DataFrames with the first column name
as the name of the original column and the second column name 'count'
containing the number of occurrences for each value. 

Use the `Counter` method of the `collections` module. Return the DataFrames
with sorted values from greatest to least. You hold off on sorting
until you have defined the `sort_values` method.

Accept a boolean parameter `normalize` that returns relative 
frequencies when `True`.

If the calling DataFrame has a single column, return a single DataFrame.

### 19. `rename` method
Accept a dictionary of old column names mapped to new column names. Return a new DataFrame

### 20. `drop` method
Accept a list of column names and return a DataFrame without those columns

### 21. Non-aggregation methods
There are several non-aggregation methods that function similarly. Create a
generic method `_non_agg` that can implement:

* `abs`
* `cummin`
* `cummax`
* `cumsum`
* `clip`
* `round`
* `copy`

The `cummin` and `cummax` functions in NumPy necessitate dot notation to reach. We cannot use `getattr` for this and instead have to use the more specialized
`attrgetter` from the `operator` library.

 Notice that some of these have parameters. Collect them with `*args`.
 
### 22. `diff` and `pct_change` methods
Return the raw difference or percentage change between rows given a distance `n`. You can drop the first n rows.
 
### 23. Arithmetic and Comparison Operators
All the arithmetic and comparison operators have special methods available. For instance `__add__` is used for the plus sign, and `__le__` is used for less than or equal to. Each of these methods accepts a single other parameter.
 
 Write a generic method, `_oper` that works with each of these methods.
 
### 24. `sort_values` method
This method takes two parameters. The sorting column or columns (as a string or list) and a boolean for the direction to sort. You will need to use NumPy's `argsort` to get the order of the sort for a single column and `lexsort` to sort multiple columns.
 
### 25. `sample` method
This method randomly samples the rows of the DataFrame. You can either choose an exact
number to sample with `n` or a fraction with `frac`. Sample with replacement by using
the boolean `replace`. You can also set the random number seed.

### 26. `str` accessor
In the `__init__` method, there was a line that created `str` as an instance variable with the `StringMethods` type.

All the string methods use the generic `_str_method` method which accepts the name of the method, the column name and any method-specific parameters.

Modify the generic `_str_method` to make all the other string methods work.

### 27. `pivot_table` method
This is by far the most complex method to implement. Allow `rows` and `columns` to be column names who's unique values form the groups. Aggregate the column passed to the `values` parameter with the `aggfunc` string.

Allow either `rows` or `columns` to be `None`. If `values` or `aggfunc` is `None` then find the frequency (like in `value_counts`).

### 28. Automatically add documentation
This method is already completed and automatically adds documentation to the aggregation methods by setting the `__doc__` attribute.

### 29. Reading simple CSVs
Implement the `read_csv` function by reading through each line. Assume the first line has the column names. Use the second line to assign the data types of each column.

[0]: https://www.anaconda.com/distribution/
[1]: https://docs.pytest.org/en/latest/getting-started.html
[2]: https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html
[3]: https://en.wikipedia.org/wiki/Test-driven_development
[4]: https://docs.pytest.org/en/latest/goodpractices.html#conventions-for-python-test-discovery