__doc__="""Define the builder for calling REVTeX.

The REVTeX 4.1 builder emits and additional bibliography files that is
<root>Notes.bib.  We need to tell SCons that this file is emitted and
needs to be cleaned up.

"""

import copy
import os

from SCons.Builder import BuilderBase

def emitter(target, source, env):
    import platform

    pdf_emitter = env["BUILDERS"]["PDF"].emitter

    _, ext = os.path.splitext(str(source[0]))
    if ext in pdf_emitter:
        target, source = pdf_emitter[ext](
                target=target, source=source, env=env
            )

    # print [str(x) for x in target]
    # print [str(x) for x in source]
    if platform.uname()[0] == "Windows":
        # I don't know why Windows can't get this right, but OSX knows
        # about this.
        target.append(os.path.splitext(str(source[0]))[0] + "Notes.bib")

    # print [str(x) for x in target]
    return target, source

def add_revtex(env):
    """Add the REVTeX4 Builder to the environment."""
    pdf = env["BUILDERS"]["PDF"]

    # Clone the PDF builder as a starting point.
    revtex = BuilderBase(
            action = pdf.action,
            prefix = pdf.prefix,
            suffix = pdf.suffix,
            src_suffix = pdf.src_suffix,
            target_factory = pdf.target_factory,
            source_factory = pdf.source_factory,
            target_scanner = pdf.target_scanner,
            source_scanner = pdf.source_scanner,
            emitter = copy.deepcopy(pdf.emitter),
            multi = pdf.multi,
            env = pdf.env,
            single_source = pdf.single_source,
            name = "REVTeX",
            chdir = pdf.executor_kw.get("chdir", None),
            is_explicit = pdf.is_explicit,
            src_builder = pdf.src_builder,
            ensure_suffix = pdf.ensure_suffix,
            **pdf.overrides
        )

    # Update the emitter.
    for key in pdf.emitter.keys():
        revtex.add_emitter(key, emitter)

    env.AppendUnique(BUILDERS={"revtex" : revtex})


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

