# Generates simply 2d rectangular furniture elments
# 
# GNU GENERAL PUBLIC LICENSE Version 3
#
# by Joern Rettweiler, 2018 august 12
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
    
    #default : workarea Color blue = [0,255,255]
    layer_workarea = ("AC-Working_area")
    layer_workarea_color = [0,255,255]
    
    #default : Text Color blue = [0,0,0]
    layer_text = ("AC-Text")
    layer_text_color = [0,0,0]
    
    
    #############################
    ##FUNCTION DEFINITIONS BEGIN##
    ##############################
    
    
    
    
    
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
        + str(width)+ " x " + str(depth) + "\n" 
        + "newline")
        
        
        #rs.AddPoint(geom2d_centroid[0])
        geom_text = rs.AddTextDot(textdottext, geom2d_centroid[0])
        #rhino.text
        #Generate Blockname
        blockname = (str(furniture_name) + str(width) + "x" + str(depth))
        
        
        
        
    def ac_geom2d_workarea(width):
        global geom_workarea
        
        planexy_wa = rs.WorldXYPlane()
        
        
        # Reference (2018 august 08) https://www.baua.de/DE/Angebote/Rechtstexte-und-Technische-Regeln/Regelwerk/ASR/pdf/ASR-A1-2.pdf?__blob=publicationFile&v=7
        depth_workarea = -1000
        rs.CurrentLayer(layer_workarea)
        geom_workarea = rs.AddRectangle(planexy_wa, width, depth_workarea)
    #############################
    ##FUNCTION DEFINITIONS END###
    #############################
    
    
    
    print("hello")
    
    #filling cabinet = aktenschrank, shelf=regal
    
    furniture_typ = rs.GetInteger("1=filling cabinet 2=Shelf 3=sideboard 4=table, 5=desk", 5, 0, 5 )
    print furniture_typ
    
    #Get Furniture Dimensions and Scale them to mm
    furniture_width = rs.GetReal("Width of furniture [cm]", 80, 0)
    furniture_width = furniture_width * 10
    furniture_depth = rs.GetReal("Depth of furniture [cm]", 42, 0)
    furniture_depth = furniture_depth * 10
    
    print ("width")
    print furniture_width
    print furniture_depth
    
    if bool(furniture_typ) != 1 or 2 or 3:
        
        furniture_hight = rs.GetReal("Hight of furniture [cm]", 80, 0)
    else:
        print("noPenis")
        furniture_hight = 80


    #Add text to textvariable
    if furniture_typ == 1:
        furniture_name = "filling cabinet"
    
    elif furniture_typ == 2:
        furniture_name = "Shelf"
        
    
    elif furniture_typ == 3:
        furniture_name = "Sideboard"
        
    
    elif furniture_typ == 4:
        furniture_name = "Table"
        
    
    elif furniture_typ == 5:
        furniture_name = "Desk"
        
        rs.AddLayer(layer_text, layer_text_color, parent=layer_furniture)
        ac_geom2d_workarea(furniture_width)
    #elif furniture_typ == 3:
    #    furniture_name = "XXX"
    
    
    print furniture_name





    #Add layer after previous operation are succesfull
    rs.AddLayer(layer_furniture, layer_furniture_color)
    rs.AddLayer(layer_geom2d, layer_geom2d_color, parent=layer_furniture)
    rs.AddLayer(layer_geom3d, layer_geom3d_color, parent=layer_furniture)
    rs.AddLayer(layer_workarea, layer_workarea_color, parent=layer_furniture)
    rs.AddLayer(layer_text, layer_text_color, parent=layer_furniture)
    rs.LayerLinetype(layer_text, linetype="Dashed")
    
    
    
    rs.CurrentLayer(layer=layer_geom2d)
    ac_geom2d(furniture_width, furniture_depth)
    
    rs.AddBlock([geom_text,geom2d,geom_workarea], basepoint, blockname, delete_input=True)
    rs.InsertBlock(blockname, basepoint)
    




#call function
ac_furniture()