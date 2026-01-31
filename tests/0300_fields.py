from django import forms

from django_editors.widgets import DjangoBaseEditorWidget
from django_editors.formfields import DjangoBaseEditorField, TipTapField
from django_editors.utils.tests import html_element


def test_with_abstract_widget(settings):
    """
    Building a field using simple CharField and the abtract editor class should work
    as expected.
    """
    class DummyForm(forms.Form):
        field = forms.CharField(
            label="Rich text",
            widget=DjangoBaseEditorWidget(
                editor=settings.EDITORS["TipTap"],
                editor_init=False,
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

    class DummyForm(forms.Form):
        field = forms.CharField(
            label="Rich text",
            widget=DjangoBaseEditorWidget(
                editor=settings.EDITORS["TipTap"],
                editor_init=True,
            )
        )

    form = DummyForm()

    assert html_element(form.as_div()) == html_element(
        "<div>"
        "<label for=\"id_field\">Rich text:</label>"
        "<textarea name=\"field\" cols=\"40\" rows=\"10\" required id=\"id_field\">"
        "</textarea>"
        "<script>"
        "let id_field = new DjangoTipTap({"
        " \"source\": document.querySelector(\"#id_field\"),"
        " \"classNames\": \"form-control\""
        " });"
        " id_field.provide();"
        " </script>"
        "</div>"
    )


def test_with_concrete_widget(settings):
    """
    Building a field using simple CharField and concrete TipTap editor class should
    work as expected.
    """
    class DummyForm(forms.Form):
        field = forms.CharField(
            label="Rich text",
            widget=settings.EDITORS["TipTap"].get_widget_object(editor_init=False)
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
        "<script src=\"/static/js/bundle-tiptap.js\"></script>"
    )

    # Again but set widget with editor initialization
    class DummyForm(forms.Form):
        field = forms.CharField(
            label="Rich text",
            widget=settings.EDITORS["TipTap"].get_widget_object(editor_init=True)
        )

    form = DummyForm()

    assert html_element(form.as_div()) == html_element(
        "<div>"
        "<label for=\"id_field\">Rich text:</label>"
        "<textarea name=\"field\" cols=\"40\" rows=\"10\" required id=\"id_field\">"
        "</textarea>"
        "<script>"
        "let id_field = new DjangoTipTap({"
        " \"source\": document.querySelector(\"#id_field\"),"
        " \"classNames\": \"form-control\""
        " });"
        " id_field.provide();"
        " </script>"
        "</div>"
    )

    assert html_element(str(form.media)) == html_element(
        "<script src=\"/static/js/bundle-tiptap.js\"></script>"
    )


def test_base_field(settings):
    """
    Building a form field with abstract field class.
    """
    # Without editor init
    class DummyForm(forms.Form):
        field = DjangoBaseEditorField(
            label="Rich text",
            editor=settings.EDITORS["TipTap"],
            editor_init=False,
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
        "<script src=\"/static/js/bundle-tiptap.js\"></script>"
    )

    # Again with editor init
    class DummyForm(forms.Form):
        field = DjangoBaseEditorField(
            label="Rich text",
            editor=settings.EDITORS["TipTap"],
            editor_init=True,
        )

    form = DummyForm()

    assert html_element(form.as_div()) == html_element(
        "<div>"
        "<label for=\"id_field\">Rich text:</label>"
        "<textarea name=\"field\" cols=\"40\" rows=\"10\" required id=\"id_field\">"
        "</textarea>"
        "<script>"
        "let id_field = new DjangoTipTap({"
        " \"source\": document.querySelector(\"#id_field\"),"
        " \"classNames\": \"form-control\""
        " });"
        " id_field.provide();"
        " </script>"
        "</div>"
    )


def test_concrete_field(settings):
    """
    Building a form field with concrete field class.
    """
    # Without editor init
    class DummyForm(forms.Form):
        field = TipTapField(label="Rich text", editor_init=False)

    form = DummyForm()

    assert html_element(form.as_div()) == html_element(
        "<div>"
        "<label for=\"id_field\">Rich text:</label>"
        "<textarea name=\"field\" cols=\"40\" rows=\"10\" required id=\"id_field\">"
        "</textarea>"
        "</div>"
    )

    assert html_element(str(form.media)) == html_element(
        "<script src=\"/static/js/bundle-tiptap.js\"></script>"
    )

    # Again with editor init and options
    class DummyForm(forms.Form):
        field = TipTapField(
            label="Rich text",
            editor_init=True,
            editor_options={"dummy": ["pip", "pop"], "ping": None},
        )

    form = DummyForm()

    assert html_element(form.as_div()) == html_element(
        "<div>"
        "<label for=\"id_field\">Rich text:</label>"
        "<textarea name=\"field\" cols=\"40\" rows=\"10\" required id=\"id_field\">"
        "</textarea>"
        "<script>"
        "let id_field = new DjangoTipTap({"
        " \"source\": document.querySelector(\"#id_field\"),"
        " \"editor_options\": {\"dummy\": [\"pip\", \"pop\"], \"ping\": null},"
        " \"classNames\": \"form-control\""
        " });"
        " id_field.provide();"
        " </script>"
        "</div>"
    )
