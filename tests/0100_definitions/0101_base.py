import json

from django_editors.definitions import RichEditorDefinition
from django_editors.formfields import DjangoBaseEditorField
from django_editors.widgets import DjangoBaseEditorWidget


def test_basic(settings):
    """
    Definition only with required parameters should have the right default parameters.
    """
    foobar = RichEditorDefinition(name="foobar")

    assert foobar.label == "foobar"
    assert foobar.component_name == "Djangofoobar"
    assert json.loads(foobar.as_json()) == {
        "name": "foobar",
        "label": "foobar",
        "widget": "django_editors.widgets.DjangoBaseEditorWidget",
        "formfield": "django_editors.formfields.DjangoBaseEditorField",
        "component_name": "Djangofoobar",
        "js": [],
        "css": [],
        "editor_options": {},
        "widget_options": {},
        "wrapper_options": {},
    }

    assert foobar.widget_configuration() == {
        "editor_options": {},
        "widget_options": {},
        "wrapper_options": {},
    }

    assert foobar.get_widget_class() == DjangoBaseEditorWidget
    assert foobar.get_field_class() == DjangoBaseEditorField


def test_with_assets(settings):
    """
    Definition with some assets.
    """
    foobar = RichEditorDefinition(
        name="Foobar",
        css=["css/bundle-foo.css"],
        js=["js/bundle-bar.js"],
    )
    assert foobar.label == "Foobar"
    assert foobar.component_name == "DjangoFoobar"
    assert json.loads(foobar.as_json()) == {
        "name": "Foobar",
        "label": "Foobar",
        "widget": "django_editors.widgets.DjangoBaseEditorWidget",
        "formfield": "django_editors.formfields.DjangoBaseEditorField",
        "component_name": "DjangoFoobar",
        "js": [
            "js/bundle-bar.js"
        ],
        "css": [
            "css/bundle-foo.css"
        ],
        "editor_options": {},
        "widget_options": {},
        "wrapper_options": {},
    }

    assert foobar.get_assets() == {
        "css": {"all": ["css/bundle-foo.css"]},
        "js": ["js/bundle-bar.js"]
    }


def test_options(settings):
    """
    Defined options are correctly stored and can be overrided from
    'widget_configuration()' method.
    """
    foobar = RichEditorDefinition(
        name="Foobar",
        editor_options={"foo": "bar"},
        widget_options={"required": ""},
        wrapper_options={"ping": "pong"},
    )

    assert json.loads(foobar.as_json()) == {
        "name": "Foobar",
        "label": "Foobar",
        "widget": "django_editors.widgets.DjangoBaseEditorWidget",
        "formfield": "django_editors.formfields.DjangoBaseEditorField",
        "component_name": "DjangoFoobar",
        "js": [],
        "css": [],
        "editor_options": {"foo": "bar"},
        "widget_options": {"required": ""},
        "wrapper_options": {"ping": "pong"},
    }

    # Without method kwargs
    assert foobar.widget_configuration() == {
        "editor_options": {"foo": "bar"},
        "widget_options": {"required": ""},
        "wrapper_options": {"ping": "pong"},
    }

    # With method kwargs
    kwargs = {
        "editor_options": {"clark": "kent"},
        "widget_options": {"lois": "lane"},
        "wrapper_options": {"ping": "pang"},
    }
    assert foobar.widget_configuration(**kwargs) == {
        "editor_options": {"clark": "kent", "foo": "bar"},
        "widget_options": {"lois": "lane", "required": ""},
        "wrapper_options": {"ping": "pang"},
    }
