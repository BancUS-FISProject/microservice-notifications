const axios = require("axios");

const BASE_URL = "http://127.0.0.1:8000/v1/notifications";

describe("Notifications API", () => {

  test("Login event creates notification", async () => {
    const payload = {
      userId: "123",
      type: "login",
      metadata: {}
    };

    const res = await axios.post(`${BASE_URL}/events`, payload);

    expect(res.status).toBe(201);
    expect(res.data.type).toBe("login");
    expect(res.data.message.toLowerCase()).toContain("inicio");
  });

  test("Invalid event type returns error", async () => {
    const payload = {
      userId: "123",
      type: "hackeo",
      metadata: {}
    };

    try {
      await axios.post(`${BASE_URL}/events`, payload);
    } catch (err) {
      expect(err.response.status).toBe(400);
    }
  });
});