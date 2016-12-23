__doc__="""Define the builder for calling MATLAB.

We need a systematic way to call MATLAB to generate plots.  We will also
need to handle the generation of the log file for future reference.

"""

import os
import platform
import subprocess
from SCons.Script import Builder

def emitter(target, source, env):
    """The emitter for generating the log file."""
    target.append(os.path.splitext(str(target[0]))[0] + ".log")
    return target, source


def matlab(target, source, env):
    """Scons signature to execute MATLAB."""
    if platform.uname()[0] == "Windows":
        exe = os.path.join(
                "C:" + os.sep, "PROGRA~1", "MATLAB", "R2016a", "bin",
                "matlab.exe"
            )
    else:
        exe = "matlab"

    parts = os.path.split(str(source[0]))
    wrapper = "val=0; try, {0} {1} {2} {3}; catch err, val=46; end; "\
        "if val~=0, fprintf(2,'%s %s',err.identifier,err.message); "\
        "end; exit(val)"
    mcmd = wrapper.format(
            os.path.splitext(parts[1])[0], str(source[1]),
            str(target[0]), env.get("args", "")
        );
    cmd = [
            exe, "-nosplash", "-wait", "-nodesktop", 
            "-minimize", "-noFigureWindows", 
            "-logfile", str(target[1]), "-r", mcmd
        ]
    return subprocess.call(cmd)


def add_matlab(env):
    """Add the MATLAB Builder to the environment.

    Per the documentation, the tool is a function that operates on the
    Environment.

    Parameters
    ----------

    env: :class:`Environment`
        The SCons Environment.

    """
    MATLAB = Builder(
            action=matlab, emitter=emitter, chdir=1
        )
    env.AppendUnique(BUILDERS={"MATLAB" : MATLAB})


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

