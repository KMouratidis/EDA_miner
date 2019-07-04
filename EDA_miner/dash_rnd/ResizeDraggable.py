# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class ResizeDraggable(Component):
    """A ResizeDraggable component.
ExampleComponent is an example component.
It takes a property, `label`, and
displays it.
It renders an input with the property `value`
which is editable by the user.

Keyword arguments:
- children (dash component; optional)
- id (string; optional): The ID used to identify this component in Dash callbacks
- label (string; required): A label that will be printed when this component is rendered.
- value (string; optional): The value displayed in the input
- minWidth (number; optional)
- minHeight (number; optional)
- x (number; optional)
- y (number; optional)
- style (dict; optional)"""
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, label=Component.REQUIRED, value=Component.UNDEFINED, minWidth=Component.UNDEFINED, minHeight=Component.UNDEFINED, x=Component.UNDEFINED, y=Component.UNDEFINED, style=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'label', 'value', 'minWidth', 'minHeight', 'x', 'y', 'style']
        self._type = 'ResizeDraggable'
        self._namespace = 'dash_rnd'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'label', 'value', 'minWidth', 'minHeight', 'x', 'y', 'style']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in ['label']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(ResizeDraggable, self).__init__(children=children, **args)
