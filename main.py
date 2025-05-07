import subprocess 
import json
import sys
import datetime
import argparse
from tqdm import tqdm
from pathlib import Path
from tempfile import TemporaryDirectory
from shutil import copytree
from datetime import datetime
from blueprint_extractor  import load_blueprint_doc, serialise_blueprint_graph

use_tqdm = sys.stdout.isatty()
def progress(iterable, **kwargs):
    return tqdm(iterable, **kwargs) if use_tqdm else iterable

def run_git(args, cwd):
    return subprocess.check_output(
        ['git'] + args, cwd=cwd,
        stderr=subprocess.DEVNULL,
        text=True
    ).strip()

def get_commits_with_blueprint(repo_path, blueprint_path='blueprint'):
    all_commits = run_git(
        ['log', '--reverse', '--pretty=format:%H', '--', blueprint_path],
        cwd=repo_path
    ).splitlines()
    relevant_commits = []
    for commit in progress(all_commits, desc='Filtering commits'):
        try:
            run_git(
                ['cat-file', '-e', f'{commit}:{blueprint_path}'],
                cwd=repo_path
            )
            relevant_commits.append(commit)
        except subprocess.CalledProcessError:
            pass
    return relevant_commits

def get_commit_date(repo_path, commit):
    timestamp = run_git(
        ['show', '-s', '--format=%ct', commit],
        cwd=repo_path
    )
    return datetime.utcfromtimestamp(
        int(timestamp)
    ).isoformat()

def extract_graphs_across_commits(repo_path, blueprint_path='blueprint'):
    print(f'finding relevant commits in project {repo_path}')
    commits = get_commits_with_blueprint(repo_path, blueprint_path=blueprint_path)
    print(f'retrieved relevant commits')
    results = {}
    last_graph_serial = None
    for commit in progress(commits, desc='Extracting graphs'):
        run_git(['checkout', '--quiet', commit], cwd=repo_path)
        try:
            doc = load_blueprint_doc(repo_path)
            graph = serialise_blueprint_graph(doc)
            graph_serial = json.dumps(graph, sort_keys=True)
            if graph_serial != last_graph_serial:
                results[commit] = {
                    'date': get_commit_date(repo_path, commit),
                    'graph': graph
                }
                last_graph_serial = graph_serial
        except Exception as e:
            print(f"Skipping {commit} due to error {e}")
    return results


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Extract Lean blueprint graphs into JSON format"
    )
    parser.add_argument(
        'project_path',
        type=Path,
        help='Path to the Lean project repository.'
    )
    parser.add_argument(
        'output_file',
        type=Path,
        help='Path to place the JSON output file.'
    )
    parser.add_argument(
        '--blueprint-path',
        type=str,
        default="blueprint",
        help="Relative path to blueprint directory inside repository (defaults to blueprint, i.e the directory is at the root)."
    )
    parser.add_argument(
        '--no-progress',
        dest="show_progress",
        action="store_false",
        help="Disable progress bars."
    )
    args = parser.parse_args()
    use_tqdm = args.show_progress
    result = extract_graphs_across_commits(
        args.project_path,
        blueprint_path =  args.blueprint_path
    )
    with args.output_file.open("w") as f:
        json.dump(result, f, indent=2)

    print(f"Written blueprint history to {args.output_file} - ✓")
