# Asume gcloud SDK already logged in

all: create

deploy:
	cd test_function && gcloud functions deploy place-test --entry-point main --memory 2048MB --runtime python37 --trigger-http --allow-unauthenticated

logs:
	gcloud functions logs read place-test

describe:
	gcloud functions describe place-test