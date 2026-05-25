#!/usr/bin/python
# -*- coding:utf-8 -*-
from agents.base_agent import BaseAgent
from core.trajectory import min_curvature
from core.thickness import compute_all_thicknesses

class CalculationAgent(BaseAgent):
    def execute(self, context):
        survey = context["survey"]
        formations = context["formations"]
        traj = min_curvature(survey)
        thickness = compute_all_thicknesses(traj, formations)
        context["trajectory"] = traj
        context["thickness"] = thickness
        context["calc_status"] = "完成"
        return context