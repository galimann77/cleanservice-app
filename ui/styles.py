import os

def get_css():
    """
    Loads the custom CSS file from the styles directory.
    """
    css_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "styles", "custom.css")
    
    try:
        with open(css_file_path, "r") as f:
            css_content = f.read()
            return f"<style>{css_content}</style>"
    except FileNotFoundError:
        return "<style></style><!-- Custom CSS not found -->"
    except Exception as e:
        return f"<style></style><!-- Error loading CSS: {e} -->"
