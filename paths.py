#!/usr/bin/python

#f = open('pt-april-comcast.txt', 'r')
f = open('path-sea-1-output.txt', 'r')

def hops_to_routenodes(hops):
	node = RouteNode(hops[0])
	if len(hops) > 1:
		node.addChild(hops_to_routenodes(hops[1:]))
	return node

def print_routenode(rn, max_depth, indent=0):
	if indent > max_depth:
		return
	print("".join(["\t" for i in range(indent)]) + rn.getMe() + ":" + str(rn.getHeat()))
	for i in rn.getChildren():
		print_routenode(i, max_depth, indent+1)

class RouteNode:
	def __init__(self, me):
		self.me = me
		self.children = []
		self.heat = 1
	def getMe(self):
		return self.me
	def addChild(self, child):
		self.children.append(child)
	def addHeat(self):
		self.heat = self.heat + 1
	def getHeat(self):
		return self.heat
	def getChildren(self):
		return self.children
	def __str__(self):
		return self.me + ": " + str(len(self.children)) + " children."

def route_append(existing, new):
	if existing.getMe() == new.getMe():
		existing.addHeat()
		#
		# In both of these first two cases,
		# we have "handled" the node, so
		# we return true.
		#

		#
		# We are out of new children, 
		# but we have a match. In other words,
		# this route is already in our tree.
		#
		if len(new.getChildren()) == 0:
			return True
		# We have no more existing children,
		# but we have more new children. In 
		# other words, a new route extends from
		# here so we'll append it.
		#
		if len(existing.getChildren()) == 0:
			existing.addChild(new.getChildren()[0])
			return True

		#
		# Walk the children of the existing node
		# and see if there is a child that can handle
		# our new node.
		#
		for e in existing.getChildren():
			if route_append(e, new.getChildren()[0]):
				return True
		#
		# There was no existing child node that
		# could handle this new node, so we are going
		# to add it here.
		#
		existing.addChild(new.getChildren()[0])
		return True
	# 
	# Since this node does not match the new node,
	# we cannot handle it. So, we return false.
	#
	return False

routes = []
for line in f:
	line = line.strip()
	components = line.split(",")
	hops = components[2].split("#")
	#hops = line.split("#")
	print("length of hops: " + str(len(hops)))
	hops.reverse()
	rn = hops_to_routenodes(hops)
	match = False
	for i in routes:
		if route_append(i, rn):
			match = True
	if match == False:
		routes.append(rn)
for i in routes:
	print_routenode(i,4)
