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

export function createRepositoryMutation(userUUID: string, name: string): string {
  return (`mutation {
    createRepository(userUuid: ${userUUID}, name: ${name})
    {
      success
      errors
    }
  }`);
}
