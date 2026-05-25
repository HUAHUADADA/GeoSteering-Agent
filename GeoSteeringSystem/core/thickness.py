#!/usr/bin/python
# -*- coding:utf-8 -*-
import numpy as np
from core.models import FormationLayer
from core.trajectory import interpolate_trajectory_at_md

def formation_normal(dip, dip_azimuth):
    dip_rad = np.radians(dip)
    azi_rad = np.radians(dip_azimuth)
    nx = np.sin(dip_rad) * np.sin(azi_rad)
    ny = np.sin(dip_rad) * np.cos(azi_rad)
    nz = np.cos(dip_rad)
    norm = np.sqrt(nx*nx + ny*ny + nz*nz)
    return np.array([nx, ny, nz]) / norm

def true_thickness(top_pt, base_pt, layer):
    delta = np.array([base_pt.x - top_pt.x, base_pt.y - top_pt.y, base_pt.z - top_pt.z])
    normal = formation_normal(layer.dip, layer.dip_azimuth)
    return abs(np.dot(delta, normal))

def compute_all_thicknesses(trajectory, layers):
    results = []
    for layer in layers:
        if layer.top_md >= layer.base_md:
            continue
        top_pt = interpolate_trajectory_at_md(trajectory, layer.top_md)
        base_pt = interpolate_trajectory_at_md(trajectory, layer.base_md)
        apparent = layer.base_md - layer.top_md
        true_thick = true_thickness(top_pt, base_pt, layer)
        results.append({
            "地层名称": layer.name,
            "真厚度(米)": round(true_thick, 2),
            "视厚度(米)": round(apparent, 2)
        })
    return results