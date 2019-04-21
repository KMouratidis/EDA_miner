
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
