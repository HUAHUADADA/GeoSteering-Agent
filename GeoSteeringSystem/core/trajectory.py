#!/usr/bin/python
# -*- coding:utf-8 -*-
import numpy as np
from core.models import TrajectoryPoint

def min_curvature(survey_points, start_n=0.0, start_e=0.0, start_z=0.0):
    if len(survey_points) < 1:
        return []
    traj = []
    prev = TrajectoryPoint(
        md=survey_points[0].md,
        x=start_n, y=start_e, z=start_z,
        incl=survey_points[0].incl, azi=survey_points[0].azi
    )
    traj.append(prev)
    for i in range(1, len(survey_points)):
        cur = survey_points[i]
        d_md = cur.md - prev.md
        if d_md == 0:
            continue
        inc1 = np.radians(prev.incl)
        inc2 = np.radians(cur.incl)
        azi1 = np.radians(prev.azi)
        azi2 = np.radians(cur.azi)
        vec1 = np.array([np.sin(inc1)*np.cos(azi1), np.sin(inc1)*np.sin(azi1), np.cos(inc1)])
        vec2 = np.array([np.sin(inc2)*np.cos(azi2), np.sin(inc2)*np.sin(azi2), np.cos(inc2)])
        dot = np.clip(np.dot(vec1, vec2), -1.0, 1.0)
        beta = np.arccos(dot)
        if beta < 1e-6:
            rf = 1.0
        else:
            rf = 2.0 / beta * np.tan(beta/2.0)
        delta = d_md * rf * (vec1 + vec2) / 2.0
        new_n = prev.x + delta[0]
        new_e = prev.y + delta[1]
        new_z = prev.z + delta[2]
        new_pt = TrajectoryPoint(
            md=cur.md, x=new_n, y=new_e, z=new_z,
            incl=cur.incl, azi=cur.azi
        )
        traj.append(new_pt)
        prev = new_pt
    return traj

def interpolate_trajectory_at_md(trajectory, target_md):
    if target_md <= trajectory[0].md:
        return trajectory[0]
    if target_md >= trajectory[-1].md:
        return trajectory[-1]
    for i in range(1, len(trajectory)):
        if trajectory[i].md >= target_md:
            p0 = trajectory[i-1]
            p1 = trajectory[i]
            ratio = (target_md - p0.md) / (p1.md - p0.md)
            x = p0.x + ratio * (p1.x - p0.x)
            y = p0.y + ratio * (p1.y - p0.y)
            z = p0.z + ratio * (p1.z - p0.z)
            incl = p0.incl + ratio * (p1.incl - p0.incl)
            azi = p0.azi + ratio * (p1.azi - p0.azi)
            return TrajectoryPoint(md=target_md, x=x, y=y, z=z, incl=incl, azi=azi)
    return trajectory[-1]