from plasTeX.TeX import TeX
from plasTeX import TeXDocument
from plasTeX import Config
from pathlib import Path
import os
from contextlib import contextmanager

@contextmanager
def cwd(path):
    "changes directory to a given path"
    prev = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev)


def load_blueprint_doc(project_path: str) -> TeXDocument:
    """Given a PROJECT_PATH extracts the corresponding TeXDocument."""
    BLUEPRINT_DIR = Path(project_path) / 'blueprint'
    LATEX_DIR = BLUEPRINT_DIR / 'src'
    CONFIG_PATH = LATEX_DIR / 'plastex.cfg'

    config: Config = Config.defaultConfig()
    config.read([CONFIG_PATH])

    tex = TeX()
    tex.ownerDocument.config = config
    tex.ownerDocument.userdata['jobname'] = 'extract_graph'
    tex.ownerDocument.userdata['working-dir'] = '.'
    with cwd(LATEX_DIR):
        tex.input(open("web.tex").read())
        doc = tex.parse()

    return doc

def serialise_blueprint_graph(doc: TeXDocument):
    """Given a blueprint document, extracts the dependency graph as a json"""
    results = []
    for graph in doc.userdata['dep_graph']['graphs'].values():
        for node in graph.nodes:
            node_deps = node.userdata.get('uses', [])
            node_deps = [dep.id for dep in node_deps]
            node_lean_decls = node.userdata.get('leandecls', [])
            node_name = node.nodeName
            node_title = node.title.source if node.title else ''
            node_source = node.source
            node_caption = node.caption
            node_caption_name = node.captionName.source if node.captionName else ''
            node_tag_name = node.tagName
            node_full_title = node.fullTitle.source if hasattr(node, 'fullTitle') and node.fullTitle else ''
            node_text_content = node.textContent
            node_can_state = node.userdata.get('can_state', False)
            node_can_prove = node.userdata.get('can_prove', False)
            node_proved = node.userdata.get('proved', False)
            node_fully_proved = node.userdata.get('fully_proved', False)

            node_obj = {
              'id': node.id,
              'node_deps': node_deps,
              'node_lean_decls': node_lean_decls,
              'node_name': node_name,
              'node_title': node_title,
              'node_source': node_source,
              'node_caption': node_caption,
              'node_caption_name': node_caption_name,
              'node_tag_name': node_tag_name,
              'node_full_title': node_full_title,
              'node_text_content': node_text_content,
              'node_can_state': node_can_state,
              'node_can_prove': node_can_prove,
              'node_proved': node_proved,
              'node_fully_proved': node_fully_proved,
            }
            results.append(node_obj)

    return results
