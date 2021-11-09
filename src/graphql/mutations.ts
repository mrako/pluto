export function createProjectMutation(name: string, description:string):string {
  return (`mutation {
    createProject(name: "${name}", description: "${description}") 
      {
        success 
        errors 
        project 
        { 
          name 
          description
          uuid
        }
      }
    }`
  );
}

export function bindUserToProjectMutation(installationId: string, plutoUserUUID: string, code: string): string {
  return (`mutation {
    bindPlutoUser(installationId: "${installationId}", plutoUserUUID: "${plutoUserUUID}", code: "${code}")
    {
      success
      errors
      userAccount { username }
      projectUser { username }
      organisation { name }
    }
  }`);
}

export function createRepositoryMutation(name: string, projectUUID: string, githubToken: string): string {
  return (`mutation {
    createRepository(name: "${name}", description: "", projectUuid: "${projectUUID}" github_auth_token: "${githubToken}")
    {
      success
      errors
    }
  }`);
}
