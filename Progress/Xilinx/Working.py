#********************************************************************************
# + Prerequisite:
#   - ModelDesk Traffic project must be opened
#   - MotionDesk Traffic project must be opened
#
# + This script generate automatically for following sensor model:
#   Sensor3D Pyramid, Sensor3D IceCone and Sensor2D flat IceCone
#
# + This script read the sensor parameters from ModelDesk and generated
#   3d model for MotionDesk as customer objects.
#
# + Per default the generated object is attached to the chassis and all translational
#   and rotational offset of the sensor is considered during generation.
#
# + It could be necessary to do some manually adaption to the new added movable objects
#   in MotionDesk:
#   - connect to motion data "chassis"
#   - change the render mode to "transparent"
#   - change the transparency value to "70%"
#
# + After changing any parameter of any sensor (3d or 2d) in ModelDesk,
#   please start the python script again to synchronize with MotionDesk (movable objects)
#
# + The generated sensor name is numerated as following:
#   - for Sensor3D:     Sensor3D_01,    Sensor3D_02,    ...
#   - for Sensor2D:     Sensor2D_01,    Sensor2D_02,    ...
#   - for Sensor2DGeo:  Sensor2DGeo_01, Sensor2DGeo_03, ...
#
# Copyright (c) 2017 - 2020 by dSPACE GmbH, GERMANY
#
#********************************************************************************
from collections    import namedtuple
import os
import sys
import numpy
import math
import traceback
import tempfile
import time

#--------------------------------------------------------------------------------
# To start a new python process to run a script, please see the following sample:
#--------------------------------------------------------------------------------
# import subprocess
# import sys
# subprocess.Popen(["start", sys.executable, "blabla.py"])
#--------------------------------------------------------------------------------

ElementTypes = namedtuple('ElementTypes', 'dSPACE Customer')
elemTypes = ElementTypes(dSPACE=0, Customer=1)


#********************************************************************************
class Effect:
    def __init__(self, id, diffuse, ambient, transparency):
        self.id = id
        self.name = id
        if len(diffuse) == 3:
            self.diffuse = (diffuse[0], diffuse[1], diffuse[2], 1.0)
        else:
            self.diffuse = diffuse
        self.ambient = ambient
        self.transparency = transparency

    def write(self, fid, nTab=0):
        fid.write('{0}<effect id="{1}" name="{2}">\n'.format('\t'*nTab, self.id, self.name))
        nTab = nTab + 1
        fid.write('{0}<profile_COMMON> <technique sid="common"> <phong>\n'.format('\t'*nTab))

        fid.write('{0}<diffuse> <color>{1} {2} {3} {4}</color> </diffuse>\n'.format('\t'*nTab, self.diffuse[0], self.diffuse[1], self.diffuse[2], self.diffuse[3]))
        fid.write('{0}<ambient> <color>{1} {2} {3} {4}</color> </ambient>\n'.format('\t'*nTab, self.ambient[0], self.ambient[1], self.ambient[2], self.ambient[3]))
        fid.write('{0}<transparency> <float>{1}</float> </transparency>\n'.format('\t'*nTab, self.transparency))

        fid.write('{0}</phong> </technique>\n'.format('\t'*nTab))
        fid.write('{0}<extra> <technique profile="GOOGLEEARTH"> <double_sided>0</double_sided> </technique> </extra>\n'.format('\t'*nTab))
        fid.write('{0}</profile_COMMON>\n'.format('\t'*nTab))
        nTab = nTab - 1
        fid.write('{0}</effect>\n'.format('\t'*nTab))


#********************************************************************************
class Material:
    def __init__(self, id, name, effect):
        self.id = id
        self.name = name
        self.effect = effect

    def write(self, fid, nTab=0):
        fid.write('{0}<material id="{1}" name="{2}">\n'.format('\t'*nTab, self.id, self.name))
        nTab = nTab + 1
        fid.write('{0}<instance_effect url="#{1}" />\n'.format('\t'*nTab, self.effect.name))
        nTab = nTab - 1
        fid.write('{0}</material>\n'.format('\t'*nTab))

#********************************************************************************
class FloatSource:
    def __init__(self, id, array_list, stride):
        self.id = id
        self.stride = stride
        self.nArray = len(array_list)
        self.count = self.nArray // len(stride)
        self.data = numpy.reshape(numpy.array(array_list), (self.count, len(stride)))

    def __len__(self):
        return len(self.data)

    def write(self, fid, nTab=0):
        fid.write('{0}<source id="{1}">\n'.format('\t'*nTab, self.id))
        nTab = nTab + 1
        fid.write('{0}<float_array count="{1}" id="{2}-array">\n'.format('\t'*nTab, self.nArray, self.id))
        for v in self.data.flatten():
            fid.write('{0} '.format(v))
        fid.write('\n{0}</float_array>\n'.format('\t'*nTab))
        
        fid.write('{0}<technique_common>\n'.format('\t'*nTab))
        fid.write('{0}<accessor count="{1}" source="#{2}-array" stride="{3}">\n'.format('\t'*nTab, self.count, self.id, len(self.stride)))
        for comp in self.stride:
            fid.write('{0}<param name="{1}" type="float" />\n'.format('\t'*(nTab+1), comp))
        fid.write('{0}</accessor>\n'.format('\t'*nTab))
        fid.write('{0}</technique_common>\n'.format('\t'*nTab))
        nTab = nTab - 1
        fid.write('{0}</source>\n'.format('\t'*nTab))


#********************************************************************************
class InputList:
    def __init__(self):
        self.inputList = []
        pass

    def addInput(self, offset, semantic, source):
        InputListTypes = namedtuple('InputListTypes', 'Offset Semantic Source')
        self.inputList.append(InputListTypes(Offset = offset, Semantic = semantic, Source = source))

#********************************************************************************
class TriangleSet:
    def __init__(self, indices_list, inputList, material):
        self.indices = numpy.array(indices_list)
        self.inputList = inputList
        self.material = material

    def write(self, fid, nTab=0):
        fid.write('{0}<triangles count="{1}" material="{2}">\n'.format('\t'*nTab, len(self.indices)/6, self.material))
        for input in self.inputList.inputList:
            addSource = ''
            if input.Semantic == 'VERTEX':
                addSource = '-vertices'
            fid.write('{0}<input offset="{1}" semantic="{2}" source="{3}{4}" />\n'.format('\t'*nTab, input.Offset, input.Semantic, input.Source, addSource))
        fid.write('{0}<p>\n'.format('\t'*nTab))
        for v in self.indices:
            fid.write('{0} '.format(v))
        fid.write('\n{0}</p>\n'.format('\t'*nTab))
        fid.write('{0}</triangles>\n'.format('\t'*nTab))


#********************************************************************************
class Geometry:
    def __init__(self, id, name, vertex, normal=None):
        self.id = id
        self.name = name
        self.vertex = vertex # FloatSource
        self.normal = normal # FloatSource
        self.primitives = []

    def createTriangleSet(self, indices_list, input_list, material):
        triSet = TriangleSet(indices_list, input_list, material)
        return triSet

    def write(self, fid, nTab=0):
        fid.write('{0}<geometry id="{1}" name="{2}"> <mesh>\n'.format('\t'*nTab, self.id, self.name))
        nTab = nTab + 1
        self.vertex.write(fid, nTab)
        if self.normal != None:
            self.normal.write(fid, nTab)
        fid.write('{0}<vertices id="{1}-vertices">\n'.format('\t'*nTab, self.vertex.id))
        fid.write('\t{0}<input semantic="POSITION" source="#{1}" />\n'.format('\t'*nTab, self.vertex.id))
        fid.write('{0}</vertices>\n'.format('\t'*nTab))
        for prim in self.primitives:
            prim.write(fid, nTab)
        nTab = nTab - 1
        fid.write('{0}</mesh> </geometry>\n'.format('\t'*nTab))


#********************************************************************************
class MaterialNode:
    def __init__(self, material_symbol, material):
        self.material_symbol = material_symbol
        self.material = material

    def write(self, fid, nTab=0):
        fid.write('{0}<bind_material> <technique_common>\n'.format('\t'*nTab))
        fid.write('{0}\t<instance_material symbol="{1}" target="#{2}"/>\n'.format('\t'*nTab, self.material_symbol, self.material.id))
        fid.write('{0}</technique_common> </bind_material>\n'.format('\t'*nTab))

#********************************************************************************
class GeometryNode:
    def __init__(self, geom, matnode_list):
        self.geom = geom
        self.matnode_list = matnode_list

    def write(self, fid, nTab=0):
        fid.write('{0}<instance_geometry url="#{1}">\n'.format('\t'*nTab, self.geom.id))
        nTab = nTab + 1
        for matnode in self.matnode_list:
            matnode.write(fid, nTab)
        nTab = nTab - 1
        fid.write('{0}</instance_geometry>\n'.format('\t'*nTab))

#********************************************************************************
class Node:
    def __init__(self, id, children):
        self.id = id
        self.geonode_list = children

    def write(self, fid, nTab=0):
        fid.write('{0}<node id="{1}" name="{2}">\n'.format('\t'*nTab, self.id, self.id))
        nTab = nTab + 1
        for geo in self.geonode_list:
            geo.write(fid, nTab)
        nTab = nTab - 1
        fid.write('{0}</node>\n'.format('\t'*nTab))


#********************************************************************************
class Scene:
    def __init__(self, id, node_list):
        self.id = id
        self.node_list = node_list

    def write(self, fid, nTab=0):
        fid.write('{0}<visual_scene id="{1}">\n'.format('\t'*nTab, self.id))
        nTab = nTab + 1
        for node in self.node_list:
            node.write(fid, nTab)
        nTab = nTab - 1
        fid.write('{0}</visual_scene>\n'.format('\t'*nTab))


#********************************************************************************
class Collada:
    def __init__(self):
        self.effects = []
        self.materials = []
        self.geometries = []
        self.scenes = []
        self.scene = None

    def write(self, filename):
        fid = open(filename, 'w')
        fid.write('<COLLADA xmlns="http://www.collada.org/2005/11/COLLADASchema" version="1.4.1">\n')
        fid.write('  <asset>\n')
        fid.write('    <up_axis>Y_UP</up_axis>\n')
        fid.write('  </asset>\n')
        
        fid.write('  <library_effects>\n')
        for effect in self.effects:
            effect.write(fid, 1)
        fid.write('  </library_effects>\n')

        fid.write('  <library_materials>\n')
        for material in self.materials:
            material.write(fid, 1)
        fid.write('  </library_materials>\n')
        
        fid.write('  <library_geometries>\n')
        for geo in self.geometries:
            geo.write(fid, 1)
        fid.write('  </library_geometries>\n')
        
        fid.write('  <library_visual_scenes>\n')
        for sce in self.scenes:
            sce.write(fid, 1)
        fid.write('  </library_visual_scenes>\n')

        fid.write('  <scene>\n')
        if self.scene != None:
            fid.write('    <instance_visual_scene url="#{0}" />\n'.format(self.scene.id))
        fid.write('  </scene>\n')

        fid.write('</COLLADA>\n')
        fid.close()




#********************************************************************************
def Normalize(v):
    return v / numpy.sqrt( numpy.dot(v,v) + 1e-3 )

#********************************************************************************
def GenIceCone2D(effect, lengthScopeZone, horizontalAngle, detail, r_offset=numpy.zeros(3), R_offset=numpy.matrix(numpy.eye(3))):
    mesh = Collada()

    mat = Material("material0", "mymaterial", effect)
    mesh.effects.append(effect)
    mesh.materials.append(mat)

    vert_floats = [0, 0, 0]
    normal_floats = [0, 1, 0]

    angle = 90.0 - horizontalAngle / 2.0
    while angle <= 90.0 + horizontalAngle / 2.0:
        vert_floats.append(math.sin(math.radians(angle)) * lengthScopeZone)
        vert_floats.append(math.cos(math.radians(angle)) * lengthScopeZone)
        vert_floats.append(0)

        normal_floats.append(0)
        normal_floats.append(1)
        normal_floats.append(0)

        angle += float(horizontalAngle) / detail
    
    vert_src = FloatSource("cubeverts-array", vert_floats, ('X', 'Y', 'Z'))
    normal_src = FloatSource("cubenormals-array", normal_floats, ('X', 'Y', 'Z'))

    # translation and rotation offset
    R_T = R_offset.T
    for kk in range(0, len(vert_src)):
        vert_src.data[kk][:] = r_offset + (vert_src.data[kk] * R_T)

    geom = Geometry("geometry0", "mycube", vert_src, normal_src)

    input_list = InputList()
    input_list.addInput(0, 'VERTEX', "#cubeverts-array")
    input_list.addInput(1, 'NORMAL', "#cubenormals-array")

    indices_int = []
    for i in range(1, detail+1):
        indices_int.append(0)
        indices_int.append(i+1)
        indices_int.append(i)

    triset = geom.createTriangleSet(indices_int, input_list, "materialref")
    geom.primitives.append(triset)
    mesh.geometries.append(geom)

    matnode = MaterialNode("materialref", mat)
    geomnode = GeometryNode(geom, [matnode])
    node = Node("node0", children=[geomnode])

    myscene = Scene("myscene", [node])
    mesh.scenes.append(myscene)
    mesh.scene = myscene

    return mesh


#********************************************************************************
def GenSphere(mesh, nRings, nSegments, lengthScopeZone, lengthSensorHead, horizontalAngle, verticalAngle, r_offset=numpy.zeros(3), R_offset=numpy.matrix(numpy.eye(3))):
    r = 1.0
    alpha_horz = math.radians(horizontalAngle / 2.0)
    cos_horz = (lengthScopeZone - lengthSensorHead) * math.sin(alpha_horz) / math.cos(alpha_horz)
    
    alpha_vert = math.radians(verticalAngle / 2.0)
    cos_vert = (lengthScopeZone - lengthSensorHead) * math.sin(alpha_vert) / math.cos(alpha_vert)

    vert_floats = []
    indices_int = []

    fDeltaRingAngle = (math.pi / nRings)
    fDeltaSegAngle = (2 * math.pi / nSegments)
    wVerticeIndex = 0

    # Generate the group of rings for the sphere
    for ring in range(0, nRings + 1):
        r0 = r * math.sin (ring * fDeltaRingAngle)
        y0 = r * math.cos (ring * fDeltaRingAngle)  * lengthSensorHead + lengthScopeZone - lengthSensorHead
 
        # Generate the group of segments for the current ring
        for seg in range(0, nSegments + 1):
            z0 = r0 * math.sin(seg * fDeltaSegAngle) * cos_horz
            x0 = r0 * math.cos(seg * fDeltaSegAngle) * cos_vert
 
            # Add one vertex to the strip which makes up the sphere
            vert_floats.extend([y0, z0, x0])

            if ring < nRings/2:
                # each vertex (except the last) has six indices pointing to it
                indices_int.append( wVerticeIndex + nSegments)
                indices_int.append( wVerticeIndex)               
                indices_int.append( wVerticeIndex + nSegments + 1)
                indices_int.append( wVerticeIndex )
                indices_int.append( wVerticeIndex + 1)
                indices_int.append( wVerticeIndex + nSegments + 1)
                wVerticeIndex = wVerticeIndex + 1

    vert_src = FloatSource("sphereverts-array", vert_floats, ('X', 'Y', 'Z'))

    # translation and rotation offset
    R_T = R_offset.T
    for kk in range(0, len(vert_src)):
        vert_src.data[kk][:] = r_offset + (vert_src.data[kk] * R_T)

    # generate normals
    normal_floats = []
    indices_int_new = []
    for kk in range(0, len(indices_int)//3):
        ii = kk * 3
        i1, i2, i3 = indices_int[ii], indices_int[ii+1], indices_int[ii+2]
        v1, v2, v3 = vert_src.data[i1], vert_src.data[i2], vert_src.data[i3]
        v12 = v2 - v1
        v13 = v3 - v1
        normal_floats.extend(Normalize(numpy.cross(v12, v13)).tolist())
        indices_int_new.extend([i1, kk, i2, kk, i3, kk])

    normal_src = FloatSource("spherenormals-array", normal_floats, ('X', 'Y', 'Z'))
    geom = Geometry("geometry1", "sphere", vert_src, normal_src)

    input_list = InputList()
    input_list.addInput(0, 'VERTEX', "#sphereverts-array")
    input_list.addInput(1, 'NORMAL', "#spherenormals-array")

    triset = geom.createTriangleSet(indices_int_new, input_list, "materialref")
    geom.primitives.append(triset)

    return geom


#********************************************************************************
def GenCone(mesh, lengthScopeZone, lengthSensorHead, horizontalAngle, verticalAngle, detail, r_offset=numpy.zeros(3), R_offset=numpy.matrix(numpy.eye(3))):
    alpha_horz = math.radians(horizontalAngle / 2.0)
    cos_horz = (lengthScopeZone - lengthSensorHead) * math.sin(alpha_horz) / math.cos(alpha_horz)
    
    alpha_vert = math.radians(verticalAngle / 2.0)
    cos_vert = (lengthScopeZone - lengthSensorHead) * math.sin(alpha_vert) / math.cos(alpha_vert)


    vert_floats = [0.0, 0.0, 0.0]

    angle = 0.0
    while angle < 360.0:
        vert_floats.append((lengthScopeZone - lengthSensorHead))
        vert_floats.append(math.sin(math.radians(angle)) * cos_horz)
        vert_floats.append(math.cos(math.radians(angle)) * cos_vert)
        angle += 360.0 / detail

    input_list = InputList()
    input_list.addInput(0, 'VERTEX', "#coneverts-array")
    input_list.addInput(1, 'NORMAL', "#conenormals-array")

    vert_src = FloatSource("coneverts-array", vert_floats, ('X', 'Y', 'Z'))

    # translation and rotation offset
    R_T = R_offset.T
    for kk in range(0, len(vert_src)):
        vert_src.data[kk][:] = r_offset + (vert_src.data[kk] * R_T)
    
    indices_int = []
    normal_floats = []
    for i in range(1, detail):
        v1 = vert_src.data[i] - vert_src.data[0]
        v2 = vert_src.data[i+1] - vert_src.data[0]
        normal_floats.extend( Normalize(numpy.cross(v1, v2)).tolist() )
        
        indices_int.extend([i, i-1, i+1, i-1, 0, i-1])
        
    v1 = vert_src.data[detail] - vert_src.data[0]
    v2 = vert_src.data[1] - vert_src.data[0]
    normal_floats.extend( Normalize(numpy.cross(v1, v2)).tolist() )
    indices_int.extend([0, i, detail, i, 1, i])

    normal_src = FloatSource("conenormals-array", normal_floats, ('X', 'Y', 'Z'))
    
    geom = Geometry("geometry0", "cone", vert_src, normal_src)
    triset = geom.createTriangleSet(indices_int, input_list, "materialref")
    geom.primitives.append(triset)
    return geom

#********************************************************************************
def GenIceCone3D(effect, lengthScopeZone, lengthSensorHead, horizontalAngle, verticalAngle, detail, r_offset=numpy.zeros(3), R_offset=numpy.matrix(numpy.eye(3))):
    mesh  = Collada()

    mat = Material("material", "mymaterial", effect)
    matnode = MaterialNode("materialref", mat)

    mesh.effects.append(effect)
    mesh.materials.append(mat)

    cone = GenCone(mesh, lengthScopeZone, lengthSensorHead, horizontalAngle, verticalAngle, detail, r_offset=r_offset, R_offset=R_offset)
    sphere = GenSphere(mesh, detail, detail, lengthScopeZone, lengthSensorHead, horizontalAngle, verticalAngle, r_offset=r_offset, R_offset=R_offset)

    mesh.geometries.append(cone)
    mesh.geometries.append(sphere)
    
    geomnodeCone = GeometryNode(cone, [matnode])
    geomnodeSphere = GeometryNode(sphere, [matnode])
    node = Node("node0", children=[geomnodeCone, geomnodeSphere])

    myscene = Scene("myscene", [node])
    mesh.scenes.append(myscene)
    mesh.scene = myscene

    return mesh

#********************************************************************************
def GenPyramid(effect, lengthScopeZone, lengthSensorHead, horizontalAngle, verticalAngle, r_offset=numpy.zeros(3), R_offset=numpy.matrix(numpy.eye(3))):
    mesh  = Collada()

    mat = Material("material0", "mymaterial", effect)
    mesh.effects.append(effect)
    mesh.materials.append(mat)

    vert_floats = []

    alpha_horz = math.radians(horizontalAngle / 2.0)
    cos_horz = lengthScopeZone * math.sin(alpha_horz) / math.cos(alpha_horz)
    
    alpha_vert = math.radians(verticalAngle / 2.0)
    cos_vert = lengthScopeZone * math.sin(alpha_vert) / math.cos(alpha_vert)


    vert_floats.append(0)
    vert_floats.append(0)
    vert_floats.append(0)

    vert_floats.append(lengthScopeZone)
    vert_floats.append(cos_horz)
    vert_floats.append(cos_vert)

    vert_floats.append(lengthScopeZone)
    vert_floats.append(-cos_horz)
    vert_floats.append(cos_vert)

    vert_floats.append(lengthScopeZone)
    vert_floats.append(-cos_horz)
    vert_floats.append(-cos_vert)

    vert_floats.append(lengthScopeZone)
    vert_floats.append(cos_horz)
    vert_floats.append(-cos_vert)

    input_list = InputList()
    input_list.addInput(0, 'VERTEX', "#cubeverts-array")
    input_list.addInput(1, 'NORMAL', "#cubenormals-array")

    indices_int = [0, 1, 4,    0, 2, 1,     0, 3, 2,    0, 4, 3,    2, 4, 1,      2, 3, 4]
    vert_src = FloatSource("cubeverts-array", vert_floats, ('X', 'Y', 'Z'))

    # translation and rotation offset
    R_T = R_offset.T
    for kk in range(0, len(vert_src)):
        vert_src.data[kk][:] = r_offset + (vert_src.data[kk] * R_T)

    # generate normals
    normal_floats = []
    indices_int_new = []
    for kk in range(0, len(indices_int)//3):
        ii = kk * 3
        i1, i2, i3 = indices_int[ii], indices_int[ii+1], indices_int[ii+2]
        v1, v2, v3 = vert_src.data[i1], vert_src.data[i2], vert_src.data[i3]
        v12 = v2 - v1
        v13 = v3 - v1
        normal_floats.extend( Normalize(numpy.cross(v12, v13)).tolist() )
        indices_int_new.extend([i1, kk, i2, kk, i3, kk])

    normal_src = FloatSource("cubenormals-array", normal_floats, ('X', 'Y', 'Z'))
    geom = Geometry("geometry0", "mycube", vert_src, normal_src)

    triset = geom.createTriangleSet(indices_int_new, input_list, "materialref")
    geom.primitives.append(triset)
    mesh.geometries.append(geom)

    matnode = MaterialNode("materialref", mat)
    geomnode = GeometryNode(geom, [matnode])
    node = Node("node0", children=[geomnode])

    myscene = Scene("myscene", [node])
    mesh.scenes.append(myscene)
    mesh.scene = myscene

    return mesh

#********************************************************************************
# GetApplicationActiveProject
#********************************************************************************
def GetApplicationActiveProject(AppName, isVisible = True):
    from win32com.client import Dispatch
    try:
        App = Dispatch(AppName)
        App.Visible = isVisible
    except Exception as e:
        raise Exception('Can not open {} Application. Please check if {} is installed properly.\n{}'.format(AppName, AppName, str(e)))

    ActPrj = App.ActiveProject
    if ActPrj == None:
        raise Exception('*** ERROR: no {} project is opened'.format(AppName))
        
    ActExp = ActPrj.ActiveExperiment
    if ActExp == None:
        raise Exception('*** ERROR: no {} experiment is opened'.format(AppName))
    
    return (App, ActPrj, ActExp)

#********************************************************************************
# GetLibraryManager
#********************************************************************************
def GetLibraryManager():
    from win32com.client import Dispatch
    try:
        App = Dispatch('MotionDesk.Application')
        App.Visible = True
    except Exception as e:
        raise Exception('Can not open MotionDesk Application. Please check if MotionDesk is installed properly.\n' + str(e))
    return App.LibraryManagement

#********************************************************************************
# GetActiveParamSet
#********************************************************************************
def GetActiveParamSet():
    App, ActPrj, ActExp = GetApplicationActiveProject('ModelDesk.Application')

    if ActExp.ActiveParameterSet == None:
        raise Exception('no active ModelDesk ParameterSet is opened.')

    return App.ActiveProject.ActiveExperiment.ActiveParameterSet

#********************************************************************************
# GetParameterRecrods
#********************************************************************************
def GetParameterRecords(MainComponentStr):
    ParamSet = GetActiveParamSet()
    try:
        MainComponent = ParamSet.MainComponents.Item(MainComponentStr)
    except Exception as e:
        raise Exception('MainComponent "%s" is not found.\n%s' % (MainComponentStr, str(e)))
    
    return MainComponent.ParameterRecords, ParamSet

#********************************************************************************
# PrintParameterRecords
#********************************************************************************
def PrintParameterRecords(ParamRecords):
    for kk in range(0, ParamRecords.Count):
        print("{0}.  {1}".format(kk, ParamRecords.Item(kk).Name))

#********************************************************************************
# GetParameterRecord
#********************************************************************************
def GetParameterRecord(ParamRecords, RecordName):
    ParamRecord = []
    for kk in range(0, ParamRecords.Count):
        if ParamRecords.Item(kk).Name == RecordName:
            ParamRecord.append(ParamRecords.Item(kk))
    return ParamRecord

#********************************************************************************
# PrintParameterAddresses
#********************************************************************************
def PrintParameterAddresses(ParamRecord):
    print('{0}'.format(ParamRecord.Name))
    for kk in range(0, ParamRecord.ParameterAddresses.Count):
        print('{0}.  {1}'.format(kk, ParamRecord.ParameterAddresses.Item(kk)))


#********************************************************************************
# PrintParameterAddresses
#********************************************************************************
def GetParameterAddressValue(ParamSet, ParamRecord, ParAddressStr):
    value = None
    for kk in range(0, ParamRecord.ParameterAddresses.Count):
        if ParamRecord.ParameterAddresses.Item(kk).find(ParAddressStr) != -1:
            ParAddress = ParamSet.Find('{0}.{1}'.format(ParamRecord.ParameterAddresses.Item(kk), ParamRecord.InstanceID))
            if ParAddress.TypeName == 'Scalar':
                value = ParAddress.V
            else: # ParAddress.TypeName == 'Vector':
                value = ParAddress.V.Value
            break
    if value == None:
        raise Exception('"{0}" can not be found in {1}.\n'.format(ParAddressStr, ParamRecord.Name))
    return value


#********************************************************************************
# Rotation Matrix - X axis
#********************************************************************************
def RotX(vRad):
    cosV = math.cos(vRad)
    sinV = math.sin(vRad)
    return numpy.matrix([[1., 0., 0.], [0., cosV, -sinV], [0., sinV, cosV]])

#********************************************************************************
# Rotation Matrix - Y axis
#********************************************************************************
def RotY(vRad):
    cosV = math.cos(vRad)
    sinV = math.sin(vRad)
    return numpy.matrix([[cosV, 0., sinV], [0., 1., 0.], [-sinV, 0., cosV]])

#********************************************************************************
# Rotation Matrix - Z axis
#********************************************************************************
def RotZ(vRad):
    cosV = math.cos(vRad)
    sinV = math.sin(vRad)
    return numpy.matrix([[cosV, -sinV, 0.], [sinV, cosV, 0.], [0., 0., 1.]])

#********************************************************************************
# Create Rotation Matrix ZYX
#********************************************************************************
def RotMatZYX(angleXYZDeg):
    xRad, yRad, zRad = [math.pi/180.*v for v in angleXYZDeg]
    return RotZ(zRad) * RotY(yRad) * RotX(xRad)

#********************************************************************************
# GenSensorFromModelDesk
#********************************************************************************
def GenSensorFromModelDesk(chassisObjectName, attachToChassis=True):
    ParamRecords, ParamSet = GetParameterRecords('Environment')

    # transparency = 1.0 => No transparency
    effect3d = Effect("effect0", diffuse=(0.0, 0.0, 0.1), ambient=(0.0, 0.0, 0.8, 1.0), transparency=1.0)
    effect2d = Effect("effect0", diffuse=(0.0, 0.0, 0.0), ambient=(0.8, 0.0, 0.0, 1.0), transparency=1.0)

    # get temp folder and create if not yet exist
    tempDir = tempfile.gettempdir() + '\\asm\\'
    if not os.path.exists(tempDir):
        os.makedirs(tempDir)
    print('*** Collada will be created temporary in folder: {}'.format(tempDir))
    
    r_offset, R_offset = numpy.zeros(3), numpy.mat(numpy.eye(3))
    
    #=== Object Sensor 3D ===
    ObjSensor3dName = []
    ObjSensor3dEnab = [] # enable or disable
    ParamRecordList = GetParameterRecord(ParamRecords, 'Object Sensor 3D')
    print('*** Object sensor 3d: found {}'.format(len(ParamRecordList)))
    for kk in range(0, len(ParamRecordList)):
        print('    ID {:02}, {}'.format(ParamRecordList[kk].InstanceID, ParamRecordList[kk].FileName))
        Pos_Sensor_Apex_CoorSys_V = GetParameterAddressValue(ParamSet, ParamRecordList[kk], 'Const_Pos_Sensor_Apex_CoorSys_V')
        Angle_Orientation_Sensor_CoorSys_V = GetParameterAddressValue(ParamSet, ParamRecordList[kk], 'Const_Angle_Orientation_Sensor_CoorSys_V')
        r_offset, R_offset = numpy.zeros(3), numpy.mat(numpy.eye(3))
        if attachToChassis:
            print('    translation and rotation offset are considered')
            print('    generated sensor will be attached to the chassis')
            r_offset[:] = [Pos_Sensor_Apex_CoorSys_V[0], -Pos_Sensor_Apex_CoorSys_V[1], -Pos_Sensor_Apex_CoorSys_V[2]]
            R_offset = RotMatZYX([Angle_Orientation_Sensor_CoorSys_V[0], -Angle_Orientation_Sensor_CoorSys_V[1], -Angle_Orientation_Sensor_CoorSys_V[2]])

        Sw_Sensor_Enable = GetParameterAddressValue(ParamSet, ParamRecordList[kk], 'Sw_Sensor_Enable')
        Sw_Geometry = GetParameterAddressValue(ParamSet, ParamRecordList[kk], 'Sw_Geometry')
        Length_ScopeZone = GetParameterAddressValue(ParamSet, ParamRecordList[kk], 'Const_Length_ScopeZone')
        Length_ScopeZone_Head = GetParameterAddressValue(ParamSet, ParamRecordList[kk], 'Const_Length_ScopeZone_Head')
        Angle_ScopeZone_Horizontal = GetParameterAddressValue(ParamSet, ParamRecordList[kk], 'Const_Angle_ScopeZone_Horizontal')
        Angle_ScopeZone_Vertical = GetParameterAddressValue(ParamSet, ParamRecordList[kk], 'Const_Angle_ScopeZone_Vertical')
        print('        Sw_Sensor_Enable {}'.format(Sw_Sensor_Enable))
        print('        Sw_Geometry {}'.format(Sw_Geometry))
        print('        Pos_Sensor_Apex_CoorSys_V {}'.format(Pos_Sensor_Apex_CoorSys_V))
        print('        Angle_Orientation_Sensor_CoorSys_V {}'.format(Angle_Orientation_Sensor_CoorSys_V))
        print('        Length_ScopeZone {}'.format(Length_ScopeZone))
        print('        Length_ScopeZone_Head {}'.format(Length_ScopeZone_Head))
        print('        Angle_ScopeZone_Horizontal {}'.format(Angle_ScopeZone_Horizontal))
        print('        Angle_ScopeZone_Vertical {}'.format(Angle_ScopeZone_Vertical))
        mesh = None
        if Sw_Geometry == 1.0: # Pyramid
            mesh = GenPyramid(effect3d, lengthScopeZone = Length_ScopeZone, lengthSensorHead = Length_ScopeZone_Head, \
                              horizontalAngle = Angle_ScopeZone_Horizontal, verticalAngle = Angle_ScopeZone_Vertical, \
                              r_offset = r_offset, R_offset = R_offset)
        else:
            mesh = GenIceCone3D(effect3d, lengthScopeZone = Length_ScopeZone, lengthSensorHead = Length_ScopeZone_Head, \
                              horizontalAngle = Angle_ScopeZone_Horizontal, verticalAngle = Angle_ScopeZone_Vertical, \
                              detail=32, \
                              r_offset = r_offset, R_offset = R_offset)

        fileName = 'Sensor3D_{:02}'.format(ParamRecordList[kk].InstanceID)
        ObjSensor3dName.append(fileName)
        ObjSensor3dEnab.append(Sw_Sensor_Enable)
        mesh.write(tempDir + fileName + '.dae')

    #=== Object Sensor 2D Geometry (old Sensor 2D implementation) ===
    ObjSensor2dName = []
    ObjSensor2dEnab = [] # enable or disable
    ParamRecordList = GetParameterRecord(ParamRecords, 'Object Sensor 2D Geometry')
    print('*** Object Sensor 2d Geometry: found {}'.format(len(ParamRecordList)))
    for kk in range(0, len(ParamRecordList)):
        print('    ID {:02}, {}'.format(ParamRecordList[kk].InstanceID, ParamRecordList[kk].FileName))

        Sw_Sensor_Enable = GetParameterAddressValue(ParamSet, ParamRecordList[kk], 'Sensor_Enable')
        Pos_Sensor = GetParameterAddressValue(ParamSet, ParamRecordList[kk], 'Pos_Sensor')
        Angle_Orientation_Sensor = GetParameterAddressValue(ParamSet, ParamRecordList[kk], 'Angle_Orientation_Sensor')
        Length_ScopeZone = GetParameterAddressValue(ParamSet, ParamRecordList[kk], 'Length_ScopeZone')
        Angle_ScopeZone_Horizontal = GetParameterAddressValue(ParamSet, ParamRecordList[kk], 'Angle_ScopeZone_Horizontal')
        print('        Sensor_Enable {}'.format(Sw_Sensor_Enable))
        print('        Pos_Sensor {}'.format(Pos_Sensor))
        print('        Angle_Orientation_Sensor {}'.format(Angle_Orientation_Sensor))
        print('        Length_ScopeZone {}'.format(Length_ScopeZone))
        print('        Angle_ScopeZone_Horizontal {}'.format(Angle_ScopeZone_Horizontal))
        r_offset[:] = [Pos_Sensor[0], -Pos_Sensor[1], -Pos_Sensor[2]]
        R_offset = RotZ(-Angle_Orientation_Sensor * math.pi/180.0)
        mesh = GenIceCone2D(effect2d, lengthScopeZone=Length_ScopeZone, horizontalAngle=Angle_ScopeZone_Horizontal, detail=32, r_offset=r_offset, R_offset=R_offset)

        fileName = 'Sensor2DGeo_{:02}'.format(ParamRecordList[kk].InstanceID)
        ObjSensor2dName.append(fileName)
        ObjSensor2dEnab.append(Sw_Sensor_Enable)
        mesh.write(tempDir + fileName + '.dae')

    #=== Object Sensor 2D ===
    ObjSensor2dNameNew = []
    ObjSensor2dEnabNew = [] # enable or disable
    ParamRecordList = GetParameterRecord(ParamRecords, 'Object Sensor 2D')
    print('*** Object Sensor 2d: found {}'.format(len(ParamRecordList)))
    for kk in range(0, len(ParamRecordList)):
        print('    ID {:02}, {}'.format(ParamRecordList[kk].InstanceID, ParamRecordList[kk].FileName))

        Sw_Sensor_Enable = GetParameterAddressValue(ParamSet, ParamRecordList[kk], 'Sw_Sensor_Enable')
        Pos_Sensor = GetParameterAddressValue(ParamSet, ParamRecordList[kk], 'Const_Pos_Sensor_Apex_CoorSys_V')
        Angle_Orientation_Sensor = GetParameterAddressValue(ParamSet, ParamRecordList[kk], 'Const_Angle_z_Orientation_Sensor_CoorSys_V')
        Length_ScopeZone = GetParameterAddressValue(ParamSet, ParamRecordList[kk], 'Const_Length_ScopeZone')
        Angle_ScopeZone_Horizontal = GetParameterAddressValue(ParamSet, ParamRecordList[kk], 'Const_Angle_ScopeZone_Horizontal')
        print('        Sw_Sensor_Enable {}'.format(Sw_Sensor_Enable))
        print('        Pos_Sensor {}'.format(Pos_Sensor))
        print('        Angle_Orientation_Sensor {}'.format(Angle_Orientation_Sensor))
        print('        Length_ScopeZone {}'.format(Length_ScopeZone))
        print('        Angle_ScopeZone_Horizontal {}'.format(Angle_ScopeZone_Horizontal))
        r_offset[:] = [Pos_Sensor[0], -Pos_Sensor[1], -Pos_Sensor[2]]
        R_offset = RotZ(-Angle_Orientation_Sensor * math.pi/180.0)
        mesh = GenIceCone2D(effect2d, lengthScopeZone=Length_ScopeZone, horizontalAngle=Angle_ScopeZone_Horizontal, detail=32, r_offset=r_offset, R_offset=R_offset)

        fileName = 'Sensor2D_{:02}'.format(ParamRecordList[kk].InstanceID)
        ObjSensor2dNameNew.append(fileName)
        ObjSensor2dEnabNew.append(Sw_Sensor_Enable)
        mesh.write(tempDir + fileName + '.dae')

    ObjSensor2dName = ObjSensor2dName + ObjSensor2dNameNew
    ObjSensor2dEnab = ObjSensor2dEnab + ObjSensor2dEnabNew
    del ObjSensor2dNameNew, ObjSensor2dEnabNew

    ##=== Traffic Sign Sensor Geometry ===
    #ObjTrfSignSensorName = []
    #ObjTrfSignSensorEnab = [] # enable or disable
    #ParamRecordList = GetParameterRecord(ParamRecords, 'Traffic Sign Sensor Geometry')
    #print('*** Traffic Sign Sensor Geometry: found {}'.format(len(ParamRecordList)))
    #for kk in range(0, len(ParamRecordList)):
    #    print('    ID {:02}, {}'.format(ParamRecordList[kk].InstanceID, ParamRecordList[kk].FileName))
    #
    #    Pos_Sensor_Apex_CoorSys_V = GetParameterAddressValue(ParamSet, ParamRecordList[kk], 'Pos_Sensor')
    #    Angle_Orientation_Sensor_CoorSys_V = GetParameterAddressValue(ParamSet, ParamRecordList[kk], 'Angle_Orientation_Sensor')
    #    r_offset, R_offset = numpy.zeros(3), numpy.mat(numpy.eye(3))
    #    if attachToChassis:
    #        print('    translation and rotation offset are considered')
    #        print('    generated sensor will be attached to the chassis')
    #        r_offset[:] = [Pos_Sensor_Apex_CoorSys_V[0], -Pos_Sensor_Apex_CoorSys_V[1], -Pos_Sensor_Apex_CoorSys_V[2]]
    #        R_offset = RotMatZYX([Angle_Orientation_Sensor_CoorSys_V[0], -Angle_Orientation_Sensor_CoorSys_V[1], -Angle_Orientation_Sensor_CoorSys_V[2]])
    #
    #    Sw_Sensor_Enable = GetParameterAddressValue(ParamSet, ParamRecordList[kk], 'Sensor_Enable')
    #    Length_ScopeZone = GetParameterAddressValue(ParamSet, ParamRecordList[kk], 'Length_ScopeZone')
    #    Angle_ScopeZone_Horizontal = GetParameterAddressValue(ParamSet, ParamRecordList[kk], 'Angle_ScopeZone_Horizontal')
    #    Angle_ScopeZone_Vertical = GetParameterAddressValue(ParamSet, ParamRecordList[kk], 'Angle_ScopeZone_Vertical')
    #    print('        Sw_Sensor_Enable {}'.format(Sw_Sensor_Enable))
    #    print('        Pos_Sensor_Apex_CoorSys_V {}'.format(Pos_Sensor_Apex_CoorSys_V))
    #    print('        Angle_Orientation_Sensor_CoorSys_V {}'.format(Angle_Orientation_Sensor_CoorSys_V))
    #    print('        Length_ScopeZone {}'.format(Length_ScopeZone))
    #    print('        Angle_ScopeZone_Horizontal {}'.format(Angle_ScopeZone_Horizontal))
    #    print('        Angle_ScopeZone_Vertical {}'.format(Angle_ScopeZone_Vertical))
    #    mesh = GenPyramid(effect3d, lengthScopeZone = Length_ScopeZone, lengthSensorHead = Length_ScopeZone_Head, \
    #                      horizontalAngle = Angle_ScopeZone_Horizontal, verticalAngle = Angle_ScopeZone_Vertical, \
    #                      r_offset = r_offset, R_offset = R_offset)
    #
    #    fileName = 'TrafficSignSensor_{:02}'.format(ParamRecordList[kk].InstanceID)
    #    ObjTrfSignSensorName.append(fileName)
    #    ObjTrfSignSensorEnab.append(Sw_Sensor_Enable)
    #    mesh.write(tempDir + fileName + '.dae')



    #============================
    #=== import to MotionDesk ===
    #============================
    LibManager = GetLibraryManager()
    print('*** Import generated collada to MotionDesk')
    for meshName in ObjSensor3dName:
        print('    Sensor3d: {}'.format(meshName))
        LibManager.ImportElement(tempDir + meshName + '.dae', r'Sensor3d', 'Sensor3d', True)
    for meshName in ObjSensor2dName:
        print('    Sensor2d: {}'.format(meshName))
        LibManager.ImportElement(tempDir + meshName + '.dae', r'Sensor2d', 'Sensor2d', True)

    App, ActPrj, ActExp = GetApplicationActiveProject('MotionDesk.Application')
    MOM = ActExp.VisualizationManagement.MovableObjects # Moveable Object Manager
    print('*** Added to MotionDesk as moveable object')
    for kk in range(0, len(ObjSensor3dName)):
        MOM.Remove(ObjSensor3dName[kk])
        SensorNew = MOM.Add(elemTypes.Customer, r'Sensor3d\{}'.format(ObjSensor3dName[kk]), ObjSensor3dName[kk])
        time.sleep(0.1)
        if ObjSensor3dEnab[kk] == 0:
            SensorNew.IsVisible = False
        print('    Sensor3d: {}'.format(ObjSensor3dName[kk]))

        if attachToChassis:
            Coupe = MOM.Item(chassisObjectName, 0)
            if Coupe != None:
                SensorNew.MotionDataStream = Coupe.MotionDataStream
                try:
                    SensorNew.MotionDataID = Coupe.MotionDataID
                except Exception as e:
                    print('### WARN: {}'.format(str(e)))
                    print('    MotionDataID can not be set. Please try to connect DataStream manually.\n')
            elif kk == 0:
                print('### WARN: moveable object "{}" is not found. Therefore motion data stream is not connected.'.format(chassisObjectName))
                    
        else:
            Sensor = MOM.Item('Sensor_0{}'.format(kk+1), 0)
            if Sensor != None:
                #Sensor.IsVisible = False
                SensorNew.MotionDataStream = Sensor.MotionDataStream
                try:
                    SensorNew.MotionDataID = Sensor.MotionDataID
                except Exception as e:
                    print('### WARN: {}'.format(str(e)))
                    print('    MotionDataID can not be set. Please try to connect DataStream manually.\n')
                #Sensor.GeometryFilePath = SensorNew.GeometryFilePath

        # set RenderMode = "Tranparent" and Transparency = 0.7. Should work since RLS 17-B
        try:
            SensorNew.RenderMode = 4        # 4 : Transparent
            SensorNew.Transparency = 70.0
        except:
            if kk == 0:
                print('### WARN: render mode transparency can not be set.')
            
    for kk in range(0, len(ObjSensor2dName)):
        MOM.Remove(ObjSensor2dName[kk])
        SensorNew = MOM.Add(elemTypes.Customer, r'Sensor2d\{}'.format(ObjSensor2dName[kk]), ObjSensor2dName[kk])
        time.sleep(0.1)
        if ObjSensor2dEnab[kk] == 0:
            SensorNew.IsVisible = False
        print('    Sensor2d: {}'.format(ObjSensor2dName[kk]))

        Coupe = MOM.Item(chassisObjectName, 0)
        if Coupe != None:
            SensorNew.MotionDataStream = Coupe.MotionDataStream
            try:
                SensorNew.MotionDataID = Coupe.MotionDataID
            except Exception as e:
                print('### WARN: {}'.format(str(e)))
                print('    MotionDataID can not be set. Please try to connect DataStream manually.')
        elif kk == 0:
            print('### WARN: moveable object "{}" is not found. Therefore motion data stream is not connected.'.format(chassisObjectName))
            

        # set RenderMode = "Tranparent" and Transparency = 0.7. Should work since RLS 17-B
        try:
            SensorNew.RenderMode = 4        # 4 : Transparent
            SensorNew.Transparency = 70.0
        except:
            if kk == 0:
                print('### WARN: render mode transparency can not be set.')

    # remove the generated dae
    for meshName in ObjSensor3dName:
        os.remove(tempDir + meshName + '.dae')
    for meshName in ObjSensor2dName:
        os.remove(tempDir + meshName + '.dae')
    #for meshName in ObjTrfSignSensorName:
    #    os.remove(tempDir + meshName + '.dae')

#********************************************************************************
def Main():
    try:
        GenSensorFromModelDesk(chassisObjectName='Coupe', attachToChassis=True)
    except:
        traceback.print_exc()
    return

#********************************************************************************
# Call the main function
#********************************************************************************
if __name__ == '__main__':
    Main()
    print('*** Finished generated sensor.', time.asctime(), '\n')
