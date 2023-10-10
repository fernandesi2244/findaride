const apiEndpoint = "/api";
const authEndpoint = "/auth";

const endpoints = {
  login: `${authEndpoint}/login`,
  signup: `${authEndpoint}/signup`,
  isLoggedIn: `${authEndpoint}/is-logged-in`,
  activate: `${authEndpoint}/activate`,

  organizations: `${apiEndpoint}/organizations`,
  tags: `${apiEndpoint}/tags`,
  opportunities: `${apiEndpoint}/opportunities`
};

export { endpoints };
