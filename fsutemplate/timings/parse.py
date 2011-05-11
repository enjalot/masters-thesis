
import glob
import pylab



def get_timings(filename):
    num = int(filename.split('_')[-1])
    print num
    f = open(filename, 'r')

    timings = {}
    i = 0
    for line in f.readlines():
        if i < 4 or i > 21:
            i+=1
            continue
        la = line.split('|')
        mss = la[1].split(':')[1].strip()
        name = la[0].strip()
        #print la[0].strip(), float(mss)
        timings[name] = [float(mss)]
        i+=1 
    return num,timings


#filename = 'sph_timer_log_16384'
timings = {}
nums = []

files = glob.glob('sph_timer_log_*')
files = sorted(files)
print files

num, timings = get_timings(files[0])
nums += [num]

for filename in files[1:]:
    num, ts = get_timings(filename)
    for key in ts.keys():
        timings[key] += ts[key]
    nums += [num]

print nums
print timings

import pickle
nf = open('nums.pi', 'w')
tf = open('timings.pi', 'w')
pickle.dump(nums, nf)
pickle.dump(timings, tf)
nf.close()
tf.close()


"""

#RTPS
#32768 65536 131072 262144
#ms 10  14      21      47

#KROG
#4096 Avg ms/frame: 0.702116 Avg fps: 1424.27
#8192 Avg ms/frame: 0.9218 Avg fps: 1084.83
#16384 Avg ms/frame: 1.19416 Avg fps: 837.408
#32768 Avg ms/frame: 2.3278 Avg fps: 429.589
#65536 Avg ms/frame: 4.07494 Avg fps: 245.402
#131072 Avg ms/frame: 7.13558 Avg fps: 140.143
#262144 Avg ms/frame: 13.4817 Avg fps: 74.1744


rtps_fps = [500, 333 , 200, 100, 71, 47, 21]
krog_fps = [1424, 1084, 837, 429, 245, 140, 74]
fluids_cuda = [105, 64, 30]
fluids_cpu = [32, 15, 5]

num = [4096, 8192, 16384, 32768, 65536, 131072, 262144]
fluids_num = [4096, 8192, 16384]

#pylab.plot(mac_num, mac_v, 'o-', label='Viewport')
#pylab.plot(mac_num, mac_gl, 'o-', label='GL_POINTS')
#pylab.plot(mac_num, mac_glsl, 'o-', label='GLSL')

pylab.plot(num, rtps_fps, 'o-', label='RTPS with OpenCL')
pylab.plot(num, krog_fps, 'o-', label='SPHSim with CUDA')
pylab.plot(fluids_num, fluids_cuda, 'o-', label='FLUIDS with CUDA')
pylab.plot(fluids_num, fluids_cpu, 'o-', label='FLUIDS with CPU')

pylab.legend(loc='upper right')
pylab.xlabel('Number of Particles')
pylab.ylabel('Frames Per Second')
pylab.show()
"""
