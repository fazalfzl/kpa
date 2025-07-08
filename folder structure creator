import os


def create_package_structure(base_dir):
    structure = {
        "ui2": {
            "main": ["pos_main_ui.py", "pos_main_controller.py"],
            "title_bar": ["ui.py", "logic.py"],
            "product": ["editor.py", "order_dialog.py", "manager_dialog.py"],
            "billing": {
                "action_buttons": ["logic.py", "ui.py"],
                "billing_list": ["item_widget.py", "logic.py", "ui.py"],
                "keypad": ["logic.py", "ui.py"],
                "section": ["logic.py", "ui.py"],
            },
        },
        "utils": {
            "styles": ["styles.py"],
            "constants.py": None,
        },
    }

    def create_dir_and_files(path, content):
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            with open(os.path.join(path, "__init__.py"), "w") as f:
                pass  # Create __init__.py
            for sub_path, sub_content in content.items():
                create_dir_and_files(os.path.join(path, sub_path), sub_content)
        elif isinstance(content, list):
            os.makedirs(path, exist_ok=True)
            with open(os.path.join(path, "__init__.py"), "w") as f:
                pass  # Create __init__.py
            for file_name in content:
                with open(os.path.join(path, file_name), "w") as f:
                    pass  # Create empty file
        elif content is None:
            with open(path, "w") as f:
                pass  # Create empty file

    create_dir_and_files(base_dir, structure)


# Replace 'your_project_directory' with the desired base directory for your project
base_directory = "C:\FPOS\kpapython\kpa"
create_package_structure(base_directory)
