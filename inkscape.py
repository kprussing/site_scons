__doc__="""Define the builders for Inkscape.

These convert SVG to PNG and PDF + LaTeX.

"""

import os
import platform
import re

from SCons.Script import Builder

if platform.uname()[0] == "Windows":
    # Mind the hard coding!
    cmd = os.path.join( 
            "C:"+os.sep, "PROGRA~1", "Inkscape", "inkscape.com"
        )
elif re.match("CYGWIN", platform.uname()[0]):
    cmd = os.path.join(
            "/cygdrive", "c", "PROGRA~1", "Inkscape", "inkscape.com"
        )
else:
    cmd = "inkscape"

def latex_emitter(target, source, env):
    """The emitter for LaTeX exporting from Inkscape."""
    target.append(str(target[0]) + "_tex")
    return target, source

svg2pngcmd = [ 
        cmd, "--without-gui", "-f", "$SOURCE", 
        "--export-png", "$TARGET"
    ]
svg2png = Builder(
        action=" ".join(svg2pngcmd), suffix=".png", src_suffix=".svg"
    )

svg2pdfcmd = svg2pngcmd
svg2pdfcmd[4] = "--export-pdf"
svg2pdf = Builder(
        action=" ".join(svg2pdfcmd), suffix=".pdf", src_suffix=".svg"
    )

svg2pdfcmd += ["--export-latex"]
svg2pdfcmd[4] = "--export-pdf"
svg2pdf_tex = Builder(
        action=" ".join(svg2pdfcmd), suffix=".pdf", 
        src_suffix=".svg", emitter=latex_emitter
    )

pdf2svgcmd = svg2pngcmd
pdf2svgcmd[4] = "--export-plain-svg"
pdf2svg = Builder(
        action=" ".join(svg2pdfcmd), suffix=".svg", src_suffix=".pdf"
    )

def add_inkscape(env):
    """The SCons definition of the tool.
    
    Per the documentation, the tool is a function that operates on the
    Environment.

    Parameters
    ----------

    env: :class:`Environment`
        The SCons Environment.

    """
    BUILDERS={
            "svg2png" : svg2png,
            "svg2pdf_tex" : svg2pdf,
            "svg2pdf" : svg2pdf,
            "pdf2svg" : pdf2svg
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

