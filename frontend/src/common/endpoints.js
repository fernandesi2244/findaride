const apiEndpoint = "/api";
const authEndpoint = "/auth";

const endpoints = {
  login: `${authEndpoint}/login`,
  signup: `${authEndpoint}/signup`,
  isLoggedIn: `${authEndpoint}/is-logged-in`,
  activate: `${authEndpoint}/activate`,
};

export { endpoints };
