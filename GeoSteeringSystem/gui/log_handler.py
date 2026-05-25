#!/usr/bin/python
# -*- coding:utf-8 -*-
import tkinter as tk
from datetime import datetime


class LogHandler:
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.delete(1.0, tk.END)
        self.text_widget.config(state=tk.DISABLED)

    def log(self, message):
        self.text_widget.config(state=tk.NORMAL)
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.text_widget.insert(tk.END, f"[{timestamp}] {message}\n")
        self.text_widget.see(tk.END)
        self.text_widget.config(state=tk.DISABLED)