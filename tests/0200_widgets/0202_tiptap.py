from django_editors.utils.tests import html_element


def test_widget_tiptap(settings):
    """
    TipTap widget render and media assets should be as expected.
    """
    definition = settings.EDITORS["TipTap"]
    widget = definition.get_widget_object(init_editor=False)

    input_render = widget.render("text", "<p>A <b>rich</b> content</p>")
    assert html_element(input_render) == html_element(
        "<textarea id=\"id_text\" name=\"text\" cols=\"40\" rows=\"10\">"
        "&lt;p&gt;A &lt;b&gt;rich&lt;/b&gt; content&lt;/p&gt;"
        "</textarea>"
    )

    widget = definition.get_widget_object(
        init_editor=True,
        editor_options={"dummy": ["pip", "pop"], "ping": None},
    )
    input_render = widget.render("text", "<p>A <b>rich</b> content</p>")
    assert html_element(input_render) == html_element(
        "<textarea id=\"id_text\" name=\"text\" cols=\"40\" rows=\"10\">"
        "&lt;p&gt;A &lt;b&gt;rich&lt;/b&gt; content&lt;/p&gt;"
        "</textarea>"
        "<script>"
        "let id_text = new DjangoTipTap({"
        " \"source\": document.querySelector(\"#id_text\"),"
        " \"editor_options\": {\"dummy\": [\"pip\", \"pop\"], \"ping\": null},"
        " \"classNames\": \"form-control\""
        " });"
        " id_text.provide();"
        " </script>"
    )

    assert html_element(str(widget.media)) == html_element(
        "<script src=\"/static/js/bundle-tiptap.js\"></script>"
    )
