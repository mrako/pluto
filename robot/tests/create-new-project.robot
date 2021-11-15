*** Settings ***

Library    String

Resource   ${CURDIR}/../resources/common.robot
Resource   ${CURDIR}/../resources/login-variables.robot

Test Setup          Open browser and go to homepage
Test Teardown       Close All Browsers

*** Test cases ***

Create a new project
  Verify login page is open
  Login                  ${ROBOT_USERNAME}    ${ROBOT_PASSWORD}
  Verify homepage is open
  Create project with random name


*** Keywords ***

Create project with random name
  ${PROJECT SUFFIX} =   Generate Random String  8
  Click Button    Create New Project
  Input Text      name         robot-test-project-${PROJECT SUFFIX}
  Input Text      repository   robot-test-project-${PROJECT SUFFIX}
  Input Text      githubToken   ${GITHUB_TOKEN}
  Click Button    id=create


