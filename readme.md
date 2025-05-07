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


The generated files have the following structure, see `pfr.json` for the graph for the Lean PFR formalisation extracted on <07-05-2024>:
```json
{
   "b3a101d5a83231b0febb33a487a6322537d0d9ae":
     "date": "<string> 2023-11-15T02:57:58",
     graph:  [ {
         id: <string> "entropy-def",
         node_deps: ["entropy-def"],
         node_lean_decls: ["entropy"],
         node_name: <string> "thmenv",
         node_title: <string> "Entropy",
         node_source: <string> "\begin{thmenv}[Entropy] ...",
         node_caption: <string> "Definition",
         node_caption_name: <string> "Theorem",
         node_tag_name: <string> "definition",
         node_full_title: <string> "1.1 Entropy",
         node_text_content: <string> "If X is an S-valued random variable, the entropy H[X] of X is defined  H[X] := ∑s S P[X=x]  with the convention that 0  = 0. ",
         node_can_state: <boolean> "true",
         node_can_prove: <boolean> "false",
         node_proved:  <boolean> "false",
         node_fully_proved: <boolean> "true"
      } ]
}
```

