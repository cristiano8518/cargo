import http from "k6/http";
import { check, sleep } from "k6";

export const options = {
  vus: 10,
  duration: "30s",
  thresholds: {
    http_req_failed: ["rate<0.05"],
    http_req_duration: ["p(95)<1000"],
  },
};

const BASE_URL = __ENV.BASE_URL || "http://127.0.0.1:8000";

export default function () {
  const health = http.get(`${BASE_URL}/health/`);
  check(health, {
    "health status 200": (r) => r.status === 200,
  });

  const home = http.get(`${BASE_URL}/`);
  check(home, {
    "home status 200": (r) => r.status === 200,
  });

  const routes = http.get(`${BASE_URL}/cargo/routes/`);
  check(routes, {
    "routes status 200": (r) => r.status === 200,
  });

  const cargoTypes = http.get(`${BASE_URL}/api/cargo-types/`);
  check(cargoTypes, {
    "api cargo types status 200": (r) => r.status === 200,
  });

  sleep(1);
}
