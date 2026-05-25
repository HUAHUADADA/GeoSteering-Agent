#!/usr/bin/python
# -*- coding:utf-8 -*-
class SurveyPoint:
    def __init__(self, md, incl, azi):
        self.md = md
        self.incl = incl
        self.azi = azi

class TrajectoryPoint:
    def __init__(self, md, x, y, z, incl, azi):
        self.md = md
        self.x = x
        self.y = y
        self.z = z
        self.incl = incl
        self.azi = azi

class FormationLayer:
    def __init__(self, name, top_md, base_md, dip, dip_azimuth):
        self.name = name
        self.top_md = top_md
        self.base_md = base_md
        self.dip = dip
        self.dip_azimuth = dip_azimuth