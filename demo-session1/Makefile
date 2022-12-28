SHELL := /bin/bash
VENV = ./venv
PIP = $(VENV)/bin/pip
PYTHON = $(VENV)/bin/python3

venv:
	@python3 -m venv $(VENV)

install: venv
	@source $(VENV)/bin/activate \
		$(PYTHON) -m pip install --upgrade pip &&\
			$(PIP) install --upgrade wheel &&\
				$(PIP) install --upgrade setuptools &&\
					$(PIP) install -r requirements.txt

clean:
	rm -rf __pycache__
	rm -rf $(VENV)

.PHONY: install clean