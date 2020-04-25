#From https://github.com/ccpem/mrcfile. https://mrcfile.readthedocs.io/en/latest/usage_guide.html

# Usage Guide

This is a detailed guide to using the mrcfile Python library. For a brief introduction, see the overview.

Opening MRC files
MRC files should usually be opened using the mrcfile.new() or mrcfile.open() functions. These return an instance of the MrcFile class, which represents an MRC file on disk and makes the file’s header, extended header and data available for read and write access as numpy arrays:
```
>>> # First, create a simple dataset
>>> import numpy as np
>>> example_data = np.arange(12, dtype=np.int8).reshape(3, 4)

>>> # Make a new MRC file and write the data to it:
>>> import mrcfile
>>> with mrcfile.new('tmp.mrc') as mrc:
...     mrc.set_data(example_data)
...
>>> # The file is now saved on disk. Open it again and check the data:
>>> with mrcfile.open('tmp.mrc') as mrc:
...     mrc.data
...
array([[ 0,  1,  2,  3],
       [ 4,  5,  6,  7],
       [ 8,  9, 10, 11]], dtype=int8)
```
The new() and open() functions can also handle gzip- or bzip2-compressed files very easily:
```
>>> # Make a new gzipped MRC file:
>>> with mrcfile.new('tmp.mrc.gz', compression='gzip') as mrc:
...     mrc.set_data(example_data * 2)
...
>>> # Open it again with the normal open function:
>>> with mrcfile.open('tmp.mrc.gz') as mrc:
...     mrc.data
...
array([[ 0,  2,  4,  6],
       [ 8, 10, 12, 14],
       [16, 18, 20, 22]], dtype=int8)

>>> # Same again for bzip2:
>>> with mrcfile.new('tmp.mrc.bz2', compression='bzip2') as mrc:
...     mrc.set_data(example_data * 3)
...
>>> # Open it again with the normal open function:
>>> with mrcfile.open('tmp.mrc.bz2') as mrc:
...     mrc.data
...
array([[ 0,  3,  6,  9],
       [12, 15, 18, 21],
       [24, 27, 30, 33]], dtype=int8)
```
MrcFile objects should be closed when they are finished with, to ensure any changes are flushed to disk and the underlying file object is closed:
```
>>> mrc = mrcfile.open('tmp.mrc', mode='r+')
>>> # do things...
>>> mrc.close()
```
As we saw in the examples above, MrcFile objects support Python’s with statement, which will ensure the file is closed properly after use (like a normal Python file object). It’s generally a good idea to use with if possible, but sometimes when running Python interactively (as in some of these examples), it’s more convenient to open a file and keep using it without having to work in an indented block. If you do this, remember to close the file at the end!

There’s also a flush() method that writes the MRC data to disk but leaves the file open:
```
>>> mrc = mrcfile.open('tmp.mrc', mode='r+')
>>> # do things...
>>> mrc.flush()  # make sure changes are written to disk
>>> # continue using the file...
>>> mrc.close()  # close the file when finished
```
For most purposes, the top-level functions in mrcfile should be all you need to open MRC files, but it is also possible to directly instantiate MrcFile and its subclasses, GzipMrcFile, Bzip2MrcFile and MrcMemmap:
```
>>> with mrcfile.mrcfile.MrcFile('tmp.mrc') as mrc:
...     mrc
...
MrcFile('tmp.mrc', mode='r')

>>> with mrcfile.gzipmrcfile.GzipMrcFile('tmp.mrc.gz') as mrc:
...     mrc
...
GzipMrcFile('tmp.mrc.gz', mode='r')

>>> with mrcfile.bzip2mrcfile.Bzip2MrcFile('tmp.mrc.bz2') as mrc:
...     mrc
...
Bzip2MrcFile('tmp.mrc.bz2', mode='r')

>>> with mrcfile.mrcmemmap.MrcMemmap('tmp.mrc') as mrc:
...     mrc
...
MrcMemmap('tmp.mrc', mode='r')
```
# Dealing with large files
mrcfile provides two ways of improving performance when handling large files: memory mapping and asynchronous (background) opening. Memory mapping treats the file’s data on disk as if it is already in memory, and only actually loads the data in small chunks when it is needed. Asynchronous opening uses a separate thread to open the file, allowing the main thread to carry on with other work while the file is loaded from disk in parallel.

Which technique is better depends on what you intend to do with the file and the characteristics of your computer, and it’s usually worth testing both approaches and seeing what works best for your particular task. In general, memory mapping gives better performance when dealing with a single file, particularly if the file is very large. If you need to process several files, asynchronous opening can be faster because you can work on one file while loading the next one.

# Memory-mapped files
With very large files, it might be helpful to use the mrcfile.mmap() function to open the file, which will open the data as a memory-mapped numpy array. The contents of the array are only read from disk as needed, so this allows large files to be opened very quickly. Parts of the data can then be read and written by slicing the array:
```
>>> # Open the file in memory-mapped mode
>>> mrc = mrcfile.mmap('tmp.mrc', mode='r+')
>>> # Now read part of the data by slicing
>>> mrc.data[1:3]
memmap([[ 4,  5,  6,  7],
        [ 8,  9, 10, 11]], dtype=int8)

>>> # Set some values by assigning to a slice
>>> mrc.data[1:3,1:3] = 0

>>> # Read the entire array - with large files this might take a while!
>>> mrc.data[:]
memmap([[ 0,  1,  2,  3],
        [ 4,  0,  0,  7],
        [ 8,  0,  0, 11]], dtype=int8)
>>> mrc.close()
```
To create new large, empty files quickly, use the mrcfile.new_mmap() function. This creates an empty file with a given shape and data mode. An optional fill value can be provided but filling a very large mmap array can take a long time, so it’s best to use this only when needed. If you plan to fill the array with other data anyway, it’s better to leave the fill value as None. A typical use case would be to create a new file and then fill it slice by slice:
```
>>> # Make a new, empty memory-mapped MRC file
>>> mrc = mrcfile.new_mmap('mmap.mrc', shape=(3, 3, 4), mrc_mode=0)
>>> # Fill each slice with a different value
>>> for val in range(len(mrc.data)):
...     mrc.data[val] = val
...
>>> mrc.data[:]
memmap([[[0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]],

        [[1, 1, 1, 1],
         [1, 1, 1, 1],
         [1, 1, 1, 1]],

        [[2, 2, 2, 2],
         [2, 2, 2, 2],
         [2, 2, 2, 2]]], dtype=int8)
```
Asynchronous opening
When processing several files in a row, asynchronous (background) opening can improve performance by allowing you to open multiple files in parallel. The mrcfile.open_async() function starts a background thread to open a file, and returns a FutureMrcFile object which you can call later to get the file after it’s been opened:
```
>>> # Open the first example file
>>> mrc1 = mrcfile.open('tmp.mrc')
>>> # Start opening the second example file before we process the first
>>> future_mrc2 = mrcfile.open_async('tmp.mrc.gz')
>>> # Now we'll do some calculations with the first file
>>> mrc1.data.sum()
36
>>> # Get the second file from its "Future" container ('result()' will wait
>>> # until the file is ready)
>>> mrc2 = future_mrc2.result()
>>> # Before we process the second file, we'll start the third one opening
>>> future_mrc3 = mrcfile.open_async('tmp.mrc.bz2')
>>> mrc2.data.max()
22
>>> # Finally, we'll get the third file and process it
>>> mrc3 = future_mrc3.result()
>>> mrc3.data
array([[ 0,  3,  6,  9],
       [12, 15, 18, 21],
       [24, 27, 30, 33]], dtype=int8)
```
As we saw in that example, calling result() will give us the MrcFile from the file opening operation. If the file hasn’t been fully opened yet, result() will simply wait until it’s ready. To avoid waiting, call done() to check if it’s finished.

File modes
MrcFile objects can be opened in three modes: r, r+ and w+. These correspond to the standard Python file modes, so r opens a file in read-only mode:
```
>>> # The default mode is 'r', for read-only access:
>>> mrc = mrcfile.open('tmp.mrc')
>>> mrc
MrcFile('tmp.mrc', mode='r')
>>> mrc.set_data(example_data)
Traceback (most recent call last):
  ...
ValueError: MRC object is read-only
>>> mrc.close()
r+ opens it for reading and writing:

>>> # Using mode 'r+' allows read and write access:
>>> mrc = mrcfile.open('tmp.mrc', mode='r+')
>>> mrc
MrcFile('tmp.mrc', mode='r+')
>>> mrc.set_data(example_data)
>>> mrc.data
array([[ 0,  1,  2,  3],
       [ 4,  5,  6,  7],
       [ 8,  9, 10, 11]], dtype=int8)
>>> mrc.close()
and w+ opens a new, empty file (also for both reading and writing):

>>> # Mode 'w+' creates a new empty file:
>>> mrc = mrcfile.open('empty.mrc', mode='w+')
>>> mrc
MrcFile('empty.mrc', mode='w+')
>>> mrc.data
array([], dtype=int8)
>>> mrc.close()
The new() function is effectively shorthand for open(name, mode='w+'):

>>> # Make a new file
>>> mrc = mrcfile.new('empty.mrc')
Traceback (most recent call last):
  ...
ValueError: File 'empty.mrc' already exists; set overwrite=True to overwrite it
>>> # Ooops, we've already got a file with that name!
>>> # If we're sure we want to overwrite it, we can try again:
>>> mrc = mrcfile.new('empty.mrc', overwrite=True)
>>> mrc
MrcFile('empty.mrc', mode='w+')
>>> mrc.close()
```
#Permissive read mode
Normally, if an MRC file is badly invalid, an exception is raised when the file is opened. This can be a problem if we want to, say, open a file and fix a header problem. To deal with this situation, open() and mmap() provide an optional permissive argument. If this is set to True, problems with the file will cause warnings to be issued (using Python’s warnings module) instead of raising exceptions, and the file will continue to be interpreted as far as possible.

Let’s see an example. First we’ll deliberately make an invalid file:
```
>>> # Make a new file and deliberately make a mistake in the header
>>> with mrcfile.new('invalid.mrc') as mrc:
...     mrc.header.map = b'map '  # standard requires b'MAP '
...
```
Now when we try to open the file, an exception is raised:
```
>>> # Opening an invalid file raises an exception:
>>> mrc = mrcfile.open('invalid.mrc')
Traceback (most recent call last):
  ...
ValueError: Map ID string not found - not an MRC file, or file is corrupt
```
If we use permissive mode, we can open the file, and we’ll see a warning about the problem (except that here, we have to catch the warning and print the message manually, because warnings don’t play nicely with doctests!):
```
>>> # Opening in permissive mode succeeds, with a warning:
>>> with warnings.catch_warnings(record=True) as w:
...     mrc = mrcfile.open('invalid.mrc', permissive=True)
...     print(w[0].message)
...
Map ID string not found - not an MRC file, or file is corrupt
```
Now let’s fix the file:
```
>>> # Fix the invalid file by correcting the header
>>> with mrcfile.open('invalid.mrc', mode='r+', permissive=True) as mrc:
...     mrc.header.map = mrcfile.constants.MAP_ID
...
```
And now we should be able to open the file again normally:
```
>>> # Now we don't need permissive mode to open the file any more:
>>> mrc = mrcfile.open('invalid.mrc')
>>> mrc.close()
```
The problems that can cause an exception when opening an MRC file are:

The header’s map field is not set correctly to confirm the file type. If the file is otherwise correct, permissive mode should be able to read the file normally.
The machine stamp is invalid and so the file’s byte order cannot be determined. In this case, permissive mode assumes that the byte order is little-endian and continues trying to read the file. If the file is actually big-endian, the mode and data size checks will also fail because these values depend on the endianness and will be nonsensical.
The mode number is not recognised. Currently accepted modes are 0, 1, 2, 4 and 6.
The data block is not large enough for the specified data type and dimensions.
In the last two cases, the data block will not be read and the data attribute will be set to None.

Fixing invalid files can be quite complicated! This usage guide might be expanded in future to explain how to analyse and fix problems, or the library itself might be improved to fix certain problems automatically. For now, if you have trouble with an invalid file, inspecting the code in this library might help you to work out how to approach the problem (start with MrcInterpreter._read_header()), or you could try asking on the CCP-EM mailing list for advice.

Using MrcFile objects
Accessing the header and data
The header and data arrays can be accessed using the header, extended_header and data attributes:
```
>>> mrc = mrcfile.open('tmp.mrc')
>>> mrc.header
rec.array((4, 3, 1, ...),
          dtype=[('nx', ...)])
>>> mrc.extended_header
array([],
      dtype='|V1')
>>> mrc.data
array([[ 0,  1,  2,  3],
       [ 4,  5,  6,  7],
       [ 8,  9, 10, 11]], dtype=int8)
>>> mrc.close()
```
These attributes are read-only and cannot be assigned to directly, but (unless the file mode is r) the arrays can be modified in-place:
```
>>> mrc = mrcfile.open('tmp.mrc', mode='r+')
>>> # A new data array cannot be assigned directly to the data attribute
>>> mrc.data = np.ones_like(example_data)
Traceback (most recent call last):
  ...
AttributeError: can't set attribute
>>> # But the data can be modified by assigning to a slice or index
>>> mrc.data[0, 0] = 10
>>> mrc.data
array([[10,  1,  2,  3],
       [ 4,  5,  6,  7],
       [ 8,  9, 10, 11]], dtype=int8)
>>> # All of the data values can be replaced this way, as long as the data
>>> # size, shape and type are not changed
>>> mrc.data[:] = np.ones_like(example_data)
>>> mrc.data
array([[1, 1, 1, 1],
       [1, 1, 1, 1],
       [1, 1, 1, 1]], dtype=int8)
>>> mrc.close()
```
To replace the data or extended header completely, call the set_data() and set_extended_header() methods:
```
>>> mrc = mrcfile.open('tmp.mrc', mode='r+')
>>> data_3d = np.linspace(-1000, 1000, 20, dtype=np.int16).reshape(2, 2, 5)
>>> mrc.set_data(data_3d)
>>> mrc.data
array([[[-1000,  -894,  -789,  -684,  -578],
        [ -473,  -368,  -263,  -157,   -52]],
       [[   52,   157,   263,   368,   473],
        [  578,   684,   789,   894,  1000]]], dtype=int16)
>>> # Setting a new data array updates the header dimensions to match
>>> mrc.header.nx
array(5, dtype=int32)
>>> mrc.header.ny
array(2, dtype=int32)
>>> mrc.header.nz
array(2, dtype=int32)
>>> # We can also set the extended header in the same way
>>> string_array = np.fromstring(b'The extended header can hold any kind of numpy array', dtype='S52')
>>> mrc.set_extended_header(string_array)
>>> mrc.extended_header
array([b'The extended header can hold any kind of numpy array'],
      dtype='|S52')
>>> # Setting the extended header updates the header's nsymbt field to match
>>> mrc.header.nsymbt
array(52, dtype=int32)
>>> mrc.close()
```
Note that setting an extended header does not automatically set or change the header’s exttyp field. You should set this yourself to identify the type of extended header you are using.

For a quick overview of the contents of a file’s header, call print_header():
```
>>> with mrcfile.open('tmp.mrc') as mrc:
...     mrc.print_header()
...
nx              : 5
ny              : 2
nz              : 2
mode            : 1
nxstart ...
Voxel size
The voxel (or pixel) size in the file can be accessed using the voxel_size attribute, which returns a numpy record array with three fields, x, y and z, for the voxel size in each dimension:

>>> with mrcfile.open('tmp.mrc') as mrc:
...     mrc.voxel_size
...
rec.array(( 0.,  0.,  0.),
          dtype=[('x', '<f4'), ('y', '<f4'), ('z', '<f4')])
```
In a new file, the voxel size is zero by default. To set the voxel size, you can assign to the voxel_size attribute, using a single number (for an isotropic voxel size), a 3-tuple or a single-item record array with x, y and z fields (which must be in that order):
```
>>> mrc = mrcfile.open('tmp.mrc', mode='r+')

>>> # Set a new isotropic voxel size:
>>> mrc.voxel_size = 1.0
>>> mrc.voxel_size
rec.array(( 1.,  1.,  1.),
          dtype=[('x', '<f4'), ('y', '<f4'), ('z', '<f4')])

>>> # Set an anisotropic voxel size using a tuple:
>>> mrc.voxel_size = (1.0, 2.0, 3.0)
>>> mrc.voxel_size
rec.array(( 1.,  2.,  3.),
          dtype=[('x', '<f4'), ('y', '<f4'), ('z', '<f4')])

>>> # And set a different anisotropic voxel size using a record array:
>>> mrc.voxel_size = np.rec.array(( 4.,  5.,  6.), dtype=[('x', '<f4'), ('y', '<f4'), ('z', '<f4')])
>>> mrc.voxel_size
rec.array(( 4.,  5.,  6.),
          dtype=[('x', '<f4'), ('y', '<f4'), ('z', '<f4')])
>>> mrc.close()
```
The sizes are not stored directly in the MRC header, but are calculated when required from the header’s cell and grid size fields. The voxel size can therefore be changed by altering the cell size:
```
>>> mrc = mrcfile.open('tmp.mrc', mode='r+')

>>> # Check the current voxel size in X:
>>> mrc.voxel_size.x
array(4.0, dtype=float32)

>>> # And check the current cell dimensions:
>>> mrc.header.cella
rec.array(( 20.,  10.,  6.),
          dtype=[('x', '<f4'), ('y', '<f4'), ('z', '<f4')])

>>> # Now change the cell's X length:
>>> mrc.header.cella.x = 10

>>> # And we see the voxel size has also changed:
>>> mrc.voxel_size.x
array(2.0, dtype=float32)

>>> mrc.close()
```
Equivalently, the cell size will be changed if a new voxel size is given:
```
>>> mrc = mrcfile.open('tmp.mrc', mode='r+')

>>> # Check the current cell dimensions:
>>> mrc.header.cella
rec.array(( 10.,  10.,  6.),
          dtype=[('x', '<f4'), ('y', '<f4'), ('z', '<f4')])

>>> # Set a new voxel size:
>>> mrc.voxel_size = 1.0

>>> # And our cell size has been updated:
>>> mrc.header.cella
rec.array(( 5.,  2.,  1.),
          dtype=[('x', '<f4'), ('y', '<f4'), ('z', '<f4')])

>>> mrc.close()
```
Because the voxel size array is calculated on demand, assigning back to it wouldn’t work so it’s flagged as read-only:
```
>>> mrc = mrcfile.open('tmp.mrc', mode='r+')

>>> # This doesn't work
>>> mrc.voxel_size.x = 2.0
Traceback (most recent call last):
  ...
ValueError: assignment destination is read-only

>>> # But you can do this
>>> vsize = mrc.voxel_size.copy()
>>> vsize.x = 2.0
>>> mrc.voxel_size = vsize
>>> mrc.voxel_size
rec.array(( 2.,  1.,  1.),
          dtype=[('x', '<f4'), ('y', '<f4'), ('z', '<f4')])
>>> mrc.close()
```
Note that the calculated voxel size will change if the grid size is changed by replacing the data array:
```
>>> mrc = mrcfile.open('tmp.mrc', mode='r+')

>>> # Check the current voxel size:
>>> mrc.voxel_size
rec.array(( 2.,  1.,  1.),
          dtype=[('x', '<f4'), ('y', '<f4'), ('z', '<f4')])
>>> # And the current data dimensions:
>>> mrc.data.shape
(2, 2, 5)

>>> # Replace the data with an array with a different shape:
>>> mrc.set_data(example_data)
>>> mrc.data.shape
(3, 4)

>>> # ...and the voxel size has changed:
>>> mrc.voxel_size
rec.array(( 2.5,  0.66666669,  1.),
          dtype=[('x', '<f4'), ('y', '<f4'), ('z', '<f4')])

>>> mrc.close()
```
#Keeping the header and data in sync
When a new data array is given (using set_data() or the data argument to mrcfile.new()), the header is automatically updated to ensure the file is is valid:
```
>>> mrc = mrcfile.open('tmp.mrc', mode='r+')

>>> # Check the current data shape and header dimensions match
>>> mrc.data.shape
(3, 4)
>>> mrc.header.nx
array(4, dtype=int32)
>>> mrc.header.nx == mrc.data.shape[-1]  # X axis is always the last in shape
True

>>> # Let's also check the maximum value recorded in the header
>>> mrc.header.dmax
array(11.0, dtype=float32)
>>> mrc.header.dmax == mrc.data.max()
True

>>> # Now set a data array with a different shape, and check the header again
>>> mrc.set_data(data_3d)
>>> mrc.data.shape
(2, 2, 5)
>>> mrc.header.nx
array(5, dtype=int32)
>>> mrc.header.nx == mrc.data.shape[-1]
True

>>> # The data statistics are updated as well
>>> mrc.header.dmax
array(1000.0, dtype=float32)
>>> mrc.header.dmax == mrc.data.max()
True
>>> mrc.close()
```
If the data array is modified in place, for example by editing values or changing the shape or dtype attributes, the header will no longer be correct:
```
>>> mrc = mrcfile.open('tmp.mrc', mode='r+')
>>> mrc.data.shape
(2, 2, 5)

>>> # Change the data shape in-place and check the header
>>> mrc.data.shape = (5, 4)
>>> mrc.header.nx == mrc.data.shape[-1]
False

>>> # We'll also change some values and check the data statistics
>>> mrc.data[2:] = 0
>>> mrc.data.max()
0
>>> mrc.header.dmax == mrc.data.max()
False
>>> mrc.close()
```
Note that the header is deliberately not updated automatically except when set_data() is called, so if you need to override any of the automatic header values you can do.

To keep the header in sync with the data, three methods can be used to update the header:

update_header_from_data(): This updates the header’s dimension fields, mode, space group and machine stamp to be consistent with the data array. Because it only inspects the data array’s attributes, this method is fast even for very large arrays.
update_header_stats(): This updates the data statistics fields in the header (dmin, dmax, dmean and rms). This method can be slow with large data arrays because it has to access the full contents of the array.
reset_header_stats(): If the data values have changed and the statistics fields are invalid, but the data array is very large and you do not want to wait for update_header_stats() to run, you can call this method to reset the header’s statistics fields to indicate that the values are undetermined.
The file we just saved had an invalid header, but of course, that’s what’s used by mrcfile to work out how to read the file from disk! When we open the file again, our change to the shape has disappeared:
```
>>> mrc = mrcfile.open('tmp.mrc', mode='r+')
>>> mrc.data.shape
(2, 2, 5)

>>> # Let's change the shape again, as we did before
>>> mrc.data.shape = (5, 4)
>>> mrc.header.nx == mrc.data.shape[-1]
False

>>> # Now let's update the dimensions:
>>> mrc.update_header_from_data()
>>> mrc.header.nx
array(4, dtype=int32)
>>> mrc.header.nx == mrc.data.shape[-1]
True

>>> # The data statistics are still incorrect:
>>> mrc.header.dmax
array(1000.0, dtype=float32)
>>> mrc.header.dmax == mrc.data.max()
False

>>> # So let's update those as well:
>>> mrc.update_header_stats()
>>> mrc.header.dmax
array(0.0, dtype=float32)
>>> mrc.header.dmax == mrc.data.max()
True
>>> mrc.close()
```
In general, if you’re changing the shape, type or endianness of the data, it’s easiest to use set_data() and the header will be kept up to date for you. If you start changing values in the data, remember that the statistics in the header will be out of date until you call update_header_stats() or reset_header_stats().

Data dimensionality
MRC files can be used to store several types of data: single images, image stacks, volumes and volume stacks. These are distinguished by the dimensionality of the data array and the space group number (the header’s ispg field):

Data type	Dimensions	Space group
Single image	2	0
Image stack	3	0
Volume	3	1–230 (1 for normal EM data)
Volume stack	4	401–630 (401 for normal EM data)
MrcFile objects have methods to allow easy identification of the data type: is_single_image(), is_image_stack(), is_volume() and is_volume_stack().
```
>>> mrc = mrcfile.open('tmp.mrc')

>>> # The file currently contains two-dimensional data
>>> mrc.data.shape
(5, 4)
>>> len(mrc.data.shape)
2

>>> # This is intepreted as a single image
>>> mrc.is_single_image()
True
>>> mrc.is_image_stack()
False
>>> mrc.is_volume()
False
>>> mrc.is_volume_stack()
False

>>> mrc.close()
```
If a file already contains image or image stack data, new three-dimensional data is treated as an image stack; otherwise, 3D data is treated as a volume by default:
```
>>> mrc = mrcfile.open('tmp.mrc', mode='r+')

>>> # New 3D data in an existing image file is treated as an image stack:
>>> mrc.set_data(data_3d)
>>> len(mrc.data.shape)
3
>>> mrc.is_volume()
False
>>> mrc.is_image_stack()
True
>>> int(mrc.header.ispg)
0
>>> mrc.close()

>>> # But normally, 3D data is treated as a volume:
>>> mrc = mrcfile.new('tmp.mrc', overwrite=True)
>>> mrc.set_data(data_3d)
>>> mrc.is_volume()
True
>>> mrc.is_image_stack()
False
>>> int(mrc.header.ispg)
1
>>> mrc.close()
```
Call set_image_stack() and set_volume() to change the interpretation of 3D data. (Note: as well as changing ispg, these methods also change mz to be 1 for image stacks and equal to nz for volumes.)
```
>>> mrc = mrcfile.open('tmp.mrc', mode='r+')

>>> # Change the file to represent an image stack:
>>> mrc.set_image_stack()
>>> mrc.is_volume()
False
>>> mrc.is_image_stack()
True
>>> int(mrc.header.ispg)
0

>>> # And now change it back to representing a volume:
>>> mrc.set_volume()
>>> mrc.is_volume()
True
>>> mrc.is_image_stack()
False
>>> int(mrc.header.ispg)
1

>>> mrc.close()
```
Note that the MRC format allows the data axes to be swapped using the header’s mapc, mapr and maps fields. This library does not attempt to swap the axes and simply assigns the columns to X, rows to Y and sections to Z. (The data array is indexed in C style, so data values can be accessed using mrc.data[z][y][x].) In general, EM data is written using the default axes, but crystallographic data files might use swapped axes in certain space groups – if this might matter to you, you should check the mapc, mapr and maps fields after opening the file and consider transposing the data array if necessary.

#Data types
Various numpy data types can be used for MRC data arrays. The conversions to MRC mode numbers are:

Data type	MRC mode
```
float16	2 (note that data will be widened to 32 bits in the file)
float32	2
int8	0
int16	1
uint8	6 (note that data will be widened to 16 bits in the file)
uint16	6
complex64	4
(Mode 3 is not supported since there is no corresponding numpy dtype.)
```
No other data types are accepted, including integer types of more than 16 bits, or float types of more than 32 bits. Many numpy array creation routines use int64 or float64 dtypes by default, which means you will need to give a dtype argument to ensure the array can be used in an MRC file:
```
>>> mrc = mrcfile.open('tmp.mrc', mode='r+')

>>> # This does not work
>>> mrc.set_data(np.zeros((4, 5)))
Traceback (most recent call last):
  ...
ValueError: dtype 'float64' cannot be converted to an MRC file mode
>>> # But this does
>>> mrc.set_data(np.zeros((4, 5), dtype=np.int16))
>>> mrc.data
array([[0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0]], dtype=int16)

>>> mrc.close()
```
#Validating MRC files
MRC files can be validated with mrcfile.validate():
```
>>> mrcfile.validate('tmp.mrc')
True
This works equally well for gzip- or bzip2-compressed files:

>>> mrcfile.validate('tmp.mrc.gz')
True

>>> mrcfile.validate('tmp.mrc.bz2')
True
Errors will cause messages to be printed to the console, and validate() will return False:

>>> # Let's make a file which is valid except for the header's mz value
>>> with mrcfile.new('tmp.mrc', overwrite=True) as mrc:
...     mrc.set_data(example_data)
...     mrc.header.mz = -1
...

>>> # Now it should fail validation and print a helpful message
>>> mrcfile.validate('tmp.mrc')
Header field 'mz' is negative
False
(More serious errors might also cause warnings to be printed to sys.stderr.)
```
Normally, messages are printed to sys.stdout (as normal for Python print() calls). validate() has an optional print_file argument which allows any text stream to be used for the output instead:
```
>>> # Create a text stream to capture the output
>>> import io
>>> output = io.StringIO()

>>> # Now validate the file...
>>> mrcfile.validate('tmp.mrc', print_file=output)
False

>>> # ...and check the output separately
>>> print(output.getvalue().strip())
```
Header field 'mz' is negative
Behind the scenes, mrcfile.validate() opens the file in permissive mode using mrcfile.open() and then calls MrcFile.validate(). If you already have an MrcFile open, you can call its validate() method directly to check the file – but note that the file size test might be inaccurate unless you call flush() first. To ensure the file is completely valid, it’s best to flush or close the file and then validate it from scratch using mrcfile.validate().

If you find that a file created with this library is invalid, and you haven’t altered anything in the header in a way that might cause problems, please file a bug report on the issue tracker!

Command line usage
Some mrcfile functionality is available directly from the command line, via scripts that are installed along with the package, or in some cases by running modules with python -m.

(If you’ve downloaded the source code instead of installing via pip, run pip install <path-to-mrcfile> or python setup.py install to make the command line scripts available.)

#Validation
MRC files can be validated with the mrcfile-validate script:
```
$ mrcfile-validate tests/test_data/EMD-3197.map
File does not declare MRC format version 20140: nversion = 0

$ # Exit status is 1 if file is invalid
$ echo $?
1
```
This script wraps the mrcfile.validator module, which can also be called directly:
```
$ python -m mrcfile.validator valid_file.mrc
$ echo $?
0
```
Multiple file names can be passed to either form of the command, and because these commands call mrcfile.validate() behind the scenes, gzip- and bzip2-compressed files can be validated as well:
```
$ mrcfile-validate valid_file_1.mrc valid_file_2.mrc.gz valid_file_3.mrc.bz2
Examining MRC headers
MRC file headers can be printed to the console with the mrcfile-header script:

$ mrcfile-header tests/test_data/EMD-3197.map
nx              : 20
ny              : 20
nz              : 20
mode            : 2
nxstart         : -2
nystart         : 0
nzstart         : 0
mx              : 20
my              : 20
mz              : 20
cella           : (228.0, 228.0, 228.0)
cellb           : (90.0, 90.0, 90.0)
...
...
```
Like mrcfile-validate, this also works for multiple files. If you want to access the same functionality from within Python, call print_header() on an open MrcFile object, or mrcfile.command_line.print_headers() with a list of file names.

#API overview
Class hierarchy
The following classes are provided by the mrcfile.py library:

MrcObject: Represents a generic MRC-like data object in memory, and provides header, extended header and data arrays and methods for operating on them.
MrcInterpreter: Subclass of MrcObject that can read and/or write its MRC data from arbitrary byte I/O streams (including Python file objects).
MrcFile: Subclass of MrcInterpreter that opens a file from disk to use as its I/O stream. This is the normal class used for most interactions with MRC files.
GzipMrcFile: Reads and writes MRC data using compressed gzip files.
Bzip2MrcFile: Reads and writes MRC data using compressed bzip2 files.
MrcMemmap: Uses a memory-mapped data array, for fast random access to very large data files. MrcMemmap overrides various parts of the MrcFile implementation to ensure that the memory-mapped data array is opened, closed and moved correctly when the data or extended header array sizes are changed.
MrcFile attributes and methods
Attributes:
```
header
extended_header
data
voxel_size
Methods:

set_extended_header()
set_data()
is_single_image()
is_image_stack()
is_volume()
is_volume_stack()
set_image_stack()
set_volume()
update_header_from_data()
update_header_stats()
reset_header_stats()
print_header()
validate()
flush()
close()
```
