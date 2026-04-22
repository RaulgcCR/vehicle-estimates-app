import api from "./api";

export function setupInterceptors(logout: () => void) {
  api.interceptors.response.use(
    (response) => response,
    (error) => {
      if (error.response?.status === 401) {
        logout();
        window.location.href = "/login";
      }

      return Promise.reject(error);
    }
  );
}