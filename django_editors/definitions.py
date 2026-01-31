import json
from copy import deepcopy
from dataclasses import (
    dataclass,
    field as dataclasses_field,
    fields as dataclasses_fields
)
from typing import Any

from django.utils.module_loading import import_string
from django_editors.utils.jsons import ExtendedJsonEncoder


@dataclass
class RichEditorDefinition:
    """
    Carry everything to build form widget and manage submitted content.

    .. Todo::
        ``name`` value must be a valid Python identifier because it can be used
        to compute object names. So we need to validate this value.

    Arguments:
        name (string): Key name used in registry and internals.

    Keyword Arguments:
        label (string): Label name to display (rarely for final user). Will be set
            with ``name`` value if not given.
        widget (class or string): Either a Python path to import for a custom form
            widget class to use or directly the widget class object.
        formfield (class or string): Either a Python path to import for a custom form
            field class to use or directly the form field class object.
        component_name (string): JavaScript class name to use to call editor. If not
            given the name is automatically composed of "Django" + ``name``.
        js (list): List of JavaScript file paths relative to static directory to load
            in document to provide editor.
        css (list): List of CSS file paths relative to static directory to implement
            editor layout.
        options (dict): Base widget options. These options can be overwritten from
            the keyword arguments passed to method ``widget_configuration()``.
    """
    name: str
    label: str = ""
    widget: Any = None
    formfield: Any = None
    component_name: str = None
    js: list[str] = dataclasses_field(default_factory=list)
    css: list[str] = dataclasses_field(default_factory=list)
    options: dict = dataclasses_field(default_factory=dict)

    def __post_init__(self):
        """
        Initialize empty positionnal argument values.
        """
        if not self.label:
            self.label = self.name

        if not self.widget:
            self.widget = "django_editors.widgets.DjangoBaseEditorWidget"

        if not self.formfield:
            self.formfield = "django_editors.formfields.DjangoBaseEditorField"

        if not self.component_name:
            self.component_name = "Django{name}".format(name=self.name)

    def get_assets(self):
        """
        This should provide all editor assets path to include in document to initialize
        an editor component.

        Returns:
            dict:
        """
        return {
            "css": {"all": self.css},
            "js": self.js,
        }

    def widget_configuration(self, **kwargs):
        """
        Returns default widget options merged with possible given custom options.

        Returns:
            dict:
        """
        options = deepcopy(self.options)

        if kwargs.get("editor_init") is True or kwargs.get("editor_init") is False:
            options["editor_init"] = kwargs.get("editor_init")

        if kwargs.get("editor_options"):
            options["editor_options"] = kwargs.get("editor_options")

        if kwargs.get("wrapper_options"):
            options["wrapper_options"] = kwargs.get("wrapper_options")

        return options

    def get_widget_class(self):
        """
        Returns the editor widget class.

        Returns:
            class: The editor class object.
        """
        # Load widget class from path if it is a string else assume it is a class
        return (
            import_string(self.widget)
            if isinstance(self.widget, str)
            else self.widget
        )

    def get_widget_object(self, **kwargs):
        """
        Returns the editor widget object with possible options.

        Arguments:
            **kwargs: Options to pass to Widget class, this may overwrite possible
                default widget options from the editor definition.

        Returns:
            django.forms.widgets.Widget: Instance of the editor widget class.
        """
        config = self.widget_configuration(**kwargs)

        if config:
            return self.get_widget_class()(**config)

        return self.get_widget_class()()

    def get_field_class(self):
        """
        Returns the editor form field class.

        .. Note::
            Opposed to widget, there is no method to get the form field instance.

        Returns:
            class:
        """
        # Load field class from path if it is a string else assume it is a class
        return (
            import_string(self.formfield)
            if isinstance(self.formfield, str)
            else self.formfield
        )

    def as_dict(self):
        """
        Convert dataclass attribute values to a dict.

        Returns:
            dict: A dict containing all the dataclass attributes.
        """
        return {
            f.name: getattr(self, f.name)
            for f in dataclasses_fields(self)
        }

    def as_json(self, indent=4):
        """
        Convert dataclass attribute values to a dict.

        Returns:
            string: A JSON containing all the dataclass attributes.
        """
        return json.dumps(self.as_dict(), indent=indent, cls=ExtendedJsonEncoder)

    def renderer(self, value):
        """
        Would render content saved from editor

        NOTE: RichEditorDefinition is not intended to be an instance of a widget but
        rather a widget factory, so this would only work with 'content' given as
        argument of this method or maybe move this into editor fields.

        .. Note::
            Commonly content is stored in HTML, but some editor may store them in
            something else that may need to be rendered. In some specific case it could
            be used also to patch HTML content.

            This will be used from a templatetags to use on content attribute from
            object.
        """
        return value

    def sanitizer(self, value):
        """
        Would sanitize content when saved.

        NOTE: Same concerns than 'renderer()'

        .. Note::
            It probably should allows for variable arguments to be passed like the
            object in case of very specific context sanitize (like where some content
            depend on other object attribute values).

            Many editor does not fully sanitize content which is considered as a
            security concern. Commonly we used Bleach to do this but it seems to be
            deprecated, let's take a see in JustHTML package.

        """
        return value
