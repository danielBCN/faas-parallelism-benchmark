# Asume ibmcloud CLI already logged in and target resource group configured.
# Also, function namespace selected for the fn plugin.

all: create

create:
	ibmcloud fn action create place-test test_function.py

update:
	ibmcloud fn action update place-test test_function.py

invoke:
	ibmcloud fn action invoke place-test --result
