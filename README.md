# Pandas Cub
ODSC West Tutorial, San Francisco, CA, Nov 3, 2018 2 p.m. by Ted Petrou

### Target Audience
This talk is targeted towards those with a solid understanding of the fundamentals
of Python. Previous experience with NumPy and Pandas will be very helpful.

### Pre-Requisites
* Intermediate knowledge of Python
* Helpful to have heard about special methods
* Helpful to have used NumPy and Pandas before

### System Requirements
* Python 3.6+ along with NumPy, Pandas
* Recommended to have installed Pytest as well

### Objectives
Most data scientists who use Python are heavy utilizers of Pandas, but might 
not know how to build their own data analysis library. In this tutorial we will 
build Pandas Cub, a library modeled after Pandas. In this tutorial, we will:

*  Define our own DataFrame class with NumPy arrays holding heterogeneous data
* Use special methods defined in the Python data model to make our own DataFrame 
work with other built-in operators and functions
* Have a nicely formatted display in the notebook
* Be able to select subsets of data with the brackets operator using strings, ints, 
lists, and single-column boolean DataFrames
* Implement all the common aggregation methods - sum, min, max, mean, median, etc...
* Implement non-aggregation methods such as isna, unique, rename, drop
* Group by one or two columns
* Have a special string accessor for specific string methods

## Structure of Tutorial

We will build each component of our DataFrame one at a time. There will be instructions
both here and in the docustrings on how to complete each step.

### Test Driven Development with pytest
The completion of each part of this project is predicated upon passing the
tests written in the test_dataframe.py and test_strings.py modules inside the 
test folder.

To run the test suite you will need to install the [pytest library][1]. The will also
install a command line tool with the same name.

### Testing
If you open up one of the test modules, you will see the tests grouped in 
different classes. To run all the tests in a single class, run the following on
the command line:

```
$pytest tests/test_dataframe.py::TestDataFrameCreation
```

To run a single test, you can do the following:

```
$pytest tests/test_dataframe.py::TestDataFrameCreation::test_df_mix
```

### Manually test in the Test Notebook

## Starting Pandas Cub
You will be editing a single file for this project - the `__init__.py` file
found in the pandas_cub directory. Each section of the tutorial is numbered 
below. Once you finish a section, you will test your code by running pytest.

A completed version of the project can be found in the pandas_cub_final directory. 
You can check your work with that file once you have completed each step. Take 
note that there might be more code.  

### 1. Dictionary of NumPy arrays

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



[1]: https://docs.pytest.org/en/latest/getting-started.html