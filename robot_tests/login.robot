*** Settings ****
Documentation                       A smoke test suite to check if the user can login to Pluto.
Library                             SeleniumLibrary     timeout=20 seconds
Test Teardown                       Close all browsers

*** Variables ***

${URL}                              https://pluto-dev.rnd.eficode.io/
${LOGIN_TEXT}                       Sign in to your account

*** Test Cases ***

Verify that user can login
    Open Browser                    ${URL}
    Wait until page contains        ${LOGIN_TEXT}