#!/bin/bash
PYTHON_VIRTUAL_ENV_NAME=py_venv
PY_LAMBDA_DEPENDENCIES=py_lambda_dependencies
PY_LAMBDA_ZIP_NAME='py_lambda_package.zip'
PY_LAMBDA_FILE_NAME='lambda_function.py'

rm -rf ${PYTHON_VIRTUAL_ENV_NAME} ${PY_LAMBDA_DEPENDENCIES} ${PY_LAMBDA_ZIP_NAME}

python -m pip install virtualenv
python -m venv ${PYTHON_VIRTUAL_ENV_NAME}
source ./${PYTHON_VIRTUAL_ENV_NAME}/bin/activate
pip install -r requirements.txt
mkdir -p $PY_LAMBDA_DEPENDENCIES/python
#cp -r ./${PYTHON_VIRTUAL_ENV_NAME}/lib/*/site-packages/* ./${PY_LAMBDA_DEPENDENCIES}
cp -r ./${PYTHON_VIRTUAL_ENV_NAME}/* ./${PY_LAMBDA_DEPENDENCIES}/python

zip -r ${PY_LAMBDA_ZIP_NAME} ./${PY_LAMBDA_DEPENDENCIES}/.
zip -g ${PY_LAMBDA_ZIP_NAME} ${PY_LAMBDA_FILE_NAME}
