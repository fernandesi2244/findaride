const apiEndpoint = "/api";
const authEndpoint = "/auth";

const endpoints = {
  login: `${authEndpoint}/login/`,
  signup: `${authEndpoint}/signup/`,
  isLoggedIn: `${authEndpoint}/is-logged-in/`,
  activate: `${authEndpoint}/activate/`,
  me: `${authEndpoint}/me/`,

  trip: `${apiEndpoint}/trip/`,
  userTrips: `${apiEndpoint}/user-trips/`,
  deleteTripRequest: `${apiEndpoint}/delete-trip-request/`,
  joinRequests: `${apiEndpoint}/join-requests/`,
  joinSelectedTrips: `${apiEndpoint}/join-selected-trips/`,
  tripList: `${apiEndpoint}/trip-list/`,
};

export { endpoints };
