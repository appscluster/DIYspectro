import cv2
import numpy as np
import pylab as pl

'''
Reads out open-source spectrometers, e.g. developed by 'http://spectralworkbench.org/'. Reads webcam stream for a given number of frames and averages over a few lines in the picture, as well as time. 
'''

def take_measurement(cam, res_x, res_y, channels, time):
	'''
	input: 
	cam: 0: intern, 1: USB webcam 
	res_x: resolution in x-direction, [px]
	res_y: resolution in y-direction, [px]
	channels: number of channels, e.g. 3 for RGB
	time: number of frames to average over

	output:
	res0: complete data array, [res_y, res_x, channels, time]
	res1: averaged over channels, [res_y, res_x, time]
	res2: averaged over channels and time, [res_y, res_x]
	'''

	# empty result array
	res0 = np.zeros((res_y, res_x, channels, time))

	# open webcam stream
	c = cv2.VideoCapture(cam)

	# set resolutions
	c.set(3, res_x)
	c.set(4, res_y)

	# write stream to array
	for i in range(time):
	    res0[:,:,:,i] = c.read()[1]

	# close webcam stream
	c.release()

	# sum over RGB channels
	res1 = res0.sum(axis=2)

	# average over time
	res2 = res1.mean(axis=2)

	return res0, res1, res2

##############################################

cam = 0 # 0: intern, 1: USB webcam

time = 100
res_x = 1280
res_y = 720
channels = 3 # RGB

# choose which parts of the image are evaluated
x_start = 0
x_stop = res_x

y_center = res_y/2
y_range = 25

##############################################

# trigger measurement
res0, res1, res2 = take_measurement(cam, res_x, res_y, channels, time)

# figs and plots
pl.figure(figsize=(10,4))
pl.subplot(211)
pl.imshow(res1[y_center - y_range:y_center + y_range, x_start:x_stop, 0])
pl.title('One Frame')

pl.subplot(212)
pl.imshow(res2[y_center - y_range:y_center + y_range, x_start:x_stop])
pl.title('Averaged over %i frames' % time)

pl.tight_layout()
pl.show()


res1_1 = res1[y_center, x_start:x_stop, time/2]
res2_1 = res2[y_center, x_start:x_stop]
res2_2 = res2[y_center - y_range:y_center + y_range, x_start:x_stop].mean(axis=0)

pl.figure()
pl.plot(res1_1, label = 'One Row')
pl.plot(res2_1, label = 'Time Average, One Row')
pl.plot(res2_2, label = 'Time Average, %i Rows' % (y_range*2))
pl.legend(loc=0)
pl.grid()
pl.title('Spectrum Enhancement. Averages over %i Frames' % time)
pl.show()

'''
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
'''