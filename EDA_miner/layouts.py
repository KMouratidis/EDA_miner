"""
Similar to `styles.py`, this module is mean as a collection of layouts \
to be used across the dash app. A layout is about what components exist \
in any view (e.g. html elements) whereas a style is about... styling! \
Styles are implemented as functions to allow use with different parameters.

Functions:
    - default_2d: Layout for most plotly graphs.
    - default_3d: Layout for 3D graphs, not implemented.
    - default_kpi: Layout for KPI graphs, not implemented.

Classes:
    - PDF_Layout1: A sample PDF layout, more to be added. Implemented \
                   as a class out of convenience, may be changed later. \
                   Usage: `PDF_Layout1.render(x_axis, y_axis)`.

Notes to others:
    Feel free to tamper with all of the functions and classes below \
    and/or add your own. Beware that in some cases (e.g. defining a \
    new PDF layout) you might need to make changes in other files, \
    or at least wait till needed functionality is added.
"""

import plotly.graph_objs as go


def default_2d(xvars, yvars):
    """
    Default `go.Layout` for 2D graphs.

    Args:
        xvars: str, title of the x-axis.
        yvars: str, title of the y-axis.

    Returns:
        A `go.Layout` instance.
    """

    if isinstance(yvars, list):
        yvars = yvars[0]

    return go.Layout(
        xaxis={'title': xvars},
        yaxis={'title': yvars},
        margin={'l': 60, 'b': 40, 't': 10, 'r': 20},
        legend={'x': 0, 'y': 1},
        hovermode='closest'
    )


def default_3d(xvars, yvars, zvars):
    """
    Default `go.Layout` for 3D graphs. Currently same as default_2d.

    Args:
        xvars: str, title of the x-axis.
        yvars: str, title of the y-axis.
        zvars: str, currently not used.

    Returns:
        A `go.Layout` instance.

    Todo:
        This needs a better implementation
    """

    return default_2d(xvars, yvars)


def default_kpi(xvars, yvars):
    """
    Default `go.Layout` for KPI graphs. Currently same as default_2d.

    Args:
        xvars: str, title of the x-axis.
        yvars: str, title of the y-axis.

    Returns:
        A `go.Layout` instance.

    Todo:
        This might need a better implementation
    """

    return default_2d(xvars, yvars)
