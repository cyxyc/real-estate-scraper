import os
import pytest
from scraper import get_HTML

def test_get_HTML():
    # Test with the default URL
    get_HTML()
    # Check if the file was created and is not empty
    assert os.path.exists('scraped_HTML.txt')
    assert os.path.getsize('scraped_HTML.txt') > 0
