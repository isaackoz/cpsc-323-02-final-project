class ASTNode:
    def __init__(self, type, children=None, leaf=None):
        self.type = type
        self.children = children if children is not None else []
        self.leaf = leaf

class AssignmentNode(ASTNode):
    def __init__(self, left, right):
        super().__init__('Assignment', [left, right])

class VariableNode(ASTNode):
    def __init__(self, name):
        super().__init__('Variable', leaf=name)

class NumberNode(ASTNode):
    def __init__(self, value):
        super().__init__('Number', leaf=value)
