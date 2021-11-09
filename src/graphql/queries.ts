export function getProjectsQuery(): string { return 'query { projects { success errors projects { name description uuid }}}'; }

export function getProjectByUUIDQuery(uuid:string): string { return `query { project(projectUuid: "${uuid}") { success errors project { name description uuid }}}`; }

export function getUserLinksQuery(): string { return 'query { userLinks { success errors links { uuid organisation { name } projectUser { username } } } }'; }
