
all: create

create:
	zip function.zip test_function.py
	aws lambda create-function --function-name place-test \
	--zip-file fileb://function.zip --handler test_function.handler --runtime python3.8 \
	--role arn:aws:iam::786929956471:role/daniel-lambda \
	--timeout 60 --memory-size 256

update:
	zip function.zip test_function.py
	aws lambda update-function-code --function-name place-test --zip-file fileb://function.zip

config:
	aws lambda update-function-configuration --function-name place-test --timeout 60 --memory-size 2048

invoke:
	aws lambda invoke --function-name place-test --payload '{}' response.json --log-type Tail

delete:
	aws lambda delete-function --function-name place-test
