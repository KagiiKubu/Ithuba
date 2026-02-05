from streamlit.testing.v1 import AppTest

def test_app_startup():
    at = AppTest.from_file("app/main.py").run()
    assert at.title[0].value == "Ithuba" 
    assert at.sidebar
    assert not at.exception