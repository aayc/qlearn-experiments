class Node:
	def __init__(self, name):
		self.name = name;
		self.neighbors = [];
		self.index = -1;
		self.lowlink = 0;

	def addNeighbor(self, other):
		self.neighbors.append(other);

	def __repr__(self):
		return self.name


def strongConnect (node, next, stack):
	node.index = next;
	node.lowlink = next;
	next += 1;

	stack.append(node);
	print node.name, " is on the stack now";
	for neighbor in node.neighbors:
		if neighbor.index == -1:
			next = strongConnect(neighbor, next, stack);
			node.lowlink = min(node.lowlink, neighbor.lowlink);
		elif node in stack:
			print "I think ", node.name, " is on the stack."
			node.lowlink = min(node.lowlink, neighbor.index);
	
	if node.lowlink == node.index:
		# We're at the root.
		offStack = Node("NONE");
		component = [];
		while offStack.name != node.name:
			offStack = stack.pop()
			print offStack.name
			component.append(offStack);

		components.append(component);

	return next;

from collections import deque;

nodes = [Node("A"), Node("B"), Node("C"), Node("D"), Node("E")]
conns = [["A", "B C"], ["B", "C A"], ["C", "A B D"], ["D", "E"]];
for conn in conns:
	n1 = filter(lambda x: x.name == conn[0], nodes)[0];
	others = conn[1].split(" ");
	for other in others:
		otherAsNode = filter(lambda x: x.name == other, nodes)[0];
		n1.addNeighbor(otherAsNode);

components = [];
next = 0;
stack = deque();
for n in nodes:
	if n.index == -1:
		strongConnect(n, next, stack);
print components;