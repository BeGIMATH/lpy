from openalea.plantgl.all import *

def import_contours(fn):
    f = open(fn,'r')
    # read header of the file
    f.readline()
    nbitems = int(f.readline().split()[1])
    result = []
    for i in xrange(nbitems):
       f.readline()
       name = f.readline().split()[1]
       nbpoints = int(f.readline().split()[1])
       typecurve = f.readline().split()[1]
       samples = None
       if typecurve == 'or':
         samples = int(f.readline().split()[1])
       points = []
       for j in xrange(nbpoints):
           coord = map(float,f.readline().split())
           point = Vector4(coord[:3]+[1])
           for k in xrange(int(coord[3])):
               points.append(point) 
       if sum([p.z for p in points]) > 0:
            n = NurbsCurve(points)
       else:
            n = NurbsCurve2D([(p.x,p.y,p.w) for p in points])        
       if samples != None:
            n.stride = samples
       n.name = name
       result.append(n)
    return result

def import_functions(fn):
    f = open(fn,'r')
    # read header of the file
    f.readline() # funcgalleryver 1 1
    nbitems = int(f.readline().split()[1]) # items: 10
    result = []
    for i in xrange(nbitems):
       f.readline() # fver 1 1
       name = f.readline().split()[1] # name: BR_LEN_0
       samples = int(f.readline().split()[1]) # samples: 5
       f.readline() # flip: off
       nbpoints = int(f.readline().split()[1]) # points: 4
       points = []
       for j in xrange(nbpoints):
           coord = map(float,f.readline().split()) # 0.000000 0.577929
           point = Vector3(coord+[1])
           points.append(point) 
       n = NurbsCurve2D(points)        
       if samples != None:
            n.stride = samples
       n.name = name
       result.append(n)
    return result

def import_patch(fn):
    f = open(fn,'r')
    # read header of the file
    f.readline()
    v = f.readline().split()
    contact = Vector3(float(v[3]),float(v[5]),float(v[7]))
    f.readline()
    v = f.readline().split()
    heading = Vector3(float(v[2]),float(v[4]),float(v[6]))
    l = heading.normalize()
    v = f.readline().split()
    up = Vector3(float(v[2]),float(v[4]),float(v[6]))
    up.normalize()
    v = f.readline().split()
    size = float(v[1])
    name = f.readline().split()[0]
    for i in xrange(4): f.readline()
    ctrlpoints = []
    left = heading^up
    m = Matrix3(-up,-left,heading)
    m = m.inverse()
    for i in xrange(4):
        v = f.readline().split()
        row = []
        for j in range(4):
            p = Vector3(float(v[j*3]),float(v[j*3+1]),float(v[j*3+2]))
            p -= contact
            p = m*p
            row.append(Vector4(p,1))
        ctrlpoints.append(row)    
    smb = BezierPatch(ctrlpoints)
    actualdim = 2*max(BoundingBox(smb).getSize())
    smb = BezierPatch([[Vector4(i.project()/actualdim,1) for i in ctrllines] for ctrllines in ctrlpoints])
    smb.name = name
    return smb

def import_colormap(fn):
    import array
    a = array.array('B')
    a.fromfile(open(fn,'rb'),256*3)
    return [Material('Color_'+str(i),Color3(a[3*i],a[3*i+1],a[3*i+2])) for i in xrange(256)]

def import_materialmap(fn):
    import array
    stream = open(fn,'rb')
    result = []
    while True:
        a = array.array('B')
        try:
            a.fromfile(stream,15)
        except Exception,e:
            break
        valiter = iter(a)
        id = valiter.next()
        transparency = valiter.next()
        ambient = (valiter.next(),valiter.next(),valiter.next())
        diffuse = (valiter.next(),valiter.next(),valiter.next())
        emission = Color3(valiter.next(),valiter.next(),valiter.next())
        specular = Color3(valiter.next(),valiter.next(),valiter.next())
        shininess = valiter.next()
        sdiffuse = sum(diffuse)
        sambient = sum(ambient)
        if sdiffuse > 0 and sambient > 0:
            ambient_ratio = sambient/float(sdiffuse)
            m = Material('Color_'+str(id),Color3(*(int(i * ambient_ratio) for i in diffuse)),1./ambient_ratio,specular,emission,shininess,transparency)
        else:
            m = Material('Color_'+str(id),Color3(*ambient),0,specular,emission,shininess,transparency)
            
        result.append(m)
    return result