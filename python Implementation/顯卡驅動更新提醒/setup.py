#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'HentaiSaru'

from cx_Freeze import setup, Executable
import sys

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(name='DriverDetection',
      version='1.0',
      description='update detection',
      options={"build_exe": {"includes": ["lxml.etree", "requests", "GPUtil", "re", "os", "tkinter.messagebox"]}},
      executables=[Executable("GPU_UpdateReminder.pyw", base=base ,icon="nvidia.ico")]
    )