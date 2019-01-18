# coding: utf-8
""" Rescale a model between full scale and model scale
 Graham Knapp
 2019-01-18
 IronPython script for Rhino
"""
# Todo: error handling, scale côtes, ctrl-z
from __future__ import print_function, division

import rhinoscriptsyntax as rs

def Scale():
    # get current state and scale from DocumentData, if present or from user, if not
    print(rs.GetDocumentData("CSTB", "echelle"))
    print(rs.GetDocumentData("CSTB", "etat"))

    if rs.GetDocumentData("CSTB", "echelle") and rs.GetDocumentData("CSTB", "etat"):
        echelle = float(rs.GetDocumentData("CSTB", "echelle"))
        oldechelle = echelle
        etat = rs.GetDocumentData("CSTB", "etat")
        oldetat = etat
    else:
        etat = ""
        etat = rs.ListBox(("Vrai Grandeur", "Modele"),
                          "Actuellement a quelle echelle ?", "mise a echelle", etat)
        if etat == None:  # cancelled
            return
        oldetat = etat
        if etat == "Modele":
            echelle = 250.
            echelle = rs.GetReal("Échelle actuelle 1:", echelle, 0)
            oldechelle = echelle
            if echelle == None:  # cancelled
                return
        else:
            if etat == "Vrai Grandeur": echelle = 1.
    # get desired state and scale
    etat = rs.ListBox(("Vrai Grandeur", "Modele"),
                      "A échelle %s. Mettre a quelle echelle ?" % (etat), "Mise à échelle", etat)
    if etat == None:  # cancelled
        return

    if etat == "Modele":
        if not echelle: echelle = 250.
        echelle = rs.GetReal("Nouvelle Echelle 1:", echelle, 0)
        if echelle == None: return

    rs.SetDocumentData("CSTB", "echelle", str(echelle))
    rs.SetDocumentData("CSTB", "etat", etat)
    # scale geometry and dimensions
    dimstyles = rs.DimStyleNames()

    if not oldetat == etat:
        if etat == "Vrai Grandeur":
            rs.ScaleObjects(rs.AllObjects(), [0, 0, 0],
                            [(echelle), (echelle), (echelle)])
            for dimstyle in dimstyles:
                rs.Command('_-ScaleDimstyle "' + dimstyle + '" ' + str(echelle))

        else:
            rs.ScaleObjects(rs.AllObjects(), [0, 0, 0],
                            [(1 / echelle), (1 / echelle), (1 / echelle)])
            for dimstyle in dimstyles:
                rs.Command('_-ScaleDimstyle "' + dimstyle + '" ' + str(1 / echelle))

    else:
        if etat == "Modele":
            rs.ScaleObjects(rs.AllObjects(), [0, 0, 0], \
                            [(oldechelle / echelle), (oldechelle / echelle), (oldechelle / echelle)])
            for dimstyle in dimstyles:
                rs.Command('_-ScaleDimstyle "' + dimstyle + '" ' + str(oldechelle / echelle))

    rs.ZoomExtents(all=True)


if __name__ == "__main__":
    Scale()