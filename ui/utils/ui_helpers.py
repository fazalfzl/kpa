# File: utils/ui_helpers.py
def toggle_visibility(widgets, visible):
    for widget in widgets:
        widget.setVisible(visible)