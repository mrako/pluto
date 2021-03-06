*** Settings ****
Documentation                       A smoke test suite to check if the user can login to Pluto.
Library                             SeleniumLibrary     timeout=10 seconds
Test Teardown                       Close all browsers

*** Variables ***

${LOGIN_TEXT}                       Sign in to your account
${USERNAMEFIELDJS}                  dom:document.querySelector("#root > amplify-authenticator").shadowRoot.querySelector("div > slot > amplify-sign-in").shadowRoot.querySelector("#username")
${PWFIELDJS}                        dom:document.querySelector("#root > amplify-authenticator").shadowRoot.querySelector("div > slot > amplify-sign-in").shadowRoot.querySelector("#password")
${SIGNIN_BUTTON}                     dom:document.querySelector("#root > amplify-authenticator").shadowRoot.querySelector("div > slot > amplify-sign-in").shadowRoot.querySelector("amplify-form-section > form > amplify-section > section > div:nth-child(4) > div > slot > div > slot > amplify-button > button > span")
${SIGNOUT_BUTTON}                   //button[contains(.,'Logout')]

*** Test Cases ***

Verify that user can login
    Open Browser                    %{URL}      browser=gc
    Wait until element is visible               ${USERNAMEFIELDJS}
    Input text                      ${USERNAMEFIELDJS}      %{TEST_ACCOUNT_USERNAME}
    Wait until element is visible               ${PWFIELDJS}
    Input password                  ${PWFIELDJS}     %{TEST_ACCOUNT_PASSWORD}
    Wait until element is visible               ${SIGNIN_BUTTON}
    Click element                   ${SIGNIN_BUTTON}
    Wait until page contains        Create new project
    Wait until element is visible  ${SIGNOUT_BUTTON}
    Click element                   ${SIGNOUT_BUTTON}
    Sleep                           1 second
    Wait until element is visible               ${USERNAMEFIELDJS}

