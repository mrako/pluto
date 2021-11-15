*** Variables ***

${VALID EMAIL}                    marko.klemetti@eficode.com
${VALID PASSWORD}                 vka@reb8MJZ*pcf8fyc

${LOGIN FIELD USERNAME}           dom:document.querySelector("#root > amplify-authenticator").shadowRoot.querySelector("div > slot > amplify-sign-in").shadowRoot.querySelector("#username")
${LOGIN FIELD PASSWORD}           dom:document.querySelector("#root > amplify-authenticator").shadowRoot.querySelector("div > slot > amplify-sign-in").shadowRoot.querySelector("#password")
${LOGIN BUTTON SIGNIN}            dom:document.querySelector("#root > amplify-authenticator").shadowRoot.querySelector("div > slot > amplify-sign-in").shadowRoot.querySelector("amplify-form-section > form > amplify-section > section > div:nth-child(4) > div > slot > div > slot > amplify-button > button > span")
${BUTTON SIGNOUT}                 //button[contains(.,'Logout')]


*** Keywords ***

Login
  [Arguments]     ${email}    ${password}
  Input Text      ${LOGIN FIELD USERNAME}    ${email}
  Input Text      ${LOGIN FIELD PASSWORD}    ${password}
  Click Element   ${LOGIN BUTTON SIGNIN}

Verify login page is open
  Location should be               ${SERVER}/login
  Wait Until Element Is Visible    ${LOGIN FIELD USERNAME}
