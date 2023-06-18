import os

import pandas as pd
import numpy as np
import math
from typing import Sized, Iterable, Union, Optional, Any, Type, Tuple, List

class Fileread:
    """
        Parse file data to a python usable output.

        Support for xlsx, csv and txt, selecting specific columns and/or rows,
        specifying header and delimiter. Dependencies: pandas and numpy.

        :rtype: object
        :param path:
            Path of the file(s). If multiple files in either a tuple of str or
            list of str.
        :param cols:
            Input in a tuple for more than one column or in int/str for one col
            input in (int/str, int/str) OR int/str OR ((int, label), (int, label))
            OR a combination.

            Used to specify the index/label of columns to append to dict
            Note: keys will be ints or strings.
        :param rows:
            Input in a tuple. ((row, label), (row, label), ...)
            OR (row, row, ...) OR combination of ((row, label), row)

            Used to specify the index of the row (int) and give a label (str) to
            append to dict. Note, keys of the rows will be strings.
        :param head:
            Boolean, default True change if the csv file doesn't have an header.
        :param delimiter:
            Default: ';', change for custom delimiter must be str.
        :param: start_row:
            Index of starting row, default int(0).
        :param: output:
            output format, either "dict" or "dictionary" for dictionary;
            "np" or "numpy" for a numpy matrix (possibly with NaN values);
            "df" or "dataframe" or "pd" or "pandas" for a pandas dataframe.
        :param: dtype:
            The data type of the output, default 'object';
            future implementations may include auto detect unless specified.
        :param: allow_duplicates:
            Allow duplicate columns to be added to the dictionary default False.
        :param: include_all:
            Unless cols or row is specified include all columns/rows from file
            default False.
        :return:
            Dict with all or specified rows/cols.
        """

    # TODO: documentation, docstrings and write support.
    def __init__(self, path: Union[list, str, tuple] = None,
                 cols: Union[list, str, tuple] = None,
                 rows: Union[list, str, tuple] = None,
                 delimiter: str = ';', head: bool = True,
                 start_row: int = None,
                 output: str = 'dict', dtype: str = 'object',
                 **kwargs):
        self.cols = cols
        self.rows = rows

        self.path = path
        self.delimiter = delimiter

        self.dtype = dtype
        self.head = head

        self.duplicate = False
        self.all = False

        # Check kwargs
        if "allow_duplicates" in kwargs:
            self.test_inp(kwargs["allow_duplicates"], bool, "Allow duplicates",
                          True)
            self.duplicate = kwargs["allow_duplicates"]

        if "include_all" in kwargs:
            self.test_inp(kwargs["include_all"], bool, "Include all",
                          True)
            self.all = kwargs["include_all"]

        if self.path.__class__.__name__ in 'list' or os.path.isdir(self.path):
            # Test inputs (row currently only supports all file wide rows)
            # TODO: dict row support
            # TODO: multifile str support
            if os.path.isdir(self.path):
                self.path = [p for p in os.listdir(self.path) if p.endswith((".csv", ".txt", ".xlsx", ".dat"))]

            self.test_inp(cols, (dict, type(None)), "cols")
            self.test_inp(rows, (type(None), list, tuple, int), "row")

            # try:
            #     assert len(cols) == len(path)
            # except AssertionError:
            #     if not self.all:
            #         raise IndexError("Length of 'path' should equal length of"
            #                          " 'cols' in multi file mode but equals: "
            #                          "{0} and {1}. If you meant to include all files"
            #                          "set include_all to True".format(len(path), len(cols)))
            #     else:
            #         # TODO: include_all support
            #         pass

            # init talley list
            df_list = []
            col_count, it = [0, ], 0
            heads = []

            # Read files
            for file in self.path:
                file = path + "/" + file
                df, head_h = self.arr__init__(file, start_row, self.head)
                df.columns = range(col_count[it], col_count[it] + len(df.columns))
                col_count.append(len(df.columns) + col_count[-1])
                df_list.append(df)
                heads.extend(head_h)
                it += 1
            df = pd.DataFrame()

            # Indexes of requested cols, if cols is None, all cols are selected
            if cols is not None:
                self.cols = cols[0]
                for i in range(1, len(cols)):
                    self.cols += (np.array(cols[i]) + col_count[i]).tolist()
            else:
                self.cols = list(range(col_count[-1]))

            # Combine dataframes
            for dataframe in df_list:
                df = pd.concat([df, dataframe], ignore_index=True, axis=1)

            # Init final values used in self.read_cols and self.read_rows
            self.heads = heads
            self.arr = df.to_numpy()
            self.arr_t = self.arr.transpose()
            self.output = output

            self.data_dict = dict()


        elif path is not None:
            df, heads = self.arr__init__(path, start_row, self.head)

            self.heads = heads
            self.arr = df.to_numpy()
            self.arr_t = self.arr.transpose()
            self.output = output

            self.data_dict = dict()

    def __call__(self, read_all=False):
        if self.cols is not None:
            self.read_cols()

        if self.rows is not None:
            self.read_rows()

        if (self.rows is None and self.cols is None) or read_all:
            for i in range(len(self.heads)):
                self.data_dict[self.heads[i]] = self.arr_t[i][
                    ~pd.isnull(self.arr_t[i])].astype(self.dtype)

        if self.output is not None:
            self.test_inp(self.output, str, 'Output', True)
            if self.output in ('dict', 'dictionary'):
                return self.data_dict
            elif self.output in ('df', 'dataframe'):
                df = pd.DataFrame(dict([(i, pd.Series(j))
                                        for i, j in self.data_dict.items()]))
                return df
            elif self.output in ('matrix', 'array', 'arr', 'numpy', 'np'):
                matrix = np.zeros(
                    (len(self.data_dict),
                     max([len(i) for i in self.data_dict.values()]))
                )
                matrix.fill(np.nan)

                # Fill the array with values.
                for i in range(len(self.data_dict)):
                    for j in range(len(list(self.data_dict.values())[i])):
                        matrix[i, j] = list(self.data_dict.values())[i][j]
                return matrix.transpose()
            else:
                raise Exception('Expected output in df or dict not in %s'
                                % self.output)

    def arr__init__(self, path: str, start_row: int, head: bool,
                    df: pd.DataFrame = None) -> Tuple[Union[Optional[str], Any],
                                                      Union[list, List[int]]]:
        """"
        Turn the file into a pandas dataframe.

        :rtype: Pandas.DataFrame
        :param: path:
            Path str
        :param: start_row:
            Int for the starting row, default 0
        :param: head:
            List with str of header values
        :param: df:
            Append the current path file to this dataframe
        :return:
            Dataframe created from the path file and input arg df.
        """
        with open(path, mode='r') as f:
            if start_row is not None:
                self.test_inp(start_row, int, 'start row')
            else:
                start_row = 0
            if path.split('.')[1] in ('csv', 'txt'):
                df = pd.read_csv(f, delimiter=self.delimiter,
                                 skiprows=range(start_row), dtype=str)
            elif path.split('.')[1] == 'xlsx':
                df = pd.read_excel(path, skiprows=range(start_row), dtype=str)
            else:
                raise Exception('Expected .csv or .xlsx, got .' +
                                path.split('.')[1])

            if head:
                heads = list(df.columns)
            else:
                # Make a numerical list instead of headers
                heads = [i for i in range(len(list(df.columns)))]

                # Add the first row at the top
                df.loc[-1] = list(df.columns)
                df.index = df.index + 1
                df = df.sort_index()
            f.close()
        return df, heads

    def read_cols(self):
        """
        Read specific columns and append to the dict
        :return:
        Data_dict
        """
        # Correctly format the columns
        if not isinstance(self.cols, (tuple, list)):
            self.cols = (self.cols,)

        for i in self.cols:
            if isinstance(i, int):
                # Test if the input isn't out of range.
                try:
                    self.arr_t[i]
                except IndexError:
                    print('\x1b[31m' +
                          'IndexError: There are %s columns, %s is out of'
                          ' bounds. Continuing...  ' % (i, len(self.arr_t))
                          + '\x1b[0m')
                    continue

                if self.heads[i] not in self.data_dict:
                    self.data_dict[self.heads[i]] = self.arr_t[i][
                        ~pd.isnull(self.arr_t[i])
                    ].astype(self.dtype)
                elif self.duplicate:
                    dupe_count = self.heads[0:i].count(self.heads[i])
                    self.data_dict[str(self.heads[i]) + ".%s"%dupe_count] = \
                        self.arr_t[i][~pd.isnull(self.arr_t[i])].astype(self.dtype)
                else:
                    print('\x1b[33m' +
                          'Column with index %s already added to dict, '
                          'Continuing...  ' % i
                          + '\x1b[0m')
                    continue

            elif isinstance(i, (tuple, list)):
                if len(i) == 2:
                    if isinstance(i[0], int):
                        if self.heads[i[0]] not in self.data_dict:
                            self.data_dict[i[1]] = self.arr_t[i[0]][
                                ~pd.isnull(self.arr_t[i[0]])
                            ].astype(self.dtype)
                        elif self.duplicate:
                            self.data_dict[i[1]] = self.arr_t[i[0]][
                                ~pd.isnull(self.arr_t[i[0]])
                            ].astype(self.dtype)
                        else:
                            print('\x1b[33m' +
                                  'Column "%s" already added to dict,'
                                  ' Continuing...  ' % i[1]
                                  + '\x1b[0m')
                            continue
                    else:
                        self.test_inp(i[0], int, 'columns', True)
                else:
                    raise Exception('Expected tuple of length 2 got length: %s'
                                    % len(i))
            elif isinstance(i, str) and self.head is True:
                try:
                    assert i in self.heads
                except AssertionError:
                    print('\x1b[31m' +
                          'LookupError: "%s" not in csv file continuing...' % i
                          + '\x1b[0m')
                    continue

                if i not in self.data_dict:
                    self.data_dict[i] = self.arr_t[
                        self.heads.index(i)
                    ][
                        ~pd.isnull(self.arr_t[self.heads.index(i)])
                    ].astype(self.dtype)
                elif self.duplicate:
                    dupe_count = self.heads[0:self.heads.index(i)].count(i)
                    self.data_dict[i + '.%s'%dupe_count] = self.arr_t[
                        self.heads.index(i)
                    ][
                        ~pd.isnull(self.arr_t[self.heads.index(i)])
                    ].astype(self.dtype)
                else:
                    print('\x1b[33m' +
                          'Column "%s" already added to dict,'
                          ' Continuing...  ' % i
                          + '\x1b[0m')
                    continue
            else:
                if self.head:
                    self.test_inp(i, (int, list, tuple, str), 'columns')
                else:
                    self.test_inp(i, (int, list, tuple), 'columns')

        return self.data_dict

    def read_rows(self):
        """
        Read specific rows.
        :return:
            Data_dict
        """
        # Format the rows
        if not isinstance(self.rows, (tuple, list)):
            self.rows = ((self.rows,),)
        row_list = list()
        for j in self.rows:
            if not isinstance(j, (tuple, list)):
                row_list.append((j,))
            else:
                row_list.append(j)

        for i in row_list:
            if len(i) == 2:
                if isinstance(i[0], int) \
                        and isinstance(i[1], (str, int, float, bytes)):
                    try:
                        self.arr[i[0]]
                    except IndexError:
                        print('\x1b[31m' +
                              'IndexError: There are %s rows,'
                              ' %s is out of bounds.' % (len(self.arr), i[0])
                              + '\x1b[0m')
                        continue

                    if not i[1] in self.data_dict:
                        self.data_dict[i[1]] = self.arr[i[0]].astype(self.dtype)
                    else:
                        print('\x1b[33m' +
                              'Row %s already added to dict continuing...'
                              % i[1]
                              + '\x1b[0m')
                        continue
                else:
                    self.test_inp(i[0], int, 'rows', True)
            elif len(i) == 1:
                if isinstance(i[0], int):
                    try:
                        self.arr[i[0]]
                    except IndexError:
                        print('\x1b[31m' +
                              'IndexError: There are '
                              + str(len(self.arr))
                              + ' rows, ' + str(i[0]) +
                              ' is out of bounds. Continuing...  '
                              + '\x1b[0m')
                        continue

                    if not 'r_' + str(row_list.index(i)) in self.data_dict:
                        self.data_dict['r_' + str(row_list.index(i))] \
                            = self.arr[i[0]].astype(self.dtype)
                    else:
                        print('\x1b[33m' +
                              'Row with index ' + str(i[0]) + ' '
                              + 'already added to dict, Continuing...  '
                              + '\x1b[0m')
                        continue
                else:
                    self.test_inp(i, int, 'row', True)
            else:
                raise Exception('Expected input of length 1 or 2 got %s'
                                % len(i))
        return self.data_dict

    def writer(self, cols=None, rows=None, single=None, new_file=None,
               table=None):
        """
        Write columns and/or rows in a csv or txt file.
        :param cols:
            input (col nr, iterable)
            OR
            iterable
        :param rows:
            input (row nr, iterable)
            OR
            iterable
        :param single:
            input ((row, col), int;str;float;byte)
        :param table:
            input (pandas df or numpy matrix, (optional positional args))
            e.g. df or (df, 'row=3') or (df, 'col=4') or
            (df, ('row=2', 'col=3'))
            NOTE the position is the position of the top left entry.
        :param new_file:
            input (file name, type) OR filename
            e.g. (DataSheet, csv) or (Datasheet.csv)
        """

        if new_file is not None and isinstance(new_file, tuple):
            self.path = str(new_file[0]) + '.' + str(new_file[1])
        elif new_file is not None and isinstance(new_file, str):
            self.path = new_file
        elif new_file is not None:
            self.test_inp(new_file, (tuple, list, str), 'path', True)

        if new_file is None:
            self.output = 'df'
            df = self.__call__(read_all=True)
            num_list, head = False, []
            if cols is not None:
                if isinstance(cols, (tuple, list)):
                    for i in cols:
                        if isinstance(i, dict):
                            head += list(i.keys())
                            values = list(i.values())
                            index = None
                            for j in range(len(values)):
                                if not isinstance(values[j], (list, tuple)):
                                    values[j] = [values[j]]
                            max_value = [len(j) for j in values] \
                                .index(max([len(j) for j in values]))
                            for j in range(len(list(i.values())[max_value])):
                                if math.isnan(list(i.values())[max_value][j]):
                                    index = j
                                    print(j, "J")
                                else:
                                    pass
                            if index is None:
                                index = max([len(j) for j in values])

                        elif isinstance(i, (list, tuple)):
                            head.append(cols.index(i))
                        else:
                            num_list = True
                            head = cols[0]
                    if num_list:
                        pass
                    else:
                        for i in range(len(head)):
                            if isinstance(head[i], tuple):
                                self.test_inp(head[i][0], str, 'header')
                                self.test_inp(head[i][1], int, 'location')

                                self.data_dict[self.heads[head[i][1]]] = \
                                    values[i]
                                df = pd.DataFrame(dict([(i, pd.Series(j))
                                                        for i, j in
                                                        self.data_dict.items()]))
                                df.rename(columns={head[i][1]: head[i][0]})
                                df = df.truncate(after=index - 1)
            df.to_csv(self.path, sep=self.delimiter, index=False)

    @staticmethod
    def test_inp(test_obj, test_if, name_inp, value=False):
        """
        Test a value if it returns false raise an exception
        :param: test_obj
        Object to be tested.
        :param:test_if
        The input that is tested to be equal as. (in int, str, double etc)
        :param: value
        Bool, if True the exception also shows test_obj not recommended for
        long lists.
        :param: name_inp
        String, the informal name of the object shown in exception.
        """
        assert isinstance(name_inp, str)
        try:
            assert isinstance(test_obj, test_if)
        except AssertionError:
            if not isinstance(test_if, tuple):
                if not value:
                    raise TypeError(
                        'Expected %s for %s but got %s' %
                        (test_if.__name__,
                         name_inp, test_obj.__class__.__name__)
                    )
                else:
                    raise TypeError(
                        'Expected %s for %s but got type %s with'
                        ' value: %s' %
                        (test_if.__name__, name_inp,
                         test_obj.__class__.__name__, test_obj)
                    )
            else:
                test_if = [i.__name__ for i in test_if]
                if not value:
                    raise TypeError(
                        'Expected %s for %s but got %s' %
                        (', '.join(test_if), name_inp,
                         test_obj.__class__.__name__)
                    )
                else:
                    raise TypeError(
                        'Expected %s for %s but got type %s with'
                        ' value: %s' %
                        (', '.join(test_if), name_inp,
                         test_obj.__class__.__name__, test_obj)
                    )
        return None

    @staticmethod
    def filter_nan(arr: Iterable) -> np.array:
        """
        Filter nan's out of array
        :param arr: Numpy array
        :return: Filtered array
        """
        return np.array[lambda v: v == v, arr]


class csvread(Fileread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print('\x1b[33m' +
              'UPDATE: csvread is now called Fileread! From update 0.0.4 and on'
              ' it will only be possible to call this function with "Fileread".'
              + '\x1b[0m')
