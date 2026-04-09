from django_editors.utils.tests import html_element


def test_widget_suneditor(settings):
    """
    SunEditor widget render and media assets should be as expected.
    """
    definition = settings.EDITORS["SunEditor"]
    widget = definition.get_widget_object(init_editor=False)

    input_render = widget.render("text", "<p>A <b>rich</b> content</p>")
    assert html_element(input_render) == html_element(
        "<textarea id=\"id_text\" name=\"text\" cols=\"40\" rows=\"10\">"
        "&lt;p&gt;A &lt;b&gt;rich&lt;/b&gt; content&lt;/p&gt;"
        "</textarea>"
    )

    widget = definition.get_widget_object(init_editor=True)
    input_render = widget.render("text", "<p>A <b>rich</b> content</p>")
    assert html_element(input_render) == html_element(
        "<textarea id=\"id_text\" name=\"text\" cols=\"40\" rows=\"10\">"
        "&lt;p&gt;A &lt;b&gt;rich&lt;/b&gt; content&lt;/p&gt;"
        "</textarea>"
        "<script>"
        "let id_text = new DjangoSunEditor({"
        " \"source\": document.querySelector(\"#id_text\"),"
        " \"classNames\": \"form-control\""
        " });"
        " id_text.provide();"
        " </script>"
    )

    assert html_element(str(widget.media)) == html_element(
        "<link href=\"/static/js/suneditor.min.css\" media=\"all\" rel=\"stylesheet\">"
        "<script src=\"/static/js/bundle-suneditor.js\">"
    )
