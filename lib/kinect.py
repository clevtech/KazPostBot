import freenect, time
from numpy import *


def getDepthMap():
	while 1:
		try:
			depth, timestamp = freenect.sync_get_depth()
			break
		except:
			time.sleep(10)
			pass
	return depth

def motion():
	print("Getting freenect values")
	depth = array(getDepthMap())
	print("Depth map is given")
	left = depth[0:220, [range(10, 200)]]
	center = depth[0:220, [range(201, 429)]]
	right = depth[0:220, [range(430, 630)]]
	shadowL = int(amin(left)/100)
	shadowC = int(amin(center)/100)
	shadowR = int(amin(right)/100)
	shadow = [shadowL, shadowC, shadowR]
	print("Shadow values are: " + str(shadow))
	if amin(shadow) <= 8:
		if int(shadowL) < int(shadowR):
			print("Something in left")
			return("R")
		elif int(shadowR) < int(shadowL):
			print("Something in right")
			return("L")
		elif amin(shadow) <= 4:
			print("Something in very close")
			return("S")
		else:
			print("Something in middle")
			return("S")
	else:
		print("Continue movement")
		return("G")
