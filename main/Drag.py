import level1

def Drag(density, velocity, dragCoeff, Area):
	# F = force due to drag
	p = density
	v = velocity
	c = dragCoeff
	A = Area
	if v>0:
		F = 0.5*p*(v**2)*c*A
	elif v<0:
		F = -0.5*p*(v**2)*c*A
	else:
		F=0
	return F
