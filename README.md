A decompiler for Emacs Lisp bytecode... or at least a proof of concept.

This code uses the [Python spark-parser](https://pypi.python.org/pypi/spark_parser/) for its Earley algorithm parser and the code organization.

This is in a very early stage, but amazingly the code seems sound so
far.

Until docs are better organized, see
[Writing Semantic-action Rules](https://github.com/rocky/python-spark/wiki/Writing-Semantic-action-rules)
and the
https://github.com/rocky/python-uncompyle6/wiki/Deparsing-Paper for a
more general overview.

There isn't a lot on the detals of Elisp bytecode, but see [the section on Elisp
Disassembly](https://www.gnu.org/software/emacs/manual/html_node/elisp/Disassembly.html).

You may find yourself consulting the source code: [`emacs/src/data.c`](http://git.savannah.gnu.org/cgit/emacs.git/tree/src/data.c) and [`emacs/src/bytecode.c`](http://git.savannah.gnu.org/cgit/emacs.git/tree/src/bytecode.c).


Until this is rewritten into Emacs Lisp, this project uses the text
output from that as its input. (We lose the full text of docstrings in
the process).
