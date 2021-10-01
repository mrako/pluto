# Create reports folder
sudo mkdir reports && sudo chmod 777 reports

docker run --shm-size=1g \
  -e ROBOT_THREADS=1 \
  -e PABOT_OPTIONS="" \
  -e ROBOT_OPTIONS="" \
  -e BROWSER=chrome \
  -e TEST_SECRET=$TEST_SECRET \
  -v reports:/opt/robotframework/reports:Z \
  -v robot_tests:/opt/robotframework/tests:Z \
  --user $(id -u):$(id -g) \
  ppodgorsek/robot-framework:latest