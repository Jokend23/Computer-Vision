import cv2 as cv
import numpy as np


cap = cv.VideoCapture('video.mp4')

if not cap.isOpened():
	print('Can\'t open input video')
	exit()

img_size = [200, 360]
src = np.float32([
		[0, 200],
		[380, 200],
		[260, 160],
		[90, 160]
	])

src_draw = np.array(src, dtype=np.int32)

dst = np.float32([
		[0, img_size[0]],
		[img_size[1], img_size[0]],
		[img_size[1], 0],
		[0, 0]
	])

while cv.waitKey(1) != 27:
	ret, frame = cap.read()
	if not ret:
		print('End of video')
		break

	resized = cv.resize(frame, (img_size[1], img_size[0]))
	cv.imshow('frame', resized)

	r_channel = resized[:,:,2]
	binary = np.zeros_like(r_channel)
	binary[(r_channel > 200)] = 1

	hls = cv.cvtColor(resized, cv.COLOR_BGR2HLS)
	s_channel = resized[:,:,2]
	binary2 = np.zeros_like(s_channel)
	binary2[(s_channel > 130)] = 1

	allBinary = np.zeros_like(binary)
	allBinary[(binary==1)|(binary2==1)]=255
	# cv.imshow('binary', allBinary)

	allBinary_visual = allBinary.copy()

	cv.polylines(allBinary_visual, [src_draw], True, 255)
	cv.imshow('polygon', allBinary_visual)

	M = cv.getPerspectiveTransform(src, dst)
	warped = cv.warpPerspective(allBinary, M, (img_size[1], img_size[0]), flags=cv.INTER_LINEAR)
	# cv.imshow('warped', warped)

	histogram = np.sum(warped[warped.shape[0]//2:,:], axis=0)

	midpring = histogram.shape[0] // 2

	ind_whites_colum_L = np.argmax(histogram[:midpring])
	ind_whites_colum_R = np.argmax(histogram[midpring:]) + midpring
	warped_visual = warped.copy()
	cv.line(warped_visual, (ind_whites_colum_L, 0), (ind_whites_colum_L, warped_visual.shape[0]), 110, 2)
	cv.line(warped_visual, (ind_whites_colum_R, 0), (ind_whites_colum_R, warped_visual.shape[0]), 110, 2)
	# cv.imshow('warped colum', warped_visual)

	nWindow = 9
	Window_height = np.int(warped.shape[0]/nWindow)
	Window_half_width = 25

	XCenterLeftWindow = ind_whites_colum_L
	XCenterRightWindow = ind_whites_colum_R

	left_lane_inds = np.array([], dtype=np.int16)
	right_lane_inds = np.array([], dtype=np.int16)

	out_img = np.dstack((warped, warped, warped))

	nonzero = warped.nonzero()
	WhitePixelIndY = np.array(nonzero[0])
	WhitePixelIndX = np.array(nonzero[1])

	for window in range(nWindow):
		win_y1 = warped.shape[0] - (window + 1) * Window_height
		win_y2 = warped.shape[0] - (window) * Window_height

		left_win_x1 = XCenterLeftWindow - Window_half_width
		left_win_x2 = XCenterLeftWindow + Window_half_width

		right_win_x1 = XCenterRightWindow - Window_half_width
		right_win_x2 = XCenterRightWindow + Window_half_width

		cv.rectangle(out_img, (left_win_x1, win_y1), (left_win_x2, win_y2), (50 + window * 21, 0, 0), 2)
		cv.rectangle(out_img, (right_win_x1, win_y1), (right_win_x2, win_y2), (0, 0, 50 * window * 21), 2)
		# cv.imshow('window', out_img)

		good_left_inds = (
			(WhitePixelIndY > win_y1) & 
			(WhitePixelIndY <= win_y2) & 
			(WhitePixelIndX >= left_win_x1) & 
			(WhitePixelIndX <= left_win_x2)
		).nonzero()[0]

		good_right_inds = (
			(WhitePixelIndY > win_y1) & 
			(WhitePixelIndY <= win_y2) & 
			(WhitePixelIndX >= right_win_x1) & 
			(WhitePixelIndX <= right_win_x2)
		).nonzero()[0]

		left_lane_inds = np.concatenate((left_lane_inds, good_left_inds))
		right_lane_inds = np.concatenate((right_lane_inds, good_right_inds))

		if len(good_left_inds) > 50:
			XCenterLeftWindow = np.int(np.mean(WhitePixelIndX[good_left_inds]))
		if len(good_right_inds) > 50:
			XCenterRightWindow = np.int(np.mean(WhitePixelIndX[good_right_inds]))

	out_img[WhitePixelIndY[left_lane_inds], WhitePixelIndX[left_lane_inds]] = [255, 0, 0]
	out_img[WhitePixelIndY[right_lane_inds], WhitePixelIndX[right_lane_inds]] = [0, 0, 255]

	# cv.imshow('Lane', out_img)

	leftx = WhitePixelIndX[left_lane_inds]
	lefty = WhitePixelIndY[left_lane_inds]

	rightx = WhitePixelIndX[right_lane_inds]
	righty = WhitePixelIndY[right_lane_inds]
	try:
		left_fir=np.polyfit(lefty, leftx, 2)
		right_fit=np.polyfit(righty, rightx, 2)
	except TypeError:
		continue

	center_fit = (left_fir + right_fit / 2)

	for ver_ind in range(out_img.shape[0]):
		gor_ind = (
			center_fit[0] * (ver_ind ** 2) +
			center_fit[1] * ver_ind + 
			center_fit[2]
		)
		cv.circle(out_img, (int(gor_ind), int(ver_ind)), 2, (255, 0, 255), 1)
	cv.imshow('center', out_img)