#!/usr/bin/python
# -*- coding:utf-8 -*-
from agents.calc_agent import CalculationAgent
from agents.sensitivity_agent import SensitivityAgent
from agents.report_agent import ReportAgent


class Orchestrator:
    def __init__(self):
        self.calc_agent = CalculationAgent()
        self.sens_agent = SensitivityAgent()
        self.report_agent = ReportAgent()

    def run_pipeline(self, survey, formations, do_sensitivity=True, delta=5):
        context = {
            "survey": survey,
            "formations": formations,
            "sensitivity_delta": delta
        }
        context = self.calc_agent.execute(context)
        if do_sensitivity:
            context = self.sens_agent.execute(context)
        context = self.report_agent.execute(context)
        return context