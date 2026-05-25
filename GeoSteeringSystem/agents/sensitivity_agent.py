#!/usr/bin/python
# -*- coding:utf-8 -*-
from copy import deepcopy
from agents.base_agent import BaseAgent
from core.models import SurveyPoint
from core.trajectory import min_curvature
from core.thickness import compute_all_thicknesses

class SensitivityAgent(BaseAgent):
    def execute(self, context):
        delta = context.get("sensitivity_delta", 5)
        original_survey = context["survey"]
        modified_survey = []
        for pt in original_survey:
            modified_survey.append(SurveyPoint(pt.md, pt.incl + delta, pt.azi))
        formations = context["formations"]
        traj_sens = min_curvature(modified_survey)
        thick_sens = compute_all_thicknesses(traj_sens, formations)
        context["trajectory_sensitivity"] = traj_sens
        context["thickness_sensitivity"] = thick_sens
        context["sens_status"] = "完成"
        return context