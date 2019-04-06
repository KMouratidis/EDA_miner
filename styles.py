
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
