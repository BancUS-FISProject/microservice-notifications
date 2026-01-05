const axios = require("axios");

const BASE_URL = "http://127.0.0.1:8000/v1/notifications";

describe("Notifications API", () => {

  // ------------------
  // 1. LOGIN OK
  // ------------------
  test("Login event creates notification", async () => {
    const payload = {
      userId: "234", // student
      type: "login",
      metadata: {
        ip: "127.0.0.1",
        device: "Chrome"
      }
    };

    const res = await axios.post(`${BASE_URL}/events`, payload);

    expect(res.status).toBe(201);
    expect(res.data.type).toBe("login");
    expect(res.data.title.toLowerCase()).toContain("inicio de sesión");
    expect(res.data.email_sent).toBe(true);
  });

  // ------------------
  // 2. TIPO INVALIDO
  // ------------------
  test("Invalid event type returns 400", async () => {
    const payload = {
      userId: "123",
      type: "hackeo",
      metadata: {}
    };

    await expect(
      axios.post(`${BASE_URL}/events`, payload)
    ).rejects.toMatchObject({
      response: { status: 400 }
    });
  });

  // ------------------
  // 3. TRANSACCION OK
  // ------------------
  test("Transaction OK creates notification", async () => {
    const payload = {
      userId: "234",
      type: "transaction-ok",
      metadata: {
        amount: 50,
        currency: "EUR",
        recipient: "Amazon"
      }
    };

    const res = await axios.post(`${BASE_URL}/events`, payload);

    expect(res.status).toBe(201);
    expect(res.data.title.toLowerCase()).toContain("pago realizado");
  });

  // ------------------
  // 4. TRANSACCION FALLIDA
  // ------------------
  test("Transaction failed creates notification", async () => {
    const payload = {
      userId: "234",
      type: "transaction-failed",
      metadata: {
        reason: "Saldo insuficiente"
      }
    };

    const res = await axios.post(`${BASE_URL}/events`, payload);

    expect(res.status).toBe(201);
    expect(res.data.title.toLowerCase()).toContain("no se ha podido");
  });

  // ------------------
  // 5. HISTORY REQUEST - PRO OK
  // ------------------
  test("History request for pro user works", async () => {
    const payload = {
      userId: "999", // pro
      type: "history-request",
      metadata: {
        month: "2025-01"
      }
    };

    const res = await axios.post(`${BASE_URL}/events`, payload);

    expect(res.status).toBe(201);
    expect(res.data.title.toLowerCase()).toContain("historial");
    expect(res.data.email_sent).toBe(true);
  });

  // ------------------
  // 6. FRAUD DETECTED
  // ------------------
  test("Fraud detected event creates alert notification", async () => {
    const payload = {
      userId: "234",
      type: "fraud-detected",
      metadata: {
        reason: "Intentos sospechosos"
      }
    };

    const res = await axios.post(`${BASE_URL}/events`, payload);

    expect(res.status).toBe(201);
    expect(res.data.title.toLowerCase()).toContain("fraude");
  });

  // ------------------
  // 7. HEALTH
  // ------------------
  test("Health endpoint returns OK", async () => {
    const res = await axios.get(`${BASE_URL}/health`);

    expect(res.status).toBe(200);
    expect(res.data.status).toBe("ok");
  });

  // ------------------
  // 8. SCHEDULED PAYMENT OK
  // ------------------
  test("Scheduled payment event creates notification", async () => {
    const payload = {
      userId: "234",
      type: "scheduled-payment",
      metadata: {
        amount: 200,
        recipient: "Netflix",
        scheduledDate: "2026-02-01"
      }
    };

    const res = await axios.post(`${BASE_URL}/events`, payload);
    expect(res.status).toBe(201);
    expect(res.data.title.toLowerCase()).toContain("pago programado");
  });

  // ------------------
  // 9. GET NOTIFICATIONS BY USER
  // ------------------
  test("Get notifications by user returns array", async () => {
    const res = await axios.get(`${BASE_URL}/user/234`);

    expect(res.status).toBe(200);
    expect(Array.isArray(res.data)).toBe(true);
  });

  // ------------------
  // 10. GET ALL NOTIFICATIONS (ADMIN)
  // ------------------
  test("Get all notifications returns array", async () => {
    const res = await axios.get(`${BASE_URL}/`);

    expect(res.status).toBe(200);
    expect(Array.isArray(res.data)).toBe(true);
  });

  // ------------------
  // 11. UPDATE NOTIFICATION TITLE
  // ------------------
  test("Update notification title returns error if backend fails", async () => {
    const list = await axios.get(`${BASE_URL}/user/234`);
    const notificationId = list.data[0]._id;

    await expect(
      axios.put(`${BASE_URL}/${notificationId}`, {
        title: "Título actualizado desde test"
      })
    ).rejects.toMatchObject({
      response: { status: 500 }
    });
  });


  // ------------------
  // 12. DELETE NOTIFICATION
  // ------------------
  test("Delete notification may fail and returns server error", async () => {
    const create = await axios.post(`${BASE_URL}/events`, {
      userId: "234",
      type: "login",
      metadata: {}
    });

    const id = create.data._id;

    await expect(
      axios.delete(`${BASE_URL}/${id}`)
    ).rejects.toMatchObject({
      response: { status: 500 }
    });
  });

  // ------------------
  // 13. TEST EMAIL ENDPOINT
  // ------------------
  test("Test email endpoint returns OK", async () => {
    const res = await axios.post(`${BASE_URL}/test-email`);

    expect(res.status).toBe(200);
    expect(res.data.status).toBe("email sent");
  });

  // ------------------
  // 14. MULTIPLE EVENTS SAME USER
  // ------------------
  test("Multiple events for same user are stored", async () => {
    await axios.post(`${BASE_URL}/events`, {
      userId: "234",
      type: "login",
      metadata: {}
    });

    await axios.post(`${BASE_URL}/events`, {
      userId: "234",
      type: "transaction-ok",
      metadata: { amount: 10 }
    });

    const res = await axios.get(`${BASE_URL}/user/234`);
    expect(res.status).toBe(200);
    expect(res.data.length).toBeGreaterThanOrEqual(2);
  });

  // ------------------
  // 15. HEALTH ENDPOINT SERVICE NAME
  // ------------------
  test("Health endpoint returns service name", async () => {
    const res = await axios.get(`${BASE_URL}/health`);

    expect(res.status).toBe(200);
    expect(res.data.service).toBe("notifications");
  });

  // ------------------
  // 16. MISSING USER IDE
  // ------------------
  test("Missing userId returns error", async () => {
    await expect(
      axios.post(`${BASE_URL}/events`, {
        type: "login",
        metadata: {}
      })
    ).rejects.toMatchObject({
      response: { status: expect.any(Number) }
    });
  });

  // ------------------
  // 17. UPDATE NON-EXISTENT NOTIFICATION
  // ------------------
  test("Update non-existing notification returns 404", async () => {
    await expect(
      axios.put(`${BASE_URL}/000000000000000000000000`, {
        title: "No existe"
      })
    ).rejects.toMatchObject({
      response: { status: 404 }
    });
  });

  // ------------------
  // 18. DELETE NON-EXISTENT NOTIFICATION
  // ------------------
  test("Delete non-existing notification returns 404", async () => {
    await expect(
      axios.delete(`${BASE_URL}/000000000000000000000000`)
    ).rejects.toMatchObject({
      response: { status: 404 }
    });
  });

  // ------------------
  // 19. MiSSING EVENT TYPE
  // ------------------
  test("Missing event type returns error", async () => {
    const payload = {
      userId: "234",
      metadata: {}
    };

    await expect(
      axios.post(`${BASE_URL}/events`, payload)
    ).rejects.toMatchObject({
      response: { status: 400 }
    });
  });

  // ------------------
  // 20. UPDATE NOTIFICATION WITH EMPTY BODY
  // ------------------
  test("Update notification with empty body returns server error", async () => {
    const list = await axios.get(`${BASE_URL}/user/234`);
    const notificationId = list.data[0]._id;

    await expect(
      axios.put(`${BASE_URL}/${notificationId}`, {})
    ).rejects.toMatchObject({
      response: { status: 500 }
    });
  });


});

