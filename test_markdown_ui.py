def test_markdown_renderer_contains_code_and_bold_markup():
    from app import renderMarkdown

    result = renderMarkdown('Use **bold** and `code`')
    assert '<strong>bold</strong>' in result
    assert '<code>code</code>' in result
