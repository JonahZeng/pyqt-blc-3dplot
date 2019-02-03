# _*_ encoding=utf-8 _*_
import numpy as np
from scipy.signal import savgol_filter
from scipy.ndimage import uniform_filter,  zoom

def handle(rawNames,  bayer,  width,  height,  bitDepth):
    assert isinstance(rawNames,  str) or isinstance(rawNames,  list)
    assert isinstance(bayer,  str)
    assert isinstance(width,  int)
    assert isinstance(height,  int)
    raw_sum = np.zeros((height,  width), dtype=np.float)#raw多帧叠加结果
    for raw in rawNames:
        data = np.fromfile(raw,  np.uint16).reshape(height,  width)
        raw_sum = raw_sum + data
    raw_mean = raw_sum/len(rawNames)
    if bayer == "BG":
        raw_b = raw_mean[0::2, 0::2]#分解4个通道
        raw_gb = raw_mean[0::2, 1::2]
        raw_gr = raw_mean[1::2, 0::2]
        raw_r = raw_mean[1::2, 1::2]
    elif bayer == "RG":
        raw_r = raw_mean[0::2, 0::2]#分解4个通道
        raw_gr = raw_mean[0::2, 1::2]
        raw_gb = raw_mean[1::2, 0::2]
        raw_b = raw_mean[1::2, 1::2]
    elif bayer == "GB":
        raw_gb = raw_mean[0::2, 0::2]#分解4个通道
        raw_b = raw_mean[0::2, 1::2]
        raw_r = raw_mean[1::2, 0::2]
        raw_gr = raw_mean[1::2, 1::2]
    elif bayer == "GR":
        raw_gr = raw_mean[0::2, 0::2]#分解4个通道
        raw_r = raw_mean[0::2, 1::2]
        raw_b = raw_mean[1::2, 0::2]
        raw_gb = raw_mean[1::2, 1::2]
    else:
        return None
    mean_raw_r = uniform_filter(raw_r, 11)#单通道11*11平均
    mean_raw_gr = uniform_filter(raw_gr, 11)
    mean_raw_gb = uniform_filter(raw_gb, 11)
    mean_raw_b = uniform_filter(raw_b, 11)
    mean_raw_r = zoom(mean_raw_r, 1/16, mode='nearest')#单通道缩放1/16
    mean_raw_gr = zoom(mean_raw_gr, 1/16, mode='nearest')
    mean_raw_gb = zoom(mean_raw_gb, 1/16, mode='nearest')
    mean_raw_b = zoom(mean_raw_b, 1/16, mode='nearest')
    win_length = width//(16*8)
    win_length = ((win_length>>1)<<1) + 1
    win_height = height//(16*8)
    win_height = ((win_height>>1)<<1) + 1
    mean_raw_r = savgol_filter(mean_raw_r, win_length, 2,  axis=1)#x方向2次拟合,窗宽
    mean_raw_gr = savgol_filter(mean_raw_gr, win_length, 2,  axis=1)
    mean_raw_gb = savgol_filter(mean_raw_gb, win_length, 2,  axis=1)
    mean_raw_b = savgol_filter(mean_raw_b, win_length, 2,  axis=1)
    mean_raw_r = savgol_filter(mean_raw_r, win_height, 2,  axis=0)#y方向2次拟合,窗宽
    mean_raw_gr = savgol_filter(mean_raw_gr, win_height, 2,  axis=0)
    mean_raw_gb = savgol_filter(mean_raw_gb, win_height, 2,  axis=0)
    mean_raw_b = savgol_filter(mean_raw_b, win_height, 2,  axis=0)
    return (mean_raw_r,  mean_raw_gr, mean_raw_gb,  mean_raw_b)
