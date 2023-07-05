@echo off
pushd %~dp0

python3 ./MakeTable.py

popd
if "%1"=="" pause