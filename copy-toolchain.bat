@echo off
robocopy ..\VELGeoMaster\toolchain toolchain\ /MIR /XF secrets.py /XD .venv /NFL /NDL /NJH /nc /ns /np
