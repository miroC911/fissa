'''
Various functions to read and extract from Tiff stacks using the pillow library

Author: swk, swkeemink@scimail.eu
Initial date: 2015-05-29
Updated:      2015-10-18
'''

from __future__ import division

import numpy as np
from PIL import Image, ImageSequence


def image2array(img, dtype=np.uint8, band=0):
    '''
    Convert a single PIL/Pillow image into a numpy array.

    Parameters
    ----------
    img : PIL.Image
        Source image, loaded with PIL or Pillow.
    dtype : data-type, optional
        The data type which corresponds to the encoding of each channel
        in the source image. Default is `numpy.uint8`, which
        corresponds to 8 unsigned bits per channel and is hence encoded
        with integers in the range 0-255.
    band : int, optional
        Which band (color channel) to get extract data from. If `img`
        is greyscale, this must be 0. If `img` is in RGB, BGR or CMYK,
        format, the data will be taken from band number `band`. Default
        is 0.

    Returns
    -------
    numpy.ndarray
        2D output array, sized `(height, width)`, with data type
        `dtype`.

    Raises
    ------
    ValueError
        Requested `band` is larger than the number of available channels
    '''
    # Get the height and width from the size of the image. Note that
    # width is the first and height is the second dimension here.
    (width, height) = img.size
    # Check how many channels the image has, and that we don't try to
    # get data from a channel which doesn't exist.
    num_bands = len(img.getbands())
    if band >= num_bands:
        raise ValueError((
            'Requested band number {} exceeds the number of bands available '
            'in the image, which is {}.'
            ).format(band, num_bands))
    # If there is only one band, we need to request None instead of 0.
    if num_bands == 1:
        band = None
    # And if there isn't, make sure we aren't trying to load the data
    # from multiple channels.
    elif band is None:
        raise ValueError(
            'This function can not load the entire contents of a multi-'
            'channel (i.e. color) image.')
    # Use the `getdata` method to get an iterable sequence which runs
    # through every pixel in the image. Since this is flat, we need
    # to reshape the result. Note here that the width is the second
    # and height is the first dimension in the converted numpy array.
    return np.asarray(img.getdata(band), dtype).reshape((height, width))


def get_frame_number(img):
    '''
    Get the number of frames for pillow Image img

    Parameters
    ----------
    img : PIL.Image
        An image loaded using Pillow Image.

    Returns
    -------
    int
        Number of frames in img
    '''
    if hasattr(img, 'n_frames'):
        # Introduced in Pillow 2.9.0
        return img.n_frames
    # Keep going up one frame, until no such frame exists (resulting in
    # EOFEerror)
    while True:
        try:
            img.seek(img.tell() + 1)
        except EOFError:
            break  # end of sequence
    return img.tell() + 1


def imgstack2array(img, dtype=np.uint8, band=0):
    '''
    Loads an entire greyscale tiff stack as a single numpy array.

    Parameters
    ----------
    img : PIL.Image
        An image loaded using Pillow Image.
    dtype : data-type, optional
        The data type which corresponds to the encoding of each channel
        in the source image. Default is `numpy.uint8`, which
        corresponds to 8 unsigned bits per channel.
    band : int, optional
        Which band (color channel) to get extract data from. If `img`
        is greyscale, this must be 0. If `img` is in RGB, BGR or CMYK,
        format, the data will be taken from band number `band`. Default
        is 0.

    Returns
    -------
    numpy.ndarray
        The contents of the TIFF file, parsed into a 3-dimensional
        array, depending on whether the image is
        greyscale or has multiple color channels (a.k.a. bands).
        The output shape is either `(height, width, num_frames)` or
        `(height, width, num_channel, num_frames)` correspondingly.

    See also
    --------
    tiff2array
    '''
    # Get the first frame
    array0 = image2array(img, dtype=dtype, band=band)
    # From the first frame, we can tell the dtype we need to
    # initialize with, as well as the shape of each frame in the image
    shape = list(array0.shape)
    # We need to add an extra dimension to contain the time series
    shape.append(img.n_frames)
    # Initialise output array
    contents = np.zeros(shape, dtype=array0.dtype)

    # Loop over all frames
    for index, frame in enumerate(ImageSequence.Iterator(img)):
        contents[..., index] = image2array(frame, dtype=dtype, band=band)

    return contents


def tiff2array(filename, dtype=np.uint8, band=0):
    '''
    Loads an entire greyscale tiff stack as a single numpy array.

    Parameters
    ----------
    filename : string
        Path to greyscale TIFF file.
    dtype : data-type, optional
        The data type which corresponds to the encoding of each channel
        in the source image. Default is `numpy.uint8`, which
        corresponds to 8 unsigned bits per channel.
    band : int, optional
        Which band (color channel) to get extract data from. If `img`
        is greyscale, this must be 0. If `img` is in RGB, BGR or CMYK,
        format, the data will be taken from band number `band`. Default
        is 0.

    Returns
    -------
    numpy.ndarray
        The contents of the TIFF file, parsed into a three-dimensional
        array of [] shape(tiff), with all frames

    See also
    --------
    imgstack2array
    '''
    return imgstack2array(Image.open(filename), dtype=dtype, band=band)


def get_imgstack_mean(img, source_dtype=np.uint8, band=0):
    '''
    Get the mean data for an Pillow image stack or animation.

    Parameters
    ----------
    img : PIL.Image
        An animated image loaded using Pillow Image.
    source_dtype : data-type, optional
        The data type which corresponds to the encoding of each channel
        in the source image. Default is `numpy.uint8`, which
        corresponds to 8 unsigned bits per channel.
    band : int, optional
        Which band (color channel) to get extract data from. If `img`
        is greyscale, this must be 0. If `img` is in RGB, BGR or CMYK,
        format, the data will be taken from band number `band`. Default
        is 0.

    Returns
    -------
    numpy.ndarray
        Average pixel values across all frames in the animation or
        image stack, within the channel numbered `band`.

    See also
    --------
    get_mean_tiff
    '''
    # We don't load the entire image into memory at once, because
    # it is likely to be rather large.
    # Initialise holding array with zeros
    avg = np.zeros(img.size[::-1], dtype=np.float64)

    # Loop over all frames and sum the pixel intensities together
    for frame in ImageSequence.Iterator(img):
        avg += image2array(frame, dtype=source_dtype, band=band)

    # Divide by number of frames to find the average
    avg /= img.n_frames
    return avg


def get_mean_tiff(filename, source_dtype=np.uint8, band=0):
    '''
    Get the mean frame for a tiff stack.

    Parameters
    ----------
    filename : string
        Path to TIFF file.
    source_dtype : data-type, optional
        The data type which corresponds to the encoding of each channel
        in the source image. Default is `numpy.uint8`, which
        corresponds to 8 unsigned bits per channel.
    band : int, optional
        Which band (color channel) to get extract data from. If `img`
        is greyscale, this must be 0. If `img` is in RGB, BGR or CMYK,
        format, the data will be taken from band number `band`. Default
        is 0.

    Returns
    -------
    numpy.ndarray
        Average pixel values across all frames in the animation or
        image stack.

    See also
    --------
    get_imgstack_mean
    '''
    return get_imgstack_mean(Image.open(filename), source_dtype=source_dtype,
                             band=band)


def getbox(center, half_length):
    '''
    Find the edge co-ordinates of a square box with given center and
    length.

    Parameters
    ----------
    center : tuple or list
        The center of the box. Should be a two-dimensional tuple with
        each entry corresponding to the location of the center in that
        dimension, `(y, x)`.
    half_length : scalar
        Half the length of the required output box.

    Returns
    -------
    tuple
        Pixel co-ordinates to use when cutting an image down to a
        square of length `2 * half_length`. This output is appropriate
        for using with `PIL.Image.crop` to get the desired output shape.
        Output has elements `(x_0, y_0, x_1, y_1)`, which is
        `(left border, upper border, right border, lower border)`.

    Example
    -------
    >>> img = Image.load(filename)
    >>> box = getbox(center, half_length)
    >>> cropped_img = img.crop(box)
    '''
    half_length = np.rint(2 * half_length) / 2
    x0 = np.ceil(center[1]-half_length)
    y0 = np.ceil(center[0]-half_length)
    x1 = np.rint(x0 + 2*half_length)
    y1 = np.rint(y0 + 2*half_length)
    return (x0, y0, x1, y1)


def getavg(img, box, frame_indices=None, source_dtype=np.uint8, band=0):
    '''
    Get the average for the box in pillow Image img, for the specified frames

    Parameters
    ----------
    img : PIL.Image
        Loaded from a tiff stack
    box : tuple
        Box defining which co-ordinates to extract from the image,
        `(left, top, right, bottom)`.
    frame_indices : list or None, optional
        which frames to get. If None, all frames are used
    source_dtype : data-type, optional
        The data type which corresponds to the encoding of each channel
        in the source image. Default is `numpy.uint8`, which
        corresponds to 8 unsigned bits per channel and is hence encoded
        with integers in the range 0-255.
    band : int, optional
        Which band (color channel) to get extract data from. If `img`
        is greyscale, this must be 0. If `img` is in RGB, BGR or CMYK,
        format, the data will be taken from band number `band`. Default
        is 0.

    Returns
    -------
    numpy.ndarray
        Array of shape of img, which is the averaged image
    '''
    if frame_indices is None:
        frame_indices = range(img.n_frames)

    width = box[2] - box[0]
    height = box[3] - box[1]

    # Initialise floating point array to hold running total
    avg = np.zeros((height, width), dtype=np.float64)

    for frame_index in frame_indices:
        # get frame (note: best to now get all relevant data from this frame,
        # so don't have to seek again (although takes neglible time)
        img.seek(frame_index)
        avg[:] += image2array(img.crop(box), dtype=source_dtype, band=band)
    avg = avg / len(frame_indices)

    return avg


def extract_from_single_tiff(filename, masksets, source_dtype=np.uint8,
                             band=0):
    '''
    Extract the traces from the tiff stack at filename for given rois and
    trials, using Pillow.

    Parameters
    ----------
    filename : string
        Path to source TIFF file.
    masksets : dict of lists of boolean arrays
        A dictionary of masks, where each key maps to a maskset. A
        maskset is a list of boolean arrays masks, with each array
        indicating the spatial extent of a region of interest (ROI)
        within the image - `True` inside the ROI and `False` outside.
    source_dtype : data-type, optional
        The data type which corresponds to the encoding of each channel
        in the source image. Default is `numpy.uint8`, which
        corresponds to 8 unsigned bits per channel and is hence encoded
        with integers in the range 0-255.
    band : int, optional
        Which band (color channel) to get extract data from. If `img`
        is greyscale, this must be 0. If `img` is in RGB, BGR or CMYK,
        format, the data will be taken from band number `band`. Default
        is 0.

    Returns
    -------
    traces : dict of numpy.ndarray
        A dictionary with keys the same as that of `masksets`, each
        mapping to a two-dimensional `numpy.ndarray`, sized
        `(num_masks, num_frames)`, of traces extracted from the pixels
        constituting each mask.
    '''
    img = Image.open(filename)
    # Initiaise an empty dictionary for containing the output
    traces = {}
    # Extract the data and put in output dictionary
    for label, maskset in masksets.items():
        # Extract traces for this maskset
        traces[label] = extract_traces(img, maskset, source_dtype=source_dtype,
                                       band=band)
    return traces


def extract_traces(img, masks, source_dtype=np.uint8, band=0):
    '''
    Get the traces for each mask in masks from the pillow object img for
    nframes.

    Parameters
    ----------
    img : PIL.Image
        Pillow loaded tiff stack
    masks : list of boolean arrays
        list of masks (boolean arrays)
    source_dtype : data-type, optional
        The data type which corresponds to the encoding of each channel
        in the source image. Default is `numpy.uint8`, which
        corresponds to 8 unsigned bits per channel and is hence encoded
        with integers in the range 0-255.
    band : int, optional
        Which band (color channel) to get extract data from. If `img`
        is greyscale, this must be 0. If `img` is in RGB, BGR or CMYK,
        format, the data will be taken from band number `band`. Default
        is 0.

    Returns
    -------
    numpy.ndarray
        Traces across frames in image stack `img` for each mask, sized
        `(num_masks, num_frames)`.
    '''
    # TODO: Try loading in entire image into memory (as a memory intensive
    #       alternative) to see if that speeds up the algorithm much.
    #       Would increase memory needs, but could be worth it.

    # Initialise an array predfine list with the data
    traces = np.zeros((len(masks), img.n_frames), dtype=np.float64)

    # For each frame, get the data
    for frame_index, frame in enumerate(ImageSequence.Iterator(img)):
        # Get the pixel values for this frame
        frame_array = image2array(frame, dtype=source_dtype, band=band)
        # For each mask, extract the contents for this frame
        for mask_index, mask in enumerate(masks):
            traces[mask_index, frame_index] = np.mean(frame_array[mask])

    return traces
