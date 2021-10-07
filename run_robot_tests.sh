# Create reports folder
sudo mkdir reports && sudo chmod 777 reports

docker run --shm-size=1g \
  -e ROBOT_THREADS=1 \
  -e PABOT_OPTIONS="" \
  -e ROBOT_OPTIONS="" \
  -e BROWSER=chrome \
  -e TEST_ACCOUNT_PASSWORD=$TEST_ACCOUNT_PASSWORD \
  -e TEST_ACCOUNT_USERNAME=$TEST_ACCOUNT_USERNAME \
  -e URL=$URL \
  -v $(pwd)/reports:/opt/robotframework/reports:Z \
  -v $(pwd)/robot_tests:/opt/robotframework/tests:Z \
  --user $(id -u):$(id -g) \
  ppodgorsek/robot-framework:latest
