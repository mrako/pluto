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

export function bindUserToProjectMutation(installationId: string, plutoUserUUID: string): string {
  return (`mutation {
    bindPlutoUser(installationId: "${installationId}", plutoUserUUID: "${plutoUserUUID}")
    {
      success
      errors
      userAccount { username }
      projectUser { username }
      organisation { name }
    }
  }`);
}
