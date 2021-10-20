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
