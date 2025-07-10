import os

def write_python_files_to_text(base_dir, output_file):
    with open(output_file, 'w', encoding='utf-8') as out_file:
        for root, dirs, files in os.walk(base_dir):
            # Exclude the .venv folder
            dirs[:] = [d for d in dirs if d != '.venv']
            for file in files:
                if file.endswith('.py') and file != '__init__.py' and file != 'code reader.py' and file != 'gifconverter.py':
                    file_path = os.path.join(root, file)
                    out_file.write(f"Path: {file_path}\n")
                    out_file.write("-" * 80 + "\n")
                    with open(file_path, 'r', encoding='utf-8') as py_file:
                        out_file.write(py_file.read())
                    out_file.write("\n" + "=" * 80 + "\n\n")

# Replace 'your_codebase_directory' with the path to your codebase
base_directory = 'C:\FPOS\kpapython\kpa'
output_file_path = 'output.txt'

write_python_files_to_text(base_directory, output_file_path)