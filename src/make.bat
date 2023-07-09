@echo off
pushd %~dp0

python3 ./Main.py

popd
if "%1"=="" pause