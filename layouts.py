import plotly.graph_objs as go


def default_2d(xvars, yvars):

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
    # TODO: This needs a better implementation
    return default_2d(xvars, yvars)


def default_kpi(xvars, yvars):
    # This needs a better implementation
    return default_2d(xvars, yvars)


class PDF_Layout1:
    first_figure = go.Layout(
        autosize=False,
        bargap=0.35,
        font={
          "family": "Raleway",
          "size": 10
        },
        height=300,
        hovermode="closest",
        legend={
          "x": -0.0228945952895,
          "y": -0.189563896463,
          "orientation": "h",
          "yanchor": "top"
        },
        margin={
          "r": 0,
          "t": 20,
          "b": 10,
          "l": 10
        },
        showlegend=True,
        title="",
        width=600,
        xaxis={
          "autorange": True,
          "range": [-0.5, 4.5],
          "showline": True,
          "title": "",
          "type": "category"
        },
        yaxis={
          "autorange": True,
          "range": [0, 22.9789473684],
          "showgrid": True,
          "showline": True,
          "title": "",
          "type": "linear",
          "zeroline": False
        }
    )

    second_figure = first_figure

    @staticmethod
    def render(x_axis, y_axis):
        return go.Layout(
            autosize=False,
            bargap=0.35,
            font={
              "family": "Raleway",
              "size": 10
            },
            height=300,
            hovermode="closest",
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            showlegend=True,
            title="",
            width=600,
            xaxis=x_axis,
            yaxis=y_axis
        )
