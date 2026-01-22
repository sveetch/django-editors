import json

from django_editors.editors import RichEditorDefinition
from django_editors.formfields import DjangoBaseEditorField
from django_editors.widgets import DjangoBaseEditorWidget


def test_base(settings):
    """
    Definition should correctly compute some attribute values and methods
    """
    bizu = RichEditorDefinition(
        name="bizou",
        label="Bizu",
        widget=DjangoBaseEditorWidget,
    )

    assert bizu.label == "Bizu"
    assert bizu.component_name == "Djangobizou"
    assert json.loads(bizu.as_json()) == {
        "name": "bizou",
        "label": "Bizu",
        "widget": "django_editors.widgets.DjangoBaseEditorWidget",
        "formfield": "django_editors.formfields.DjangoBaseEditorField",
        "component_name": "Djangobizou",
        "js": [],
        "css": [],
        "options": {}
    }

    foobar = RichEditorDefinition(
        name="Foobar",
        css=["css/bundle-foo.css"],
        js=["js/bundle-bar.js"],
    )

    assert foobar.label == "Foobar"
    assert foobar.component_name == "DjangoFoobar"
    assert foobar.widget_configuration() == {}
    assert foobar.get_assets() == {
        "css": {"all": ["css/bundle-foo.css"]},
        "js": ["js/bundle-bar.js"]
    }
    assert foobar.get_widget_class() == DjangoBaseEditorWidget
    assert foobar.get_field_class() == DjangoBaseEditorField
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
        "options": {}
    }
