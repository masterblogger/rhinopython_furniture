# Generates simply 2d & 3D rectangular furniture elments
# 
# GNU GENERAL PUBLIC LICENSE Version 3
#
# by Joern Rettweiler, 2018 august 13
#
#
# Tested with Rhino 5 
#
# NO WARRANTY
#
# Note: If you want to create a rhino command that you can call via command promt
# look here: https://developer.rhino3d.com/guides/rhinopython/creating-rhino-commands-using-python/



import rhinoscriptsyntax as rs
import Rhino as rhino



def ac_furniture():
    global geom_functionarea, geom_workarea, geom2d, group3d, obj, obj2d_function
  
    group3d = "geom3d"
    rs.AddGroup(group3d)
    
    
    obj2d_function = []
 
  
  
  
  
  
  
    #############################
    ##FUNCTION DEFINITIONS BEGIN##
    ##############################
  
  
  
  
  
    def ac_layercreation():
        
        global layer_furniture, layer_geom2d, layer_geom3d, layer_workarea, layer_text, layer_functionarea, layer_furniture_color, layer_geom2d_color, layer_geom3d_color, layer_workarea_color, layer_functionarea_color, layer_text_color, layer_geom3d_pro
        
    #Parent layer
        layer_furniture = ("Furniture")
        layer_furniture_color = [0,0,0]
    
    #Enter / Edit Here your furniture layer names EDIT ONLY VALUES IN PARANTHESES,
    #default :2 geom Color red = [255,0,0]
        layer_geom2d = ("AC-Geom2d")
        layer_geom2d_color = [255,0,0]
    
    #default :3D geom Colorwhite = [255,255,255]
        layer_geom3d = ("AC-Geom3d")
        layer_geom3d_color = [255,255,255]
    
    #default :3D geom Colorwhite = [190,190,190]
        layer_geom3d_pro = ("AC-Geom3d_projection")
        layer_geom3d_projection_color = [190,190,190]
        
    #default : workarea Color blue = [0,255,255]
        layer_workarea = ("AC-Working_area")
        layer_workarea_color = [0,255,255]
    
    #default : workarea Color blue = [0,255,255]
        layer_functionarea = ("AC-Function_area")
        layer_functionarea_color = [0,255,255]
    
    #default : Text Color blue = [0,0,0]
        layer_text = ("AC-Text")
        layer_text_color = [0,0,0]
    
    

    
    

        
        #Add layer after previous operation are succesfull
        rs.AddLayer(layer_furniture, layer_furniture_color)
    
        rs.AddLayer(layer_geom2d, layer_geom2d_color, parent=layer_furniture)
    
        rs.AddLayer(layer_geom3d, layer_geom3d_color, parent=layer_furniture)
    
        rs.AddLayer(layer_workarea, layer_workarea_color, parent=layer_furniture)
        rs.LayerLinetype(layer_workarea, linetype="Dashed")
        
        rs.AddLayer(layer_text, layer_text_color, parent=layer_furniture)
        
        rs.AddLayer(layer_geom3d_pro, layer_geom3d_projection_color, parent=layer_furniture)
        rs.LayerLinetype(layer_geom3d_pro, linetype="Dashed")
        
        rs.AddLayer(layer_functionarea, layer_functionarea_color, parent=layer_furniture)
        rs.LayerLinetype(layer_functionarea, linetype="Dashed")
        
        rs.CurrentLayer(layer_furniture)
    
    
    def ac_geom2d(width, depth):
        global geom_text, geom2d, blockname, basepoint
        
        rs.CurrentLayer(layer_geom2d)
        planexy = rs.WorldXYPlane()
        geom2d = rs.AddRectangle(planexy, width, depth)
        
        
        
        geom2d_centroid = rs.CurveAreaCentroid(geom2d)
        
        basepoint = geom2d_centroid[1]
        #rs.AddPoint((geom2d_centroid))
        
        #info text
        textdottext = (furniture_name + "\n" 
        + str(furniture_width_cm)+ " x " + str(furniture_depth_cm))# + "\n" 
        #+ "newline")
        
        
        #rs.AddPoint(geom2d_centroid[0])
        rs.CurrentLayer(layer_text)
        geom_text = rs.AddTextDot(textdottext, geom2d_centroid[0])
        #rhino.text
        #Generate Blockname
        blockname = (str(furniture_name) + str(furniture_width_cm) + "x" + str(furniture_depth_cm))
        
        
        
        
        
        
    def ac_geom2d_workarea(width):
        global geom_workarea, geom_functionarea
        
        planexy_wa = rs.WorldXYPlane()
        
        
        # Reference (2018 august 08) https://www.baua.de/DE/Angebote/Rechtstexte-und-Technische-Regeln/Regelwerk/ASR/pdf/ASR-A1-2.pdf?__blob=publicationFile&v=7
        depth_workarea = -1000
        rs.CurrentLayer(layer_workarea)
        geom_workarea = rs.AddRectangle(planexy_wa, width, depth_workarea)
        
        
        geom_functionarea = geom_workarea
    
    def ac_geom2d_functionarea(width, depth):
        global geom_functionarea, geom_workarea
        
        planexy_wa = rs.WorldXYPlane()
        
        
        # Reference (2018 august 08) https://www.baua.de/DE/Angebote/Rechtstexte-und-Technische-Regeln/Regelwerk/ASR/pdf/ASR-A1-2.pdf?__blob=publicationFile&v=7
        depth = depth * -1 
        rs.CurrentLayer(layer_functionarea)
        geom_functionarea = rs.AddRectangle(planexy_wa, width, depth)
        
        geom_workarea = geom_functionarea
    
    
    def ac_geom3d_table():
        
        global table_foot_3d, geom3d
        rs.CurrentLayer(layer_geom3d_pro)
        
        side_dist = 50 #distance to side
        
        #Table foot base bottom left
        table_pt_1 = (side_dist,side_dist,0)
        foot_1 = rs.AddRectangle(table_pt_1,side_dist,side_dist)
        
        #Table foot base bottom rigth
        table_pt2_x = furniture_width - (side_dist * 2)
        table_pt_2 = (table_pt2_x,side_dist,0)
        foot_2 = rs.AddRectangle(table_pt_2,side_dist,side_dist)
        
        #Table foot base Top right
        table_pt3_y = furniture_depth - (side_dist * 2)
        table_pt_3 = (table_pt2_x, table_pt3_y,0)
        foot_3 = rs.AddRectangle(table_pt_3,side_dist,side_dist)
        
        #Table foot base Top left
        table_pt_4 = (side_dist, table_pt3_y, 0)
        foot_4 = rs.AddRectangle(table_pt_4,side_dist,side_dist)
        
        #add foots to array
        table_foot_2d = [foot_1, foot_2, foot_3, foot_4]
        
        #Extrude 2d foot geometry and put then into array/list
        rs.CurrentLayer(layer_geom3d)
        loop_count = 0
        table_foot_3d = []
        while loop_count < len(table_foot_2d):
            
            table_foot = rs.ExtrudeCurveStraight(table_foot_2d[loop_count], (0,0,0),(0,0,furniture_hight))
            table_foot = rs.CapPlanarHoles(table_foot)
            table_foot_3d.append(table_foot)
            
            loop_count = loop_count + 1
            
        #Add table plate
        plane_rectangle_pt = (0, 0, furniture_hight)
        table_table = rs.AddRectangle(plane_rectangle_pt, furniture_width, furniture_depth)
        table_table = rs.ExtrudeCurveStraight(table_table, (0,0,0),(0,0,20))
        table_table = rs.CapPlanarHoles(table_table)
        
        
        #add polysurfaces objects to group
        obj = rs.ObjectsByType(16, select=False, state = 0)
        rs.AddObjectsToGroup(obj,group3d)
    
    def ac_geom3d_desk():
        #plane = rs.WorldYZPlane()
        #rs.AddArc(plane, 50, 90)
        #plane = rs.PlaneFromPoints((0,420,0),(0,0,50),(0,0,0))
        thickness_elements = 50
        
        rs.CurrentLayer(layer_geom3d)
        #plane = (42,80,0)
        #rs.AddArc(plane, 50, 90)
        
        def ac_geom3d_desk_foot(base):
            
            if base > 0:
                base = base - thickness_elements
            #first 2d bow base for extrusion 
            arc_start_pt = (base,furniture_depth,0)
            arc_end_pt = (base, furniture_depth-thickness_elements, thickness_elements)
            arc_pt_on_arc = (base, furniture_depth - thickness_elements*0.34,thickness_elements*0.66)
            arc_1 = rs.AddArc3Pt(arc_start_pt,arc_end_pt,arc_pt_on_arc)
        
            #second 2d bow base for extrusion 
            arc_start_pt2 = (base,0,0)
            arc_end_pt2 = (base, thickness_elements, thickness_elements)
            arc_pt_on_arc2 = (base, thickness_elements*0.34, thickness_elements*0.66)
            arc_2 = rs.AddArc3Pt(arc_start_pt2,arc_end_pt2,arc_pt_on_arc2)
        
            line_1 = rs.AddLine(arc_end_pt,arc_end_pt2)
            line_2 = rs.AddLine(arc_start_pt,arc_start_pt2)
        
            foot_extrude_base = rs.JoinCurves([arc_1, arc_2, line_1, line_2], delete_input=True)
            foot_extruded = rs.ExtrudeCurveStraight(foot_extrude_base, (base,0,0),(base+thickness_elements,0,0))
            foot_extruded = rs.CapPlanarHoles(foot_extruded)
            
            #add cylinder
            base = (base + thickness_elements/2, furniture_depth/2, thickness_elements)
            hight = furniture_hight - thickness_elements
            radius = thickness_elements / 2 
            rs.AddCylinder(base, hight, radius, cap=True)
            
        ac_geom3d_desk_foot(0)
        ac_geom3d_desk_foot(furniture_width)
        
        #Add table plate
        plane_rectangle_pt = (0, 0, furniture_hight)
        table_table = rs.AddRectangle(plane_rectangle_pt, furniture_width, furniture_depth)
        table_table = rs.ExtrudeCurveStraight(table_table, (0,0,0),(0,0,20))
        table_table = rs.CapPlanarHoles(table_table)
        
        #add polysurfaces objects to group
        obj = rs.ObjectsByType(16, select=False, state = 0)
        rs.AddObjectsToGroup(obj,group3d)
        
        
    def ac_geom3d_shelf_cabinet():
        global shelf_objects
        
        wallthicknesss = 20
        rs.CurrentLayer(layer_geom3d)
        
        
        
        
        
        def ac_geom3d_shelf_cabinet_sidewall(base):
            global sw
            
            if base > 0:
                base = base - wallthicknesss
            
            sw_pt1 = (base,0,0)
            #sw_pt2 = (base, furniture_depth, 0)
            #plane = rs.WorldXYPlane()
            sw = rs.AddRectangle(sw_pt1, wallthicknesss,  furniture_depth)
            
            sw = rs.ExtrudeCurveStraight(sw, (0,0,0), (0,0,(furniture_hight- wallthicknesss)))
            sw = rs.CapPlanarHoles(sw)
        
        def ac_geom3d_shelf_cabinet_inside():
            
            
            base = (wallthicknesss, wallthicknesss, 50)
            shelf_width = furniture_width - 2 * wallthicknesss
            shelf_depth = furniture_depth - 2 * wallthicknesss
            bottom_shelf = rs.AddRectangle(base,shelf_width, shelf_depth)
            bottom_shelf = rs.ExtrudeCurveStraight(bottom_shelf, base, (wallthicknesss,wallthicknesss,0))
            bottom_shelf = rs.CapPlanarHoles(bottom_shelf)
            
            if furniture_hight >= 700:
                shelf_distance = 350 + wallthicknesss
                shelf_count = furniture_hight / shelf_distance
                
                #start posistion -> 50 for distance between bottom shelf
                shelf_position = shelf_distance + 50
                
                print "shelf Count"
                print shelf_count
                #round up
                shelf_count = shelf_count -1.5
                print "shelf Count"
                print shelf_count
                
                
                loopbreaker = 0
                while loopbreaker < shelf_count:
                    
                    base = (wallthicknesss, wallthicknesss, shelf_position)
                    
                    shelf = rs.AddRectangle(base,shelf_width, shelf_depth)
                    
                    
                    #
                    base_extrude_target = (wallthicknesss, wallthicknesss, (shelf_position + wallthicknesss))
                    shelf = rs.ExtrudeCurveStraight(shelf, base, base_extrude_target)
                    
                    shelf = rs.CapPlanarHoles(shelf)
                    
                    
                    shelf_position = shelf_position + shelf_distance
                    
                    loopbreaker = loopbreaker + 1
                    
                    
        
        #back wall
        bw_pt = (wallthicknesss, furniture_depth, 0)
        bw_width = furniture_width - 2* wallthicknesss
                
        bw =rs.AddRectangle(bw_pt, bw_width, (wallthicknesss * -1))
        bw1 = rs.ExtrudeCurveStraight(bw, (0,0,0), (0,0,(furniture_hight- wallthicknesss)))
        bw = rs.CapPlanarHoles(bw1)
        
        

        
        #top
        tw_pt = (0,0,(furniture_hight- wallthicknesss))
        tw_pt_target = (0,0, furniture_hight)
        tw = rs.AddRectangle(tw_pt, furniture_width, furniture_depth)
        tw = rs.ExtrudeCurveStraight(tw, tw_pt, tw_pt_target)
        tw = rs.CapPlanarHoles(tw)
        

        
        #Execute Functions
        ac_geom3d_shelf_cabinet_sidewall(0)

        
        ac_geom3d_shelf_cabinet_sidewall(furniture_width)

        
        ac_geom3d_shelf_cabinet_inside()
        
        
        #add polysurfaces objects to group
        obj = rs.ObjectsByType(16, select=False, state = 0)
        geom3d = rs.AddObjectsToGroup(obj,group3d)
        
        
    def ac_geom3d_wing_door():
        
        
        wallthicknesss = 20
        door_width = furniture_width / 2 - wallthicknesss
        
        
        def ac_geom3d_wing_door_itself(base):
            rotate = "flase"
            base_ogirinal = base
            if base > 0:
                base = base / 2 - wallthicknesss
                rotate = "true"
            
            wdpt = (base + wallthicknesss, 0, 30)
            wdtarget_hight = (furniture_hight - wallthicknesss)
            wdtarget = (base + wallthicknesss,0,wdtarget_hight)
            door1 = rs.AddRectangle(wdpt, door_width, wallthicknesss)
            door1 = rs.ExtrudeCurveStraight(door1, wdpt, wdtarget)
            
            if rotate == "true":
                wdp2 = (base_ogirinal - wallthicknesss, 0, 30)
                rs.RotateObject(door1,wdp2,30,None, copy=False)
            
            
            door1 = rs.CapPlanarHoles(door1)
            
            
        def ac_geom2d_wing_door(base):
            global  obj2d_function
            
            rs.CurrentLayer(layer_functionarea)
            start_y_distance = (-1 * furniture_depth)
            startpt = ((furniture_width / 2), 0 ,0)
            endpt = (wallthicknesss,start_y_distance,0)
            
            point_on_arc_x = (furniture_width / 2) * +0.90
            point_on_arc_y = furniture_depth * -0.33
            point_on_arc = (point_on_arc_x, point_on_arc_y, 0)
            
            line =rs.AddLine(endpt, (wallthicknesss,0,0))
            
            arc = rs.AddArc3Pt(endpt, startpt,point_on_arc)
            opening_projection1 = rs.JoinCurves([line,arc], delete_input=True)
            
            opening_projection2 = rs.MirrorObject(opening_projection1, ((furniture_width /2),0,0), ((furniture_width /2),wallthicknesss,0),copy=True)
            
            
            obj2d_function = [opening_projection2,opening_projection1]
            print "XXXXXXXXX"
            print len(obj2d_function)
            #obj2d_function.append(opening_projection1)
            
        ac_geom3d_wing_door_itself(0)
        ac_geom3d_wing_door_itself(furniture_width)
        
        ac_geom2d_wing_door(0)
        
        


    def ac_lock_prevlayer():
        
        
        layername = rs.LayerNames()
        
        print "layerbane"
        print layername[1]
        print len(layername)
        loopbreaker = 0
        
        
        
        while loopbreaker < len(layername):
            rs.LayerLocked(layername[loopbreaker], locked=True)
            loopbreaker = loopbreaker + 1
            print "loop"
            print loopbreaker

    #############################
    ##FUNCTION DEFINITIONS END###
    #############################
    
    #lock all existing layers
    
    
    
    
    furniture_typ = rs.GetInteger("1=filling cabinet 2=Shelf 3=sideboard 4=table, 5=desk", 5, 0, 5 )
    print furniture_typ
    
    #Get Furniture Dimensions and Scale them to mm
    furniture_width_cm = rs.GetReal("Width of furniture [cm]", 80, 0)
    furniture_width = furniture_width_cm * 10
    furniture_depth_cm = rs.GetReal("Depth of furniture [cm]", 42, 0)
    furniture_depth = furniture_depth_cm * 10
    
        
    
    if furniture_typ == 5:
        furniture_hight = 800
    
    elif furniture_typ == 4:
        furniture_hight = 800
        
    else:
        furniture_hight = rs.GetReal("Hight of furniture [cm]", 80, 0)
        #print("Test")
        furniture_hight = furniture_hight *10
        

    ac_layercreation()
    
    ac_lock_prevlayer()

    #Add text to textvariable
    if furniture_typ == 1:
        #filling cabinet furniture like shelf with wing doors
        furniture_name = "filling cabinet"
        ac_geom2d_functionarea(furniture_width, furniture_depth)
        ac_geom3d_shelf_cabinet()
        ac_geom3d_wing_door()
        
        
    elif furniture_typ == 2:
        furniture_name = "Shelf"
        ac_geom2d_functionarea(furniture_width, furniture_depth)
        ac_geom3d_shelf_cabinet()
    
    elif furniture_typ == 3:
        #sideboard shelf with sliding door
        furniture_name = "Sideboard"
        ac_geom2d_functionarea(furniture_width, furniture_depth)
        ac_geom3d_shelf_cabinet()
    
    elif furniture_typ == 4:
        furniture_name = "Table"
        
        geom_functionarea = rs.AddPoint( (0,0,0) )
        geom_workarea = geom_functionarea
        ac_geom3d_table()
        
    
    elif furniture_typ == 5:
        furniture_name = "Desk"
        ac_geom3d_desk()
        
        rs.AddLayer(layer_text, layer_text_color, parent=layer_furniture)
        ac_geom2d_workarea(furniture_width)
    #elif furniture_typ == 3:
    #    furniture_name = "XXX"
    
    
    
   
    
    rs.CurrentLayer(layer=layer_geom2d)
    ac_geom2d(furniture_width, furniture_depth)
    
    
    
    rs.CurrentLayer(layer=layer_furniture)
    
    #clean useless geom and lock layers
    #lock partial
    rs.LayerLocked(layer_geom2d, locked = True)
    rs.LayerLocked(layer_geom3d_pro, locked = True)
    rs.LayerLocked(layer_workarea, locked = True)
    rs.LayerLocked(layer_functionarea, locked = True)
    rs.LayerLocked(layer_text, locked = True)
    #clean
    obj_delete = rs.ObjectsByType(4, select=False, state=1)
    rs.DeleteObjects(obj_delete)
    
    #unlock layers
    rs.LayerLocked(layer_geom2d, locked = False)
    rs.LayerLocked(layer_geom3d_pro, locked = False)
    rs.LayerLocked(layer_workarea, locked = False)
    rs.LayerLocked(layer_functionarea, locked = False)
    rs.LayerLocked(layer_text, locked = False)
    
    print "objd function value"
    print len(obj2d_function)

    #add all objects curves and polysrf to array/list
    obj3d = rs.ObjectsByType(16, select=False, state = 0)
    blockobj = [geom_text,geom2d, geom_workarea, geom_functionarea]
    blockobj.extend(obj3d)
    blockobj.extend(obj2d_function)
    
    #if len(opening_projection) > 0:
     #   blockobj.extend(opening_projection)
    
    
    rs.CurrentLayer(layer_furniture)
    rs.AddBlock(blockobj, basepoint, blockname, delete_input=True)
    rs.InsertBlock(blockname, basepoint)
    
    #rs.CurrentLayer(layer_furniture)
    #rs.AddBlock([geom_text,geom2d, geom_workarea, geom_functionarea, obj3d[1]], basepoint, blockname, delete_input=True)
    #rs.InsertBlock(blockname, basepoint)
    
    
    



#call function
ac_furniture()
