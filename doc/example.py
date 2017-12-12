# -*- coding: utf-8 -*-

# This guide follows mostly: 
# https://github.com/numpy/numpy/blob/master/doc/example.py
"""
Here comes the module description

Detailed introduction and tutorial of method goes here.

You can even link tutorials here, if appropiate. 

If you have references you can insert them here, otherwise in the corresponding
funtions, methods or classes.

For a working example see :py:mod:`unitary_event_analysis.py<elephant.unitary_event_analysis>`
"""

class MyClass(object):  # Classes use CamelCase notation
    """
    One line description of class.

    Long description of class, may span several lines. Possible sections:

    Parameters
    ----------
    List the arguments of the constructor (__init__) here!
    
    x : float
        The X coordinate
    y : float
        The Y coordinate
  
    Raises
    ------
    ...

    See Also
    --------
    ...

    Notes
    -----
    ...

    References
    ----------
    ...

    Examples
    --------
    ...

    Methods
    -------
    Only list methods if the class is very complex
    """

    def __init__(self, param):
        """
        Constructor
        (actual documentation is in class documentation, see above!)
        """
        self.param = param

    def function_a(self, param, spiketrains, is_true=True, c='C', var=None):
        """
        One-line short description of the function.

        Long description of the function. Details of what the function is doing
        and how it is doing it. Used to clarify functionality, not to discuss
        implementation detail or background theory, which should rather be
        explored in the notes section below. You may refer to the parameters
        and the function name, but parameter descriptions still belong in the
        parameters section.

        Variable, module, function, and class names should be written
        between single back-ticks (`numpy`), NOT *bold*.

        Parameters
        ----------
        param : int or float
            Description of parameter `param`. Enclose variables in single
            backticks. The colon must be preceded by a space, or omitted if the
            type is absent.
        spiketrains : list of neo.SpikeTrain objects
            A list to copy all strings in the world.
        is_true :
            True, if 1.
            False, if 0.
            Default is True.
        c : 'C', 'F', 'A'
            If only certain values are allowed. 
            Default is 'C'.
        var : int
            Some value. 
            Default is `None`

        Returns
        -------
        signal : int
            Description of return value.
        list : list of numpy.array
            Returns a list of numpy.arrays. 

        Raises
        ------
        ValueError :
            Condition when a ValueError can occur.

        See Also
        --------
        average : Weighted average
            Used to refer to related code. Functions may be listed without 
            descriptions, and this is preferable if the functionality is 
            clear from the function name.
            scipy.random.norm : Random variates, PDFs, etc.

        Notes
        -----
        An optional section that provides additional information about the
        code, possibly including a discussion of the algorithm. This section
        may include mathematical equations, written in LaTeX format. Inline:
        :math: `x^2`. An equation:

        .. math::

        x(n) * y(n) \Leftrightarrow X(e^{j\omega } )Y(e^{j\omega } )\\
        another equation here

        Images are allowed, but should not be central to the explanation; users
        viewing the docstring as text must be able to comprehend its meaning
        without resorting to an image viewer. These additional illustrations
        are included using:

        .. image:: filename

        References
        ----------
        .. [1] O. McNoleg, "The integration of GIS, remote sensing ... "

        Examples
        --------
        These are written in doctest format, and should illustrate how to
        use the function. This text may explain the example beforehand.

        >>> np.add(1, 2)
        3

        >>> import numpy as np
        >>> import numpy.random
        >>> np.random.rand(2)
        array([ 0.35773152,  0.38568979])  #random

        """

        # Variables use underscore notation
        dummy_variable = 1
        a = 56  # This mini comment uses two spaces after the code!

        # Textual strings use double quotes
        error = "An error occurred. Please fix it!"

        # Non-textual strings use single quotes
        default_character = 'a'

        # Normal comments are proceeded by a single space, and begin with a
        # capital letter
        dummy_variable += 1

        # Longer comments can have several sentences. These should end with a
        # period. Just as in this example.
        dummy_variable += 1

    # Class functions need only 1 blank line.
    # This function is deprecated. Add a warning!
    def function_b(self, **kwargs):
        """
        This is a function that does b.

        .. note:: Deprecated in elephant 0.4
          `function_b` will be removed in elephant 1.0, it is replaced by
          `function_c` because the latter works also with Numpy Ver. 1.6.

        Parameters
        ----------
        kwargs: {divide, over, under, invalid}
            From numpy.errstate.
            Keyword arguments. The valid keywords are the
            possible floating-point exceptions. Each keyword should have a
            string value that defines the treatment for the particular error.
            Possible values are {'ignore', 'warn', 'raise', 'call', 'print',
            'log'}.

        """
        pass


class MyOtherClass(object):
    """
    Class documentation
    """

    def __init__(self, params):
        """
        Constructor
        """

        pass


# Functions also need 2 blank lines between any structures.
def top_level_function(param):
    """
    The same docstring guidelines as in the class above.
    """
    pass


def another_top_level_function(param):
    """
    The same docstring guidelines as in the class above.
    """
    pass
