import sys
from spark_parser.ast import AST as spark_AST

intern = sys.intern


class SyntaxTree(spark_AST):
    def __init__(self, *args, transformed_by=None, **kwargs):
        self.transformed_by = transformed_by
        super(SyntaxTree, self).__init__(*args, **kwargs)

    def __repr__(self):
        return self.__repr1__("", None)

    def __repr1__(self, indent, sibNum=None):
        rv = str(self.kind)
        if sibNum is not None:
            rv = "%2d. %s" % (sibNum, rv)
        enumerate_children = False
        if len(self) > 1:
            rv += " (%d)" % (len(self))
            enumerate_children = True
        if self.transformed_by is not None:
            if self.transformed_by is True:
                rv += " (transformed)"
            else:
                rv += " (transformed by %s)" % self.transformed_by
        rv = indent + rv
        indent += "    "
        i = 0
        for node in self:
            if hasattr(node, "__repr1__"):
                if enumerate_children:
                    child = node.__repr1__(indent, i)
                else:
                    child = node.__repr1__(indent, None)
            else:
                if enumerate_children:
                    child = indent + "%2d. %s" % (i, inst)
                else:
                    child = indent + inst
                pass
            rv += "\n" + child
            i += 1
        return rv
