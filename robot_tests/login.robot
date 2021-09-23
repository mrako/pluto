*** Settings ****
Documentation                       A smoke test suite to check if the user can login to Pluto.
...
...
...
Test Teardown                       Close all browsers

*** Variables ***

${URL}                              https://pluto-dev.rnd.eficode.io/
${LOGIN_TEXT}                       Sign in to your account

*** Keywords ***

Verify that user can login
    Open Browser                    ${URL}
    Wait until page contains        ${LOGIN_TEXT}