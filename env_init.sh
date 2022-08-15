#!/bin/bash
PYTHON_VIRTUAL_ENV_NAME=py_venv
PY_LAMBDA_FILE_NAME='lambda_function.py'

rm -rf ${PYTHON_VIRTUAL_ENV_NAME}

python -m pip install virtualenv
python -m venv ${PYTHON_VIRTUAL_ENV_NAME}
source ./${PYTHON_VIRTUAL_ENV_NAME}/bin/activate
pip install -r requirements.txt
