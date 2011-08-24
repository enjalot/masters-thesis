
import pickle
import pylab

from pylab import arange,pi,sin,cos,sqrt
fig_width_pt = 1200 # Get this from LaTeX using \showthe\columnwidth
inches_per_pt = 1.0/72.27               # Convert pt to inch
golden_mean = (sqrt(5)-1.0)/2.0         # Aesthetic ratio
fig_width = fig_width_pt*inches_per_pt  # width in inches
fig_height = fig_width*golden_mean      # height in inches
fig_size =  [fig_width,fig_height]
params = {'backend': 'WXAgg',
          'axes.labelsize': 20,
          'text.fontsize': 20,
          'legend.fontsize': 20,
          'xtick.labelsize': 20,
          'ytick.labelsize': 20,
          #'text.usetex': True,
          'figure.figsize': fig_size}
pylab.rcParams.update(params)



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


fps = True 
nv_kernel = False#True 
nv_ati_neighbors = False 
nv_neighbors = False 


#num_ticks = [16384, 32768, 65536, 131072, 262144]
num_ticks = [32768, 65536, 131072, 262144]

if fps:
    fps_ticks = [30, 60, 100, 200, 400, 1000]
    krog_fps = [1424, 1084, 837, 429, 245, 140, 74]
    fig = pylab.figure(0)
    print nv_rtps_fps
    pylab.plot(nv_nums[2:], krog_fps[2:], 'H-', linewidth=4, markersize=10, label='SimpleSPH on GTX480 max_num = num')
    pylab.plot(nv_nums[2:], nv_rtps_fps[2:], '^-', linewidth=4, markersize=10, label='RTPS on GTX480 max_num = num')
    pylab.plot(nv_nums[2:], ati_rtps_fps[2:], 'o-', linewidth=4, markersize=10, label='RTPS on FireProV7800 max_num = num')

    pylab.axhline(30, linestyle='--', alpha=.5, label='30fps')
    pylab.axhline(60, linestyle='-.', alpha=.5, label='60fps')

    

    pylab.legend(loc='upper right')
    pylab.xlabel('Number of Particles')
    pylab.ylabel('Frames Per Second')
    pylab.xticks(num_ticks, num_ticks)
    pylab.yticks(fps_ticks, fps_ticks)

    #fig


    pylab.figure(1)
    pylab.plot(nv_nums[2:], krog_fps[2:], 'H-', linewidth=4, markersize=10, label='SimpleSPH on GTX480 max_num = num')
    pylab.plot(nv_nums[2:], nv_mill_rtps_fps[2:], '^-', linewidth=4, markersize=10, label='RTPS on GTX480 max_num = 1million')
    pylab.plot(nv_nums[2:], ati_mill_rtps_fps[2:], 'o-', linewidth=4, markersize=10, label='RTPS on FireProV7800 max_num = 1million')

    pylab.axhline(30, linestyle='--', alpha=.5, label='30fps')
    pylab.axhline(60, linestyle='-.', alpha=.5, label='60fps')
    pylab.legend(loc='upper right')
    pylab.xlabel('Number of Particles')
    pylab.ylabel('Frames Per Second')
    pylab.xticks(num_ticks, num_ticks)
    pylab.yticks(fps_ticks, fps_ticks)


if nv_kernel:
    pylab.figure(2)

    keys = [
        'Hash GPU kernel execution',
        'CellIndices GPU kernel execution',
        'Permute GPU kernel execution',
        'Collision Wall GPU kernel execution',
        'Collision triangles function',
        'LeapFrog Integration GPU kernel execution',
        'Bitonic Sort function',
        'Density GPU kernel execution',
        'Force GPU kernel execution',
    ]
    colors = [
            '.25',
            '.5',
            '.75',
            'm',
            'c',
            'y',
            'b',
            'g',
            'r',
    ]
    markers = [
            'o',
            'o',
            'o',
            'o',
            'o',
            'o',
            '^',
            'D',
            'H',
    ]


    bot = nv_timings[keys[0]]
    width = 10000
    for i,key in enumerate(keys):
        """
        if i == 0:
            pylab.bar(nv_nums[2:], nv_timings[key][2:], width, color=colors[i], label=key)
        else:
            pylab.bar(nv_nums[2:], nv_timings[key][2:], width, bottom=bot[2:], color=colors[i], label=key)
            #each bar needs to start at the cumulative bottom of the last
            for j,x in enumerate(bot):
                bot[j] += nv_timings[key][j]
                
        """
        pylab.plot(nv_nums, nv_timings[key], 'o-', linewidth=4.0, markersize=10, color=colors[i], marker=markers[i], label=key)


    pylab.legend(loc='upper left')
    pylab.xlabel('Number of Particles')
    pylab.ylabel('Milliseconds')
    import numpy
    pylab.xticks(num_ticks, num_ticks)
    #num_ticks = numpy.array(num_ticks)
    #pylab.xticks(num_ticks + width / 2., num_ticks)

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

    keys = [
        'Bitonic Sort function',
        'Density GPU kernel execution',
        'Force GPU kernel execution',
    ]

    nv_pie = []
    ati_pie = []
    for key in keys:
        nv_pie += [ nv_timings[key][-1] ]
        ati_pie += [ ati_timings[key][-1] ]



    
    fig = pylab.figure(4)#, figsize=(8,12))
    #ax = pylab.axes([0.1, 0.1, 0.8, 0.8])
    bigAxes = pylab.axes(frameon=False)     # hide frame
    pylab.xticks([])                        # don't want to see any ticks on this axis
    pylab.yticks([])
    pylab.subplots_adjust(bottom=.1, left=.4, right=.6, top=.94, hspace=.5)

    nvp = fig.add_subplot(2,1,1)
    atip = fig.add_subplot(2, 1, 2)#, sharex=nvp, sharey=nvp)

    #pylab.pie(nv_pie, labels=keys, autopct='%1.1f%%', shadow=False)
    #pylab.pie(nv_pie, labels=keys, autopct='%1.1f%%', shadow=False)
    nvp.pie(nv_pie, labels=keys, autopct='%1.1f%%', shadow=False, colors=['c','g','r'])
    #pylab.title('NVIDIA', bbox={'facecolor':'0.8', 'pad':5})
    nvp.text(-.5, -1.6, "NVIDIA", fontsize="30")

    #pylab.figure(5, figsize=(6,6))
    #ax = pylab.axes([0.1, 0.1, 0.8, 0.8])
    #pylab.pie(ati_pie, labels=keys, autopct='%1.1f%%', shadow=False)
    #pylab.pie(ati_pie, labels=keys, autopct='%1.1f%%', shadow=False)
    atip.pie(ati_pie, labels=keys, autopct='%1.1f%%', shadow=False, colors=['c','g','r'])
    #atip.title('ATI', bbox={'facecolor':'0.8', 'pad':5})
    atip.text(-.3, -1.6, "ATI", fontsize="30")
    #pylab.pie(ati_timings, labels='AMD')
        
    #atip.legend(loc="lower center")

    #for key in keys:
        #pylab.plot(nv_nums, nv_timings[key], 'o-', label='NVIDIA ' + key)
        #pylab.plot(nv_nums, ati_timings[key], 's--', label='AMD' + key)




    #pylab.legend(loc='upper left')
    #pylab.xlabel('Number of Particles')
    #pylab.ylabel('Milliseconds')





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
