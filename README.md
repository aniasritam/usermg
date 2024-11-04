Steps to setup this repo :
Install docker 
Install LocalStack from https://docs.localstack.cloud/getting-started/installation/ , unzip the file and run the exe file in powershell
Open Docker Desktop
Run the following command to start localstack - "  docker run -d -p 4566:4566 -e SERVICES=dynamodb localstack/localstack "
Run the following command to create a dynamodb table - " aws dynamodb create-table --table-name User --attribute-definitions AttributeName=email,AttributeType=S --key-schema AttributeName=email,KeyType=HASH --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 --endpoint-url http://localhost:4566 "
Clone the repo
run the command to start the application - " uvicorn app.main:app --reload"
