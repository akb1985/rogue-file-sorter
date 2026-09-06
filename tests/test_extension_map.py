from src.sorter.extension_map import ExtensionResolver

def test_resolver_mappings():
    mapping = {".pdf": "/docs", ".JPG": "/pics"}
    resolver = ExtensionResolver(mapping)
    
    assert resolver.get_destination("file.pdf") == "/docs"
    assert resolver.get_destination("PHOTO.JPG") == "/pics"
    assert resolver.get_destination("PHOTO.jpg") == "/pics"
    assert resolver.get_destination("download.crdownload") is None
    assert resolver.get_destination("readme") is None