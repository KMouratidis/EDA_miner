"""
This module is meant as a collection of styles that cannot be defined
in the CSS (e.g. due to JS/Dash libraries' rendered elements not being
viewable in inspection, or some overriding).

Available styles:
    - cyto_stylesheet: The style used for the Model Builder, and will \
                       probably also be used for other cytoscape \
                       visualizations.
"""

cyto_stylesheet = [
    {
        'selector': 'node',
        'style': {
            'label': 'data(label)',
            'font-size': 18,
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
            'width': 80,
            'height': 80,
            'background-fit': 'cover',
            'background-image': 'data(url)'
        }
    },
]
