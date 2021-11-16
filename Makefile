.PHONY: dist

#DEFINE HERE THE PYTHON AND PIP VERSION (python/python3 or pip/pip3)
PYTHON = python
PIP = pip

check:
	@${PYTHON} --version || (echo "Python is not installed."; exit 1)


install: check
	 ${PYTHON} setup.py install


uninstall: check
	 ${PIP} uninstall sms-python-client


test: check	 
	${PYTHON} -m unittest discover tests


clean:
	rm -rf dist build
	rm -rf *.egg-info
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete


dist: check
	${PYTHON} setup.py sdist
	${PYTHON} setup.py bdist_wheel


install_dist: check
	${PIP} install dist/sms-python-client-0.9.tar.gz



	








