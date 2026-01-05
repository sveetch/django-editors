from django import forms

from django_editors.widgets import DjangoBaseEditorWidget
from django_editors.utils.tests import html_element
from django_editors.editors import RichEditorRuler


def test_base(settings):
    """
    Build a TipTap widget in the raw way should render as expected.
    """
    widget = DjangoBaseEditorWidget(
        editor_metadata=RichEditorRuler(
            name="Foobar",
            css=["css/bundle-foo.css"],
            js=["js/bundle-bar.js"],
        )
    )

    input_render = widget.render("text", "<p>A <b>rich</b> content</p>")

    assert html_element(input_render) == html_element(
        "<textarea name=\"text\" cols=\"40\" rows=\"10\">"
        "&lt;p&gt;A &lt;b&gt;rich&lt;/b&gt; content&lt;/p&gt;"
        "</textarea>"
    )

    assert html_element(str(widget.media)) == html_element(
        "<link href=\"/static/css/bundle-foo.css\" media=\"all\" rel=\"stylesheet\">"
        "<script src=\"/static/js/bundle-bar.js\"></script>"
    )


def test_widget_tiptap(settings):
    """
    TipTap widget render and media assets should be as expected.
    """
    ruler = settings.EDITORS["TipTap"]
    widget = ruler.get_widget_object()

    input_render = widget.render("text", "<p>A <b>rich</b> content</p>")

    assert html_element(input_render) == html_element(
        "<textarea name=\"text\" cols=\"40\" rows=\"10\">"
        "&lt;p&gt;A &lt;b&gt;rich&lt;/b&gt; content&lt;/p&gt;"
        "</textarea>"
    )

    assert html_element(str(widget.media)) == html_element(
        "<script src=\"/static/js/bundle-tiptap.js\"></script>"
    )


def test_widget_suneditor(settings):
    """
    SunEditor widget render and media assets should be as expected.
    """
    ruler = settings.EDITORS["SunEditor"]
    widget = ruler.get_widget_object()

    input_render = widget.render("text", "<p>A <b>rich</b> content</p>")

    assert html_element(input_render) == html_element(
        "<textarea name=\"text\" cols=\"40\" rows=\"10\">"
        "&lt;p&gt;A &lt;b&gt;rich&lt;/b&gt; content&lt;/p&gt;"
        "</textarea>"
    )

    assert html_element(str(widget.media)) == html_element(
        "<link href=\"/static/js/suneditor.min.css\" media=\"all\" rel=\"stylesheet\">"
        "<script src=\"/static/js/bundle-suneditor.js\">"
    )
