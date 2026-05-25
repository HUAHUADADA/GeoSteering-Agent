#!/usr/bin/python
# -*- coding:utf-8 -*-
from agents.base_agent import BaseAgent
from datetime import datetime

class ReportAgent(BaseAgent):
    def execute(self, context):
        original = context["thickness"]
        sensitivity = context.get("thickness_sensitivity", [])
        delta = context.get("sensitivity_delta", 5)
        report_lines = []
        report_lines.append("=== 多Agent地质导向分析报告 ===")
        report_lines.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append("\n【原始地层真厚度】")
        for r in original:
            report_lines.append(f"  {r['地层名称']}: {r['真厚度(米)']} 米")
        if sensitivity:
            report_lines.append(f"\n【敏感性分析】（井斜角增加 {delta}°）")
            for r in sensitivity:
                report_lines.append(f"  {r['地层名称']}: {r['真厚度(米)']} 米")
            report_lines.append("\n【智能解读】")
            report_lines.append("  井斜角增加导致井轨迹更陡，穿过地层的真厚度略微减小。")
            report_lines.append("  建议在实钻中控制井斜角在25-30度范围内以保持地层对比准确性。")
        else:
            report_lines.append("\n【提示】未进行敏感性分析，可调整参数后重新运行。")
        context["report"] = "\n".join(report_lines)
        context["report_status"] = "完成"
        return context