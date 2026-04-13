The following are the solutions for **Test 2 (SEEL4213: Software Engineering)**, based on the provided source materials.

### **Section 1: Requirements Engineering (25%)**

**Functional vs. Non-Functional Classification:**
*   The system shall read the DHT11 sensor every 60 seconds: **Functional (F)** (describes a specific behavior/function).
*   The database shall recover from a power failure without data corruption (ACID compliance): **Non-Functional (NF)** (describes a quality attribute of reliability).
*   The dashboard must load historical data graphs within 3 seconds: **Non-Functional (NF)** (describes a performance constraint).
*   The system shall trigger an email alert if temperature exceeds 35°C: **Functional (F)** (describes a system response to an input).

**Use Case Diagram:**
*   **Actors:** System Administrator (Primary), DHT11 Sensor (Secondary/Hardware Actor).
*   **Use Cases:** "Read Sensor Data," "Sync to Cloud," and "View Dashboard."
*   **Relationship:** "Read Sensor Data" **\<\<include>>** "Sync to Cloud" (assuming every reading is synced) or "View Dashboard" **\<\<include>>** "Login."

---

### **Section 2: Object-Oriented Analysis and Design (15%)**

**Sequence Diagram (SSD):**
*   **Flow:** 
    1.  **Timer** sends a signal/trigger to the **Controller**.
    2.  **Controller** calls `read()` on the **DHT11 Sensor**.
    3.  **DHT11 Sensor** returns `data (temp, hum)` to the **Controller**.

**GRASP Principles:**
*   The principle being applied is **High Cohesion**. Keeping hardware code separate from database operations ensures each class has a "single, well-defined purpose".

---

### **Section 3: High-Level Design (15%)**

**Architectural Styles (MVC):**
*   **Model:** **SQLite Database** (handles data storage and logic).
*   **View:** **Blynk Dashboard** (the user interface that displays the data).
*   **Controller:** **RPi Python App** (the bridge that processes input and updates the Model/View).

**Coupling:**
*   It is preferable to have **Low Coupling**. 
*   **Reason:** Low coupling ensures that changes to the Sensor driver do not break the Cloud Sync module, making the system easier to maintain, test, and reuse.

---

### **Section 4: Design Patterns (10%)**

**Pattern Selection:**
1.  Ensuring only one instance of I2CBusManager: **Singleton**.
2.  Automatically notifying Logger and Dashboard of new readings: **Observer**.
3.  Modeling transitions (INITIALIZING → READING → SLEEPING): **State**.

---

### **Section 5: Database Design (25%)**

**Entity-Relationship Diagram (ERD):**
*   **Entities:** **Room** (Attributes: RoomID, Name) and **Reading** (Attributes: ReadingID, Temperature, Humidity).
*   **Relationship:** A **One-to-Many (1:M)** line from Room to Reading (one room can have many recorded readings).

**SQL Operations:**
*   `SELECT AVG(temperature) FROM sensor_data WHERE humidity > 80;` 
    *(Note: The exact column names "temperature" and "humidity" are standard SQL naming conventions and not explicitly defined in the snippet, but follow the logic of the source)*

---

### **Section 6: Implementation (10%)**

**Algorithm Complexity:**
*   The Big O complexity is **O(n)** (Linear Search). Searching through an unsorted list requires checking every element in the worst case.

**Refactoring (Magic Numbers):**
*   **Code Smell:** A "Magic Number" is a **hardcoded numeric value** (like `35` or `80`) used in the code without an explanation of its meaning.
*   **Fix:** Replace the number with a **named constant** (e.g., `MAX_TEMP_THRESHOLD = 35`) to improve readability and maintainability.
