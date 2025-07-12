import os

# Base directory where your actual source files exist
SOURCE_BASE = "."

# Output directory for tests
TESTS_DIR = "tests"

# Subdirectories to mirror
MODULE_DIRS = [
    "core/models",
    "core/services",
    "database",
    "ui/billing/action_buttons",
    "ui/billing/billing_list",
    "ui/billing/keypad",
    "ui/billing/section",
    "ui/main",
    "ui/product",
    "ui/title_bar"
]

# File mapping rules
def get_test_filename(source_filename):
    base = os.path.basename(source_filename)
    if base.endswith(".py") and not base.startswith("__"):
        return f"test_{base}"
    return None

# Start script
def create_test_structure():
    for module_dir in MODULE_DIRS:
        source_path = os.path.join(SOURCE_BASE, module_dir)
        test_path = os.path.join(TESTS_DIR, module_dir)

        if not os.path.exists(source_path):
            print(f"⚠️ Skipped missing source: {source_path}")
            continue

        os.makedirs(test_path, exist_ok=True)
        print(f"✅ Created: {test_path}")

        for filename in os.listdir(source_path):
            if not filename.endswith(".py") or filename.startswith("__"):
                continue

            test_filename = get_test_filename(filename)
            if not test_filename:
                continue

            test_file_path = os.path.join(test_path, test_filename)
            if not os.path.exists(test_file_path):
                with open(test_file_path, "w") as f:
                    f.write(f"""import pytest

# TODO: Add tests for {filename}
def test_placeholder():
    assert True
""")
                print(f"📝 Created test file: {test_file_path}")
            else:
                print(f"⏭️ Skipped existing: {test_file_path}")

if __name__ == "__main__":
    create_test_structure()
