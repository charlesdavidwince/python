import glob
import subprocess
import os.path

# do it at last words

ABSPATH = "/usr/local/lib/"  # absolute path to relative libraries
# libraries to correct
LIBPATHS = ['/usr/local/lib/python2.7/site-packages/cv2.so', '/usr/local/lib/libopencv*'] 

PREFIX = 'sudo install_name_tool -change '

assert(ABSPATH.startswith('/') and ABSPATH.endswith('/'), 
    'please provide absolute library path ending with /'

libs = []
for path in LIBPATHS:
  libs += glob.glob(path)

cmd =  []
err = []
for lib in libs:
  if not os.path.isfile(lib):
    err.append(lib+" library not found") # glob should take care
  datastr = subprocess.check_output(['otool','-l','-v', lib])
  data = datastr.split('\n') 
  for line in data:
    ll = line.split()
    if not ll: continue
    if (ll[0] == 'name' and ll[1].endswith('.dylib') and not ll[1].startswith('/')):
      libname = ll[1].split('/')[-1]
      if os.path.isfile(ABSPATH+libname):  
        cmd.append(PREFIX+ll[1]+" "+ABSPATH+libname+' '+lib)
      else:
        err.append(ABSPATH+libname+" does not exist, hence can't correct: "+ll[1]+" in: "+lib)

ohandle = open("rpathChangeCmd.txt", 'w')
for lib in cmd:
  ohandle.write(lib+'\n')
ohandle.close()

if err:
  ehandle = open("rpathChangeErr.txt", 'w')
  for e in err:
    ehandle.write(e+'\n')
  ehandle.close()