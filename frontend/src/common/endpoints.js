const apiEndpoint = "/api";
const authEndpoint = "/auth";

const endpoints = {
  login: `${authEndpoint}/login/`,
  signup: `${authEndpoint}/signup/`,
  isLoggedIn: `${authEndpoint}/is-logged-in/`,
  activate: `${authEndpoint}/activate/`,
  me: `${authEndpoint}/me/`,

  tripRequest: `${apiEndpoint}/trip-request/`,
  userTrips: `${apiEndpoint}/user-trips/`,
  deleteTripRequest: `${apiEndpoint}/delete-trip-request/`,
  confirmationRequests: `${apiEndpoint}/confirmation-requests/`,
  joinRequests: `${apiEndpoint}/join-requests/`,
};

export { endpoints };
