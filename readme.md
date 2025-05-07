# Lean4 Blueprint Extractor
Some preliminary experiments with extracting metadata from Lean4 blueprints:

```
usage: main.py [-h] [--blueprint-path BLUEPRINT_PATH] [--no-progress]
               project_path output_file

Extract Lean blueprint graphs into JSON format.

positional arguments:
  project_path          Path to the Lean project repository.
  output_file           Path to place the JSON output file.

options:
  -h, --help            show this help message and exit
  --blueprint-path BLUEPRINT_PATH
                        Relative path to blueprint directory inside repository
                        (defaults to blueprint, i.e the directory is at the
                        root).
  --no-progress         Disable progress bars.
```


