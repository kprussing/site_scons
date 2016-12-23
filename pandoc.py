__doc__="""Define the builder for Pandoc.

"""

import os
import re

from SCons.Script import Builder

data_dir = os.path.abspath(os.curdir)
template = os.path.join(os.curdir, "templates", "default.latex")
preamble = os.path.join(data_dir, "preamble.tex")
myfilter = os.path.join(data_dir, "site_scons", "myfilter.py")

pandoccmd = [
        "pandoc", "--standalone",
        "--data-dir=" + data_dir,
        "--filter=" + myfilter,
        "--filter=pandoc-eqnos",
        "--filter=pandoc-fignos",
        "-o", "$TARGET", "$SOURCES"
    ]

docxflags = [
        "--filter=pandoc-citeproc",
    ]
latexflags = [
        "--data-dir=" + data_dir,
        "--natbib",
        "--include-in-header=" + preamble
    ]
htmlflags = docxflags + ["--mathjax"]

def add_pandoc(env):
    """Add the Pandoc command to the environment."""
    Pandoc = Builder(
            action=" ".join(pandoccmd),
            src_suffix=[".md", ".markdown", ".txt"],
            chdir=1
        )
    md2docx = Builder(
            action=" ".join(pandoccmd + docxflags),
            src_suffix=[".md", ".markdown", ".txt"],
            chdir=1
        )
    md2latex = Builder(
            action=" ".join(pandoccmd + latexflags),
            src_suffix=[".md", ".markdown", ".txt"],
            chdir=1
        )
    md2html = Builder(
            action=" ".join(pandoccmd + htmlflags),
            src_suffix=[".md", ".markdown", ".txt"],
            chdir=1
        )
    BUILDERS = {
            "Pandoc" : Pandoc,
            "md2docx" : md2docx,
            "md2latex" : md2latex,
            "md2html" : md2html,
        }
    env.AppendUnique(BUILDERS=BUILDERS)


# Copyright (c) 2016-2017 Keith F. Prussing
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
# 
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 

