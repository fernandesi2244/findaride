const apiEndpoint = "/api";
const authEndpoint = "/auth";

const endpoints = {
  login: `${authEndpoint}/login/`,
  signup: `${authEndpoint}/signup/`,
  isLoggedIn: `${authEndpoint}/is-logged-in/`,
  activate: `${authEndpoint}/activate/`,
  me: `${authEndpoint}/me/`,

  trip: `${apiEndpoint}/trip/`,
  tripRequest: `${apiEndpoint}/trip-request/`,
  userTrips: `${apiEndpoint}/user-trips/`,
  deleteTripRequest: `${apiEndpoint}/delete-trip-request/`,
  joinRequests: `${apiEndpoint}/join-requests/`,
};

export { endpoints };
