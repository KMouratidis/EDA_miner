
def dropdown(display=True, horizontal=True):

    base = {
        'display': 'inline-block' if display else "none",
        'margin':"10px",
        'verticalAlign':"bottom",
    }

    if horizontal:
        base["width"] = "30%"
    else:
        base["display"] = "block"

    return base

def upload_button():
    return {
        'width': '30%',
        'height': '60px',
        'lineHeight': '60px',
        'borderWidth': '1px',
        'borderStyle': 'dashed',
        'borderRadius': '5px',
        'textAlign': 'center',
        'margin': '10px'
    }
