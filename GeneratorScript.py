import c4d
import math as m

def currentfunc(x,y,tx,ty,func):
    out = 0
    code = """
from math import *
from random import *
x = {k}
y = {l}
output = {parsingstring}
    """.format(k=x+tx,l=y+ty,parsingstring = func)
    exec(code,globals())
    return output

def TextureScaler(op,a):
    thetag = op.GetTag(c4d.Ttexture)
    thetag[c4d.TEXTURETAG_PROJECTION] = 2
    thetag[c4d.TEXTURETAG_SEAMLESS] = True

    thetag[c4d.TEXTURETAG_SIZE,c4d.VECTOR_Y] = a
    thetag[c4d.TEXTURETAG_POSITION,c4d.VECTOR_Y] =  a


def main():

    thisobj = doc.SearchObject("mafgrapher")
    try:
        textag = thisobj.GetTag(c4d.TextureTag)
    except:
        pass
    #stuff to read from Userdata 
    
    l = thisobj[c4d.ID_USERDATA,2]
    h = thisobj[c4d.ID_USERDATA,3]
    A = thisobj[c4d.ID_USERDATA,5]
    func = thisobj[c4d.ID_USERDATA,8]
    maxval = A
    #frame nu
    frameno = 0
    scalefactor = thisobj[c4d.ID_USERDATA,6]
    phase = 0

    panx = thisobj[c4d.ID_USERDATA,13]
    pany = thisobj[c4d.ID_USERDATA,14]

    lSegments = int(thisobj[c4d.ID_USERDATA,10])
    hSegments = int(thisobj[c4d.ID_USERDATA,11])



    #point spacing
    lSpace = l /(lSegments - 1)
    hSpace = h /(hSegments - 1)

    #midpoint
    lhalfSegment = lSegments * 0.5
    points = []


    for z in xrange(hSegments):
        for x in xrange (lSegments):
            p = c4d.Vector(0.0)
            p.x = lSpace * ( x)
            p.z = hSpace * z
            try:
                p.y = A*currentfunc(p.x*scalefactor,p.z*scalefactor,panx,pany,func) #point position setting shit happens here
                if(p.y > maxval):
                    maxval = p.y
                else:
                    pass
            except:
                p.y = 1/A


            points.append(p)


    pol = c4d.BaseObject(c4d.Opolygon)
    ptCnt = lSegments * hSegments
    polyCnt =  (lSegments - 1 )* (hSegments - 1)

    #tag material stretching
    try:
        TextureScaler(thisobj,maxval/1.9)
    except:
        pass


    pol.ResizeObject(ptCnt, polyCnt)
    pol.SetAllPoints(points)
    polyIndex = 0
    for x in xrange(lSegments - 1):
        for y in xrange (hSegments - 1):
            xmove = x + y * lSegments
            ymove =  x + y * lSegments + lSegments
            cpol = c4d.CPolygon( xmove ,ymove ,ymove + 1 ,xmove + 1 )
            pol.SetPolygon(polyIndex , cpol)
            polyIndex += 1
    # Updates the polygon object
    pol.Message(c4d.MSG_UPDATE)



    # Done
    return pol
