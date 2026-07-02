from document_utils import build_context_with_document


def test_document_context_is_built():
    result = build_context_with_document("What is this?", "Sample document text")
    assert "Document content" in result
    assert "What is this?" in result
