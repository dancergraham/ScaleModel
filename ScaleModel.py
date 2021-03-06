# coding: utf-8
""" Rescale a Rhino model between full scale and model scale

 Graham Knapp
 2019-08-30
 IronPython script for Rhino v5
"""
# Todo: error handling
from __future__ import print_function, division, absolute_import

import rhinoscriptsyntax as rs
import scriptcontext as sc

def __undo_usertext(sender, e):
    """custom undo event - may be removed if bug in Rhino is fixed"""
    actuel = (rs.GetDocumentData("ScaleModel", "scale"),
                rs.GetDocumentData("ScaleModel", "state"))
    e.Document.AddCustomUndoEvent("Undo ScaleModel", __undo_usertext, actuel)
    old = e.Tag
    print(old)
    print ("returning to %s scale" % (old[1]))
    rs.SetDocumentData("ScaleModel","scale",old[0])
    rs.SetDocumentData("ScaleModel","state",old[1])
    rs.ZoomExtents()

def rescale():
    # get current state and scale from DocumentData, if present or from user, if not
    print("Current Scale: 1:", rs.GetDocumentData("ScaleModel", "scale"))
    print("Current State: ", rs.GetDocumentData("ScaleModel", "state"))

    if rs.GetDocumentData("ScaleModel", "scale") and rs.GetDocumentData("ScaleModel", "state"):
        scale = float(rs.GetDocumentData("ScaleModel", "scale"))
        oldechelle = scale
        state = rs.GetDocumentData("ScaleModel", "state")
        oldetat = state
    else:
        state = ""
        state = rs.ListBox(items=("Full-Scale", "Model Scale"),
                           message="Currently at what scale ?",
                           title="Scale Model",
                           default=state)
        if state is None:  # cancelled
            return
        oldetat = state
        if state == "Model Scale":
            scale = 250.
            scale = rs.GetReal("Current Scale 1:", scale, 0)
            oldechelle = scale
            if scale is None:  # cancelled
                return
        else:
            if state == "Full-Scale":
                scale = 1.
    previous_params = (str(scale), state)
    # get desired state and scale
    state = rs.ListBox(("Full-Scale", "Model Scale"),
                       "Currently %s. Choose new state" % (state), "Rescale", state)
    if state == None:  # cancelled
        return

    if state == "Model Scale":
        if not scale: scale = 250.
        scale = rs.GetReal("New Scale 1:", scale, 0)
        if scale == None: return

    rs.SetDocumentData("ScaleModel", "scale", str(scale))
    rs.SetDocumentData("ScaleModel", "state", state)

    # scale geometry and dimensions
    dimstyles = rs.DimStyleNames()

    rs.EnableRedraw(False)

    if not oldetat == state:
        if state == "Full-Scale":
            rs.ScaleObjects(rs.AllObjects(), [0, 0, 0],
                            [(scale), (scale), (scale)])
            for dimstyle in dimstyles:
                rs.Command('_-ScaleDimstyle "' + dimstyle + '" ' + str(scale))

        else:
            rs.ScaleObjects(rs.AllObjects(), [0, 0, 0],
                            [(1 / scale), (1 / scale), (1 / scale)])
            for dimstyle in dimstyles:
                rs.Command('_-ScaleDimstyle "' + dimstyle + '" ' + str(1 / scale))

    else:
        if state == "Model Scale":
            rs.ScaleObjects(rs.AllObjects(), [0, 0, 0], \
                            [(oldechelle / scale), (oldechelle / scale), (oldechelle / scale)])
            for dimstyle in dimstyles:
                rs.Command('_-ScaleDimstyle "' + dimstyle + '" ' + str(oldechelle / scale))
    sc.doc.AddCustomUndoEvent("Undo ScaleModel", __undo_usertext, previous_params)
    print("New Scale: 1:", rs.GetDocumentData("ScaleModel", "scale"))
    print("New State: ", rs.GetDocumentData("ScaleModel", "state"))
    rs.EnableRedraw(True)

    rs.ZoomExtents(all=True)


if __name__ == "__main__":
    rescale()
