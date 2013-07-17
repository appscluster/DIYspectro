import cv2
import numpy as np
import pylab as pl

def take_measurement(cam, res_y, res_x, channels, time):
	res0 = np.zeros((res_y, res_x, channels, time))

	c = cv2.VideoCapture(cam)

	for i in range(time):
	    res0[:,:,:,i] = c.read()[1]

	c.release()

	# sum over RGB channels
	res1 = res0.sum(axis=2)

	# average over time
	res2 = res1.mean(axis=2)

	return res0, res1, res2

##############################################

cam = 0 # 0: intern, 1: USB webcam

time = 100
res_x = 640
res_y = 480
channels = 3

x_start = 50
x_stop = 370

y_center = 230
y_range = 20

# trigger measurement
res0, res1, res2 = take_measurement(cam, res_y, res_x, channels, time)

# figs and plots
pl.figure()
pl.imshow(res1[:,:,0])
pl.title('t = 0')
pl.show()

pl.figure()
pl.imshow(res2)
pl.title('Averaged over %i frames' % time)
pl.show()

res1_1 = res1[y_center, x_start:x_stop, 0]
res2_1 = res2[y_center, x_start:x_stop]
res2_2 = res2[y_center - y_range:y_center + y_range, x_start:x_stop].mean(axis=0)

pl.figure()
pl.plot(res1_1, label = 't=0, y = #%i' % y_center)
pl.plot(res2_1, label = 'y = #%i' % y_center)
pl.plot(res2_2, label = 'y = mean(#%i - #%i)' % (y_center - y_range, y_center + y_range))
pl.legend(loc=0)
pl.grid()
pl.title('Spectrum w/ and w/o Average over %i Frames' % time)
pl.show()

pl.figure()
pl.plot(res2_2 - res1_1, label = 't=0, y = #%i' % y_center)
pl.plot(res2_2 - res2_1, label = 'y = #%i' % y_center)
pl.legend(loc=0)
pl.grid()
pl.title('Difference Spectra to %i-frame Average' % time)
pl.show()

pl.figure()
pl.plot((res2_2 - res1_1) / res2_2, label = 't=0, y = #%i' % y_center)
pl.plot((res2_2 - res2_1) / res2_2, label = 'y = #%i' % y_center)
pl.legend(loc=0)
pl.grid()
pl.title('Relative Difference Spectra to %i-frame Average' % time)
pl.show()