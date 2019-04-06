import plotly.graph_objs as go


def default_2d(xvars, yvars):
    return go.Layout(
        xaxis={'title': xvars},
        yaxis={'title': yvars},
        margin={'l': 80, 'b': 20, 't': 10, 'r': 20},
        legend={'x': 0, 'y': 1},
        hovermode='closest'
    )

def default_3d(xvars, yvars, zvars):
    # This needs a better implementation
    return default_2d(xvars, yvars)

def default_kpi(xvars, yvars):
    # This needs a better implementation
    return default_2d(xvars, yvars)
