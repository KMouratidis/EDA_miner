
def dropdown(display=True, horizontal=True):

    base = {
        'display': 'inline-block' if display else "none",
        'margin': "10px",
        'verticalAlign': "bottom",
    }

    if horizontal:
        base["width"] = "30%"
    else:
        base["display"] = "block"

    return base


cyto_stylesheet = [
    {
        'selector': 'node',
        'style': {
            'label': 'data(label)'
        }
    },
    {
        "selector": "edge",
        "style": {
            'curve-style': 'bezier',
            'target-arrow-color': 'black',
            'target-arrow-shape': 'triangle',
            'line-color': 'black'
        }
    },
    {
        "selector": ".parents",
        "style": {
            "shape": "rectangle"
        }
    },
    {
        'selector': '.withimage',
        'style': {
            'width': 50,
            'height': 50,
            'background-fit': 'cover',
            'background-image': 'data(url)'
        }
    },
]
