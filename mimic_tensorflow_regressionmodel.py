__metaclass__ = type
import numpy as np
class Operation():
    def __init__(self, input_nodes = []):
        self.input_nodes = input_nodes
        self.output_nodes = [] 
        for node in input_nodes:
            node.output_nodes.append(self)
        _default_graph.operations.append(self)
    def compute(self):
        pass
class add(Operation):
    def __init__(self, x, y):    
        super(add,self).__init__([x, y])
    def compute(self, x_var, y_var):   
        self.inputs = [x_var, y_var]
        return x_var + y_var
class multiply(Operation):
    def __init__(self, a, b):  
        super(multiply,self).__init__([a, b])
    def compute(self, a_var, b_var):   
        self.inputs = [a_var, b_var]
        return a_var * b_var
class matmul(Operation):
    def __init__(self, a, b):   
        super(matmul,self).__init__([a, b])
    def compute(self, a_mat, b_mat):
        self.inputs = [a_mat, b_mat]
        return a_mat.dot(b_mat)
class Placeholder():
    def __init__(self):
        self.output_nodes = []
        _default_graph.placeholders.append(self)

class Variable():
    def __init__(self, initial_value = None):
        self.value = initial_value
        self.output_nodes = []
        _default_graph.variables.append(self)
class Graph():
    def __init__(self):
        
        self.operations = []
        self.placeholders = []
        self.variables = []
        
    def set_as_default(self):
        global _default_graph
        _default_graph = self
g = Graph()
g.set_as_default()
A = Variable(10)
b = Variable(1)
# Will be filled out later
x = Placeholder()
y = multiply(A,x)
z = add(y,b)
def traverse_postorder(operation):
    """ 
    PostOrder Traversal of Nodes. Basically makes sure computations are done in 
    the correct order (Ax first , then Ax + b). Feel free to copy and paste this code.
    It is not super important for understanding the basic fundamentals of deep learning.
    """
    
    nodes_postorder = []
    def recurse(node):
        if isinstance(node, Operation):
            for input_node in node.input_nodes:
                recurse(input_node)
        nodes_postorder.append(node)
    recurse(operation)
    return nodes_postorder
class Session:
    def run(self, operation, feed_dict = {}):
        nodes_postorder = traverse_postorder(operation)
        for node in nodes_postorder:
            if type(node) == Placeholder:
                node.output = feed_dict[node]   
            elif type(node) == Variable:    
                node.output = node.value   
            else: # Operation    
                node.inputs = [input_node.output for input_node in node.input_nodes]     
                node.output = node.compute(*node.inputs)
            if type(node.output) == list:
                node.output = np.array(node.output)
        return operation.output
sess = Session()
result = sess.run(operation=z,feed_dict={x:10})
print(result)
g = Graph()
g.set_as_default()
A = Variable([[10,20],[30,40]])
b = Variable([1,1])
x = Placeholder()
y = matmul(A,x)
z = add(y,b)
sess = Session()
result = sess.run(operation=z,feed_dict={x:10})
print(result)

