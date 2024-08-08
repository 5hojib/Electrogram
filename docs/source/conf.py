from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.abspath("../.."))

from pygments.styles.friendly import FriendlyStyle

from pyrogram import __version__

FriendlyStyle.background_color = "#f3f2f1"

project = "Electrogram"
copyright = "2023-present, 5hojib"
author = "5hojib"

version = ".".join(__version__.split(".")[:-1])

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx_copybutton",
    "sphinx_immaterial",
]

intersphinx_mapping = {"python": ("https://docs.python.org/3", None)}

master_doc = "index"
source_suffix = ".rst"
autodoc_member_order = "bysource"

templates_path = ["../resources/templates"]
html_copy_source = False

napoleon_use_rtype = False
napoleon_use_param = False

pygments_style = "friendly"

copybutton_prompt_text = "$ "

suppress_warnings = ["image.not_readable"]

html_title = "Electrogram Documentation"
html_theme = "sphinx_immaterial"
html_static_path = ["../resources/static", "_static"]
html_show_sourcelink = True
html_show_copyright = False
html_theme_options = {
    "icon": {
        "repo": "fontawesome/brands/github",
        "edit": "material/file-edit-outline",
    },
    "site_url": "https://electrogram-docs.vercel.app/",
    "repo_url": "https://github.com/5hojib/Electrogram/",
    "repo_name": "Electrogram",
    "globaltoc_collapse": True,
    "features": [
        "navigation.expand",
        "navigation.tabs",
        "navigation.sections",
        "navigation.top",
        "search.share",
        "toc.follow",
        "toc.sticky",
        "content.tabs.link",
        "announce.dismiss",
    ],
    "palette": [{"media": "(prefers-color-scheme: dark)", "scheme": "slate"}],
    "toc_title_is_page_title": True,
    "version_dropdown": True,
    "version_info": [
        {"version": "main", "title": "main", "aliases": ["latest"]},
        {"version": "staging", "title": "staging", "aliases": []},
    ],
}

html_logo = "../resources/static/img/pyrogram.png"
html_favicon = "../resources/static/img/favicon.ico"

latex_engine = "xelatex"
latex_logo = "../resources/static/img/pyrogram.png"

latex_elements = {
    "pointsize": "12pt",
    "fontpkg": r"""
        \setmainfont{Open Sans}
        \setsansfont{Bitter}
        \setmonofont{Ubuntu Mono}
        """,
}

html_css_files = [
    "css/custom.css",
    "css/all.min.css",
]
