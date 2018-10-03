import freenect, time
from numpy import *


def getDepthMap():
	depth, timestamp = freenect.sync_get_depth()
	return depth

while 1:
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
			print("turn R")
		elif int(shadowR) < int(shadowL):
			print("turn L")
		else:
			print("turn L")
	else:
		print("go")
	time.sleep(1)
