from __future__ import annotations

import sys
from pathlib import Path

from pygments.styles.friendly import FriendlyStyle

# Set the system path
sys.path.insert(0, str(Path("../..").resolve()))

# Set the background color for Pygments style
FriendlyStyle.background_color = "#f3f2f1"

# Project information
project = "Electrogram"
copyright = "2023-present, 5hojib"
author = "5hojib"

# Sphinx extensions
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx_copybutton",
    "sphinx_immaterial",
]

# Intersphinx configuration
intersphinx_mapping = {"python": ("https://docs.python.org/3", None)}

# Document settings
master_doc = "index"
source_suffix = ".rst"
autodoc_member_order = "bysource"

# Paths for templates and static files
templates_path = ["../resources/templates"]

# HTML options
html_copy_source = False
html_title = "Electrogram Docs"
html_theme = "sphinx_immaterial"
html_show_sourcelink = True
html_permalinks = False
html_show_copyright = False
html_show_sphinx = False
html_static_path = ["../resources/static", "_static"]

# Napoleon settings
napoleon_use_rtype = False
napoleon_use_param = False

# Pygments style settings
pygments_style = "friendly"
copybutton_prompt_text = "$ "

# Suppress specific warnings
suppress_warnings = ["image.not_readable"]

# HTML theme options
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
    "palette": [
        {
            "media": "(prefers-color-scheme: light)",
            "scheme": "default",
            "primary": "blue-grey",
            "accent": "light-blue",
            "toggle": {
                "icon": "material/lightbulb-outline",
                "name": "Switch to dark mode",
            },
        },
        {
            "media": "(prefers-color-scheme: dark)",
            "scheme": "slate",
            "primary": "blue-grey",
            "accent": "lime",
            "toggle": {
                "icon": "material/lightbulb",
                "name": "Switch to light mode",
            },
        },
    ],
    "toc_title_is_page_title": True,
}

# HTML resources
html_logo = "https://github.com/5hojib/5hojib/raw/main/images/book.gif"
html_favicon = "_static/fav.svg"

# LaTeX configuration
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

# Custom CSS files
html_css_files = [
    "css/custom.css",
    "css/all.min.css",
]
