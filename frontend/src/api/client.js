import axios from "axios";

export const api = axios.create({
  baseURL: "http://localhost:8000/api",
});

export async function getJson(url, token, config = {}) {
  const response = await api.get(url, {
    ...config,
    headers: {
      Authorization: token ? `Token ${token}` : "",
      ...(config.headers || {}),
    },
  });
  return response.data;
}

export async function downloadExcel(url, token, filename = "ventas.xlsx") {
  const response = await api.get(url, {
    responseType: "blob",
    headers: {
      Authorization: token ? `Token ${token}` : "",
    },
  });

  const blob = new Blob([response.data], {
    type: response.headers["content-type"],
  });

  const anchor = document.createElement("a");
  anchor.href = window.URL.createObjectURL(blob);
  anchor.download = filename;
  anchor.click();
  window.URL.revokeObjectURL(anchor.href);
}
