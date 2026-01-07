const axios = require("axios");

const BASE_URL = "http://127.0.0.1:8000/v1/notifications";

describe("Notifications API", () => {

  // ------------------
  // 1. LOGIN OK
  // ------------------
  test("Login event creates notification", async () => {
    const payload = {
      userId: "123", // student
      type: "login",
      metadata: {
        ip: "127.0.0.1",
        device: "Chrome"
      }
    };

    const res = await axios.post(`${BASE_URL}/events`, payload, { headers: { "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOiIyMzQifQ.fake" } });

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
      userId: "123",
      type: "transaction",
      metadata: {
        amount: 50,
        recipient: "Amazon"
      }
    };

    const res = await axios.post(`${BASE_URL}/events`, payload, { headers: { "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOiIyMzQifQ.fake" } });

    expect(res.status).toBe(201);
    expect(res.data.title.toLowerCase()).toContain("pago realizado");
  });

  // ------------------
  // 4. TRANSACCION NEGATIVA OK
  // ------------------
  test("Transaction negative OK creates notification", async () => {
    const payload = {
      userId: "123",
      type: "transaction",
      metadata: {
        amount: -75,
        recipient: "eBay"
      }
    };

    const res = await axios.post(`${BASE_URL}/events`, payload, { headers: { "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOiIyMzQifQ.fake" } });

    expect(res.status).toBe(201);
    expect(res.data.title.toLowerCase()).toContain("pago realizado correctamente");
  });

  // // ------------------
  // // 5. HISTORY REQUEST 
  // // ------------------
  // test("History request", async () => {
  //   const payload = {
  //     userId: "123", // pro
  //     type: "history-request",
  //     metadata: {
  //       mode: "all"
  //     }
  //   };

  //   const res = await axios.post(`${BASE_URL}/events`, payload, { headers: { "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOiIyMzQifQ.fake" } });

  //   expect(res.status).toBe(201);
  //   expect(res.data.email_sent).toBe(true);
  // });

  // ------------------
  // 6. FRAUD DETECTED
  // ------------------
  test("Fraud detected event creates alert notification", async () => {
    const payload = {
      userId: "123",
      type: "fraud-detected",
      metadata: {
        reason: "Intentos sospechosos"
      }
    };

    const res = await axios.post(`${BASE_URL}/events`, payload, { headers: { "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOiIyMzQifQ.fake" } });

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
      userId: "123",
      type: "scheduled-payment",
      metadata: {
        amount: 200,
        recipient: "Netflix",
        scheduledDate: "2026-02-01"
      }
    };

    const res = await axios.post(`${BASE_URL}/events`, payload, { headers: { "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOiIyMzQifQ.fake" } });
    expect(res.status).toBe(201);
    expect(res.data.title.toLowerCase()).toContain("pago programado");
  });

  // ------------------
  // 9. GET NOTIFICATIONS BY USER
  // ------------------
  test("Get notifications by user returns array", async () => {
    const res = await axios.get(`${BASE_URL}/user/123`, { headers: { "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOiIyMzQifQ.fake" } });

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
  test("Update notification title", async () => {

  // 1. Crear notificación previa
  const created = await axios.post(`${BASE_URL}/events`, {
    userId: "123",
    type: "login",
    metadata: {}
  }, {
    headers: {
      "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOiIyMzQifQ.fake"
    }
  });

  const notificationId = created.data.id;

  // 2. Actualizar → debería funcionar (200)
  const resUp = await axios.put(`${BASE_URL}/${notificationId}`, {
    title: "Título actualizado desde test"
  }, {
    headers: {
      "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOiIyMzQifQ.fake"
    }
  });

  expect([200,404]).toContain(resUp.status);
  expect(resUp.data.title).toMatch(/actualizado/i);
});


  // ------------------
  // 12. DELETE NOTIFICATION
  // ------------------
test("Delete notification", async () => {

  // 1. Crear real
  const created = await axios.post(`${BASE_URL}/events`, {
    userId: "123",
    type: "transaction",
    metadata: { amount: 20 }
  }, {
    headers: {
      "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOiIyMzQifQ.fake"
    }
  });

  const id = created.data.id;

  // 2. Delete real → 200
  const resDel = await axios.delete(`${BASE_URL}/${id}`, {
    headers: {
      "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOiIyMzQifQ.fake"
    }
  });

  expect([200,404]).toContain(resDel.status);
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
      userId: "123",
      type: "login",
      metadata: {}
    }, { headers: { "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOiIyMzQifQ.fake" } });

    await axios.post(`${BASE_URL}/events`, {
      userId: "123",
      type: "transaction",
      metadata: { amount: 10 }
    }, { headers: { "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOiIyMzQifQ.fake" } });

    const res = await axios.get(`${BASE_URL}/user/123`);
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
  // 16. MISSING USER ID
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

//   // ------------------
//   // 20. UPDATE NOTIFICATION WITH EMPTY BODY
//   // ------------------
// test("Update notification with empty body returns server error", async () => {

//   // crear previa
//   const created = await axios.post(`${BASE_URL}/events`, {
//     userId: "123",
//     type: "login",
//     metadata: {}
//   }, {
//     headers: { "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOiIyMzQifQ.fake" }
//   });

//   const notificationId = created.data.id;

//   // update vacío → tu MS devuelve 400 o 500
//   await expect(
//     axios.put(`${BASE_URL}/${notificationId}`, {}, {
//       headers: { "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOiIyMzQifQ.fake" }
//     })
//   ).rejects.toMatchObject({
//     response: { status: 200 }
//   });
// });

});

