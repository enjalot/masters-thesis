
import pickle
import pylab

def ms2fps(ms):
    return 1000./ms

nf = open('nv_nums.pi', 'r')
tf = open('nv_timings.pi', 'r')
tfm = open('nv_mill_timings.pi', 'r')
atf = open('ati_timings.pi', 'r')
atfm = open('ati_mill_timings.pi', 'r')



nv_nums = pickle.load(nf)
nv_timings = pickle.load(tf)
nv_mill_timings = pickle.load(tfm)
ati_timings = pickle.load(atf)
ati_mill_timings = pickle.load(atfm)

print nv_nums
#print nv_timings

nv_rtps_fps = []
nv_mill_rtps_fps = []
ati_rtps_fps = []
ati_mill_rtps_fps = []


for ms in nv_timings["Update loop"]:
    nv_rtps_fps += [ms2fps(ms)]
for ms in nv_mill_timings["Update loop"]:
    nv_mill_rtps_fps += [ms2fps(ms)]
for ms in ati_timings["Update loop"]:
    ati_rtps_fps += [ms2fps(ms)]
for ms in ati_mill_timings["Update loop"]:
    ati_mill_rtps_fps += [ms2fps(ms)]


fps = False
nv_kernel = False 
nv_ati_neighbors = False 
nv_neighbors = True

if fps:
    krog_fps = [1424, 1084, 837, 429, 245, 140, 74]
    pylab.figure(0)
    pylab.plot(nv_nums, krog_fps, 'o-', label='SimpleSim on GTX480 max_num = num')
    pylab.plot(nv_nums, nv_rtps_fps, 'o-', label='RTPS on GTX480 max_num = num')
    pylab.plot(nv_nums, ati_rtps_fps, 'o-', label='RTPS on FireProV7800 max_num = num')

    pylab.axhline(30, linestyle='--', alpha=.5, label='30fps')
    pylab.axhline(60, linestyle='-.', alpha=.5, label='60fps')
    pylab.legend(loc='upper right')
    pylab.xlabel('Number of Particles')
    pylab.ylabel('Frames Per Second')


    pylab.figure(1)
    pylab.plot(nv_nums, krog_fps, 'o-', label='SimpleSim on GTX480 max_num = num')
    pylab.plot(nv_nums, nv_mill_rtps_fps, 'o-', label='RTPS on GTX480 max_num = 1million')
    pylab.plot(nv_nums, ati_mill_rtps_fps, 'o-', label='RTPS on FireProV7800 max_num = 1million')

    pylab.axhline(30, linestyle='--', alpha=.5, label='30fps')
    pylab.axhline(60, linestyle='-.', alpha=.5, label='60fps')
    pylab.legend(loc='upper right')
    pylab.xlabel('Number of Particles')
    pylab.ylabel('Frames Per Second')


if nv_kernel:
    pylab.figure(2)

    keys = [
        'Hash GPU kernel execution',
        'CellIndices GPU kernel execution',
        'Permute GPU kernel execution',
        'Bitonic Sort function',
        'Density GPU kernel execution',
        'Force GPU kernel execution',
        'Collision Wall GPU kernel execution',
        'Collision triangles function',
        'LeapFrog Integration GPU kernel execution',
    ]


    for key in keys:
        pylab.plot(nv_nums, nv_timings[key], 'o-', label=key)


    pylab.legend(loc='upper left')
    pylab.xlabel('Number of Particles')
    pylab.ylabel('Milliseconds')

if nv_neighbors:
    pylab.figure(3)

    keys = [
        'Bitonic Sort function',
        'Density GPU kernel execution',
        'Force GPU kernel execution',
    ]


    for key in keys:
        pylab.plot(nv_nums, nv_timings[key], 'o-', label='num ' + key)
        pylab.plot(nv_nums, nv_mill_timings[key], 's--', label='1million ' + key)


    pylab.legend(loc='upper left')
    pylab.xlabel('Number of Particles')
    pylab.ylabel('Milliseconds')


if nv_ati_neighbors:
    pylab.figure(4)

    keys = [
        'Bitonic Sort function',
        'Density GPU kernel execution',
        'Force GPU kernel execution',
    ]


    for key in keys:
        pylab.plot(nv_nums, nv_timings[key], 'o-', label='NVIDIA ' + key)
        pylab.plot(nv_nums, ati_timings[key], 's--', label='AMD' + key)


    pylab.legend(loc='upper left')
    pylab.xlabel('Number of Particles')
    pylab.ylabel('Milliseconds')





pylab.show()

"""
keys = [
        'Update loop',
        'Hash function',
        'Hash GPU kernel execution',
        'CellIndices function',
        'CellIndices GPU kernel execution',
        'Permute function',
        'Permute GPU kernel execution',
        'Bitonic Sort function',
        'Density function',
        'Density GPU kernel execution',
        'Force function',
        'Force GPU kernel execution',
        'Collision wall function',
        'Collision Wall GPU kernel execution',
        'Collision triangles function',
        'Integration function',
        'LeapFrog Integration GPU kernel execution',
        'Render call'
    ]
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
