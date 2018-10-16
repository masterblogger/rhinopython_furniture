
    #    Furniture, generates basic furniture,  by user input of width and depth (and height in some cases)
    #    Copyright (C) 2018 octobre  Joern Rettweiler
    #
    #    This program is free software: you can redistribute it and/or modify
    #    it under the terms of the GNU General Public License as published by
    #    the Free Software Foundation, either version 3 of the License, or
    #    (at your option) any later version.
    #
    #    This program is distributed in the hope that it will be useful,
    #    but WITHOUT ANY WARRANTY; without even the implied warranty of
    #    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    #    GNU General Public License for more details.
    #
    #    You should have received a copy of the GNU General Public License
    #    along with this program.  If not, see <https://www.gnu.org/licenses/>.

    #    Tested with Rhino 6 
    #
    #   Note: If you want to create a rhino command that you can call via command promt
    #   look here: https://developer.rhino3d.com/guides/rhinopython/creating-rhino-commands-using-python/
    #

import rhinoscriptsyntax as rs
import math

__commandname__ = "AC_Isolight"

# RunCommand is the called when the user enters the command name in Rhino.
# The command name is defined by the filname minus "_cmd.py"
def RunCommand( is_interactive ):
    #global
    
    
    
    
    
    ####################################
    #####BEGIN FUNCTION DECLARATION
    ####################################
    
    #not used .... 
    
        
    ####################################
    #####END FUNCTION DECLARATION
    ####################################
    
    crv_boundary = rs.GetCurveObject("Select ONE closed Curve, boundary your isolation! ")
    off_distance = rs.GetInteger("Enter thickness of isolation [mm]")
    
    offset_crv = rs.OffsetCurve(crv_boundary[0],  [0,0,0],off_distance)
    lines_boundary = rs.ExplodeCurves(crv_boundary[0],  delete_input=False)
    
    distance = off_distance *0.45
    div_crv_pts = rs.DivideCurveLength(crv_boundary[0], distance,  create_points=False, return_points=True)
    
    
    
    

    loopbreak = 0

        
        
        
    loop_stop = len(div_crv_pts) - 1
    
    
    base_lines = []
    supp_line_midpts = []
    base_line_midpts = []
    
    while loopbreak < loop_stop:
        first_pt = div_crv_pts[loopbreak]
        second = loopbreak + 1
        
        second_pt = div_crv_pts[second]
        #DEBUG print "second_pt", second_pt
        
        #add line between base curve
        base_line = rs.AddLine(first_pt, second_pt)
        
        base_lines.append(base_line)
        
        #calculate mid_pt
        
        mid_pt_x_diff = second_pt[0] - first_pt[0]
        mid_pt_x = mid_pt_x_diff / 2
        
        mid_pt_y_diff = second_pt[1] - first_pt[1]
        mid_pt_y = mid_pt_y_diff / 2
        mid_pt = rs.CreatePoint((first_pt[0]+second_pt[0])/2, (first_pt[1]+second_pt[1])/2 , 0 )
        
        #old maybe i delete this ...
        #perp_vector = (mid_pt_x - second_pt[1] + first_pt[1], mid_pt_y + second_pt[0] - first_pt[0])
        
        radiants = 1.1 #/ (math.pi *2 )
        
        vec_iso = rs.VectorCreate(first_pt, mid_pt)
        vec_iso_rot = rs.VectorRotate(vec_iso, radiants, [0,0,200])
        
        
        
        
        vec_correct_x = mid_pt_x + vec_iso_rot[0]
        vec_correct_y = mid_pt_y + vec_iso_rot[1] 
        vec_correct = rs.CreatePoint(vec_correct_x, vec_correct_y, 0)
        pt = rs.VectorAdd(vec_correct, mid_pt)
        
        
        
        supp_line = rs.AddLine(pt, mid_pt)
        suppline = rs.ExtendCurveLength(supp_line, 0, 0, (off_distance* 1.5))
        intersection_list = rs.CurveCurveIntersection(suppline, offset_crv)
        ##DEBUG print "intersection_list:" ,intersection_list
        ##DEBUG print "intersection_list:0" ,intersection_list[0]
        ##DEBUG print "intersection_list:0|1" ,intersection_list[0][1]
        
        intersection_pt = intersection_list[0][1]
        intersection_pt = rs.CreatePoint(intersection_pt)
        ##DEBUG rs.AddPoint(intersection_pt)
        rs.AddLine(intersection_pt, first_pt)
        rs.AddLine(intersection_pt, second_pt)
        
        #delete perpendicular support lines
        rs.DeleteObject(supp_line)
        #delete_abtract lines on first curve
        rs.DeleteObject(base_line)
        
        #rs.remove
        
        #rs.VectorAdd
        #rs.
        
        

        
        #rs.AddPoint(mid_pt)
        
        
        
        
        loopbreak = loopbreak + 1
    
    
    #print "div_crv_pts" ,div_crv_pts



    
    
    
    
  # you can optionally return a value from this function
  # to signify command result. Return values that make
  # sense are
  #   0 == success
  #   1 == cancel
  # If this function does not return a value, success is assumed
    return 0
RunCommand(True)
