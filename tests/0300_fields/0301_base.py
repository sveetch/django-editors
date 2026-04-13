from django import forms

from django_editors.widgets import DjangoBaseEditorWidget
from django_editors.formfields import DjangoBaseEditorField
from django_editors.utils.tests import html_element
from django_editors.definitions import RichEditorDefinition


def test_abstract(settings):
    """
    Building a field using simple CharField and the abtract editor class should work
    as expected.
    """
    editor = RichEditorDefinition(
        name="Foobar",
        css=["css/bundle-foo.css"],
        js=["js/bundle-bar.js"],
    )

    class DummyForm(forms.Form):
        field = forms.CharField(
            label="Rich text",
            widget=DjangoBaseEditorWidget(
                editor=editor,
                init_editor=False,
            )
        )

    form = DummyForm()

    assert html_element(form.as_div()) == html_element(
        "<div>"
        "<label for=\"id_field\">Rich text:</label>"
        "<textarea name=\"field\" cols=\"40\" rows=\"10\" required id=\"id_field\">"
        "</textarea>"
        "</div>"
    )


def test_abstract_init(settings):
    """
    Building a field using simple CharField, the abtract editor class and 'init' option
    should work as expected.
    """
    editor = RichEditorDefinition(
        name="Foobar",
        css=["css/bundle-foo.css"],
        js=["js/bundle-bar.js"],
    )

    class DummyForm(forms.Form):
        field = forms.CharField(
            label="Rich text",
            widget=DjangoBaseEditorWidget(
                editor=editor,
                init_editor=True,
                editor_options={"dummy": ["pip", "pop"], "ping": None},
            )
        )

    form = DummyForm()

    assert html_element(form.as_div()) == html_element(
        "<div>"
        "<label for=\"id_field\">Rich text:</label>"
        "<textarea name=\"field\" cols=\"40\" rows=\"10\" required id=\"id_field\">"
        "</textarea>"
        "<script>"
        "let id_field = new DjangoFoobar({"
        " \"source\": document.querySelector(\"#id_field\"),"
        " \"editor_options\": {\"dummy\": [\"pip\", \"pop\"], \"ping\": null},"
        " \"classNames\": \"form-control\""
        " });"
        " id_field.provide();"
        " </script>"
        "</div>"
    )


def test_concrete(settings):
    """
    Building a field using simple CharField and concrete editor class should
    work as expected.
    """
    editor = RichEditorDefinition(
        name="Foobar",
        css=["css/bundle-foo.css"],
        js=["js/bundle-bar.js"],
    )

    class DummyForm(forms.Form):
        field = forms.CharField(
            label="Rich text",
            widget=editor.get_widget_object(editor=editor, init_editor=False)
        )

    form = DummyForm()

    assert html_element(form.as_div()) == html_element(
        "<div>"
        "<label for=\"id_field\">Rich text:</label>"
        "<textarea name=\"field\" cols=\"40\" rows=\"10\" required id=\"id_field\">"
        "</textarea>"
        "</div>"
    )

    assert html_element(str(form.media)) == html_element(
        "<link href=\"/static/css/bundle-foo.css\" media=\"all\" rel=\"stylesheet\">"
        "<script src=\"/static/js/bundle-bar.js\"></script>"
    )


def test_concrete_init(settings):
    """
    Building a field using simple CharField, concrete editor class and 'init' option
    should work as expected.
    """
    editor = RichEditorDefinition(
        name="Foobar",
        css=["css/bundle-foo.css"],
        js=["js/bundle-bar.js"],
    )

    # Again but set widget with editor initialization
    class DummyForm(forms.Form):
        field = forms.CharField(
            label="Rich text",
            widget=editor.get_widget_object(
                editor=editor,
                init_editor=True,
                editor_options={"dummy": ["pip", "pop"], "ping": None},
            )
        )

    form = DummyForm()

    assert html_element(form.as_div()) == html_element(
        "<div>"
        "<label for=\"id_field\">Rich text:</label>"
        "<textarea name=\"field\" cols=\"40\" rows=\"10\" required id=\"id_field\">"
        "</textarea>"
        "<script>"
        "let id_field = new DjangoFoobar({"
        " \"source\": document.querySelector(\"#id_field\"),"
        " \"editor_options\": {\"dummy\": [\"pip\", \"pop\"], \"ping\": null},"
        " \"classNames\": \"form-control\""
        " });"
        " id_field.provide();"
        " </script>"
        "</div>"
    )


def test_field(settings):
    """
    Building a form field with abstract field class.
    """
    editor = RichEditorDefinition(
        name="Foobar",
        css=["css/bundle-foo.css"],
        js=["js/bundle-bar.js"],
    )

    # Without editor init
    class DummyForm(forms.Form):
        field = DjangoBaseEditorField(
            label="Rich text",
            editor=editor,
            init_editor=False,
        )

    form = DummyForm()

    assert html_element(form.as_div()) == html_element(
        "<div>"
        "<label for=\"id_field\">Rich text:</label>"
        "<textarea name=\"field\" cols=\"40\" rows=\"10\" required id=\"id_field\">"
        "</textarea>"
        "</div>"
    )

    assert html_element(str(form.media)) == html_element(
        "<link href=\"/static/css/bundle-foo.css\" media=\"all\" rel=\"stylesheet\">"
        "<script src=\"/static/js/bundle-bar.js\"></script>"
    )


def test_field_init(settings):
    """
    Building a form field with abstract field class and init option.
    """
    editor = RichEditorDefinition(
        name="Foobar",
        css=["css/bundle-foo.css"],
        js=["js/bundle-bar.js"],
    )

    # Again with editor init
    class DummyForm(forms.Form):
        field = DjangoBaseEditorField(
            label="Rich text",
            editor=editor,
            init_editor=True,
            editor_options={"dummy": ["pip", "pop"], "ping": None},
        )

    form = DummyForm()

    assert html_element(form.as_div()) == html_element(
        "<div>"
        "<label for=\"id_field\">Rich text:</label>"
        "<textarea name=\"field\" cols=\"40\" rows=\"10\" required id=\"id_field\">"
        "</textarea>"
        "<script>"
        "let id_field = new DjangoFoobar({"
        " \"source\": document.querySelector(\"#id_field\"),"
        " \"editor_options\": {\"dummy\": [\"pip\", \"pop\"], \"ping\": null},"
        " \"classNames\": \"form-control\""
        " });"
        " id_field.provide();"
        " </script>"
        "</div>"
    )
