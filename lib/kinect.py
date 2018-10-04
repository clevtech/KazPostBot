import freenect, time
from numpy import *


def getDepthMap():
	while 1:
		try:
			depth, timestamp = freenect.sync_get_depth()
			break
		except:
			pass
	return depth

def motion():
	depth = array(getDepthMap())
	left = depth[0:220, [range(10, 200)]]
	center = depth[0:220, [range(201, 429)]]
	right = depth[0:220, [range(430, 630)]]
	shadowL = int(amin(left)/100)
	shadowC = int(amin(center)/100)
	shadowR = int(amin(right)/100)
	shadow = [shadowL, shadowC, shadowR]
	print(shadow)
	if amin(shadow) <= 8:
		if int(shadowL) < int(shadowR):
			return("R")
		elif int(shadowR) < int(shadowL):
			return("L")
		elif amin(shadow) <= 4:
			return("S")
		else:
			return("S")
	else:
		return("G")
