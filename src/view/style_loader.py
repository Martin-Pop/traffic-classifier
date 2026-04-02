from common.file import get_absolute_path

def apply_stylesheet(app, qss_file='src/view/styles.qss'):
    qss_path = get_absolute_path(qss_file)

    try:
        with open(qss_path, 'r', encoding='utf-8') as f:
            qss_content = f.read()
        app.setStyleSheet(qss_content)
    except Exception as e:
        raise Exception(f"Error loading stylesheet: {e}")