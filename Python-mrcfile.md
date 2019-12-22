#From https://github.com/ccpem/mrcfile

mrcfile.py

Build Status Documentation Python Versions  Python Package Index  conda-forge

mrcfile is a Python implementation of the MRC2014 file format, which is used in structural biology to store image and volume data.

It allows MRC files to be created and opened easily using a very simple API, which exposes the file's header and data as numpy arrays. The code runs in Python 2 and 3 and is fully unit-tested.

This library aims to allow users and developers to read and write standard-compliant MRC files in Python as easily as possible, and with no dependencies on any compiled libraries except numpy. You can use it interactively to inspect files, correct headers and so on, or in scripts and larger software packages to provide basic MRC file I/O functions.

Key Features

Clean, simple API for access to MRC files
Easy to install and use
Validation of files according to the MRC2014 format
Seamless support for gzip and bzip2 files
Memory-mapped file option for fast random access to very large files
Asynchronous opening option for background loading of multiple files
Runs in Python 2 & 3, on Linux, Mac OS X and Windows
Installation

The mrcfile library is available from the Python package index:

pip install mrcfile
Or from conda-forge:

conda install --channel conda-forge mrcfile
It is also included in the ccpem-python environment in the CCP-EM software suite.

The source code (including the full test suite) can be found on GitHub.

Basic usage

The easiest way to open a file is with the mrcfile.open and mrcfile.new functions. These return an MrcFile object which represents an MRC file on disk.

To open an MRC file and read a slice of data:

>>> import mrcfile
>>> with mrcfile.open('tests/test_data/EMD-3197.map') as mrc:
...     mrc.data[10,10]
...
array([ 2.58179283,  3.1406002 ,  3.64495397,  3.63812137,  3.61837363,
        4.0115056 ,  3.66981959,  2.07317996,  0.1251585 , -0.87975615,
        0.12517013,  2.07319379,  3.66982722,  4.0115037 ,  3.61837196,
        3.6381247 ,  3.64495087,  3.14059472,  2.58178973,  1.92690361], dtype=float32)
To create a new file with a 2D data array, and change some values:

>>> with mrcfile.new('tmp.mrc') as mrc:
...     mrc.set_data(np.zeros((5, 5), dtype=np.int8))
...     mrc.data[1:4,1:4] = 10
...     mrc.data
...
array([[ 0,  0,  0,  0,  0],
       [ 0, 10, 10, 10,  0],
       [ 0, 10, 10, 10,  0],
       [ 0, 10, 10, 10,  0],
       [ 0,  0,  0,  0,  0]], dtype=int8)
The data will be saved to disk when the file is closed, either automatically at the end of the with block (like a normal Python file object) or manually by calling close(). You can also call flush() to write any changes to disk and keep the file open.

To validate an MRC file:

>>> mrcfile.validate('tests/test_data/EMD-3197.map')
File does not declare MRC format version 20140: nversion = 0
False

>>> mrcfile.validate('tmp.mrc')
True
Documentation

Full documentation is available on Read the Docs.

Citing mrcfile

If you find mrcfile useful in your work, please cite:

Burnley T, Palmer C & Winn M (2017) Recent developments in the CCP-EM software suite. Acta Cryst. D73:469--477. doi: 10.1107/S2059798317007859

Contributing

Please use the GitHub issue tracker for bug reports and feature requests, or email CCP-EM.

Code contributions are also welcome, please submit pull requests to the GitHub repository.

To run the test suite, go to the top-level project directory (which contains the mrcfile and tests packages) and run python -m unittest tests. (Or, if you have tox installed, run tox.)

Licence

The project is released under the BSD licence.
