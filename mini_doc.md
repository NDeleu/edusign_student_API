
---

### Application: Authentication

**Base URL:** `/api/auth/`

---

#### CRUD User

**1. Register User**
- **Endpoint:** `register/`
- **Type:** POST
- **Permissions:** IsAuthenticated, IsAdministrator
- **Description:** Register a new user.
- **JSON Request:**
```json
{
    "email": "string",
    "password": "string",
    "first_name": "string",
    "last_name": "string",
    "status": "string (choices: student, intervening, administrator)",
    "promotion": "integer (optional)"
}
```

**2. List Users**
- **Endpoint:** `users/list/`
- **Type:** GET
- **Permissions:** IsAuthenticated, IsAdministratorOrIntervening
- **Description:** Retrieve a list of all users.
- **JSON Response (example):
```json
{
    "id": "integer",
    "email": "string",
    "first_name": "string",
    "last_name": "string",
    "status": "string",
    "promotion": "integer or null"
}
```

**3. Retrieve User Details**
- **Endpoint:** `users/detail/<int:id>/`
- **Type:** GET
- **Permissions:** IsAuthenticated, IsAdministratorOrIntervening
- **Description:** Retrieve the details of a specific user by ID.
- **JSON Response (example):
```json
{
    "id": "integer",
    "email": "string",
    "first_name": "string",
    "last_name": "string",
    "status": "string",
    "promotion": "integer or null"
}
```


**4. Retrieve My Details**
- **Endpoint:** `users/my-details/`
- **Type:** GET
- **Permissions:** IsAuthenticated
- **Description:** Retrieve the details of the authenticated user.
- **JSON Response (example):
```json
{
   "id": "integer",
   "email": "string",
   "first_name": "string",
   "last_name": "string",
   "status": "string",
   "promotion": "integer or null"
}
```


**5. Update User Details**
- **Endpoint:** `users/update/<int:id>/`
- **Type:** PUT
- **Permissions:** IsAuthenticated, IsAdministrator
- **Description:** Update the details of a specific user by ID.
- **JSON Response (example):
```json
{
   "email": "string",
   "first_name": "string",
   "last_name": "string",
   "status": "string",
   "promotion": "integer or null"
}
```


**6. Change Password**
- **Endpoint:** `users/change-password/`
- **Type:** POST
- **Permissions:** IsAuthenticated
- **Description:** Change the password of the authenticated user.
```json
{
    "current_password": "string",
    "new_password": "string"
}
```

**7. Delete User**
- **Endpoint:** `users/delete/<int:id>/`
- **Type:** DELETE
- **Permissions:** IsAuthenticated, IsAdministrator
- **Description:** Delete a specific user by ID.
- **JSON Response (success example):
```json
{
   "success": "User deleted successfully."
}
```


---

#### CRUD Promotion

**1. Create Promotion**
- **Endpoint:** `promo/create/`
- **Type:** POST
- **Permissions:** IsAuthenticated, IsAdministrator
- **Description:** Create a new promotion.
- **JSON Request:**
```json
{
    "name": "string"
}
```

**2. List Promotions**
- **Endpoint:** `promo/list/`
- **Type:** GET
- **Permissions:** IsAuthenticated, IsAdministratorOrIntervening
- **Description:** Retrieve a list of all promotions.


**3. Retrieve Promotion Details**
- **Endpoint:** `promo/detail/<int:id>/`
- **Type:** GET
- **Permissions:** IsAuthenticated, IsAdministratorOrIntervening
- **Description:** Retrieve the details of a specific promotion by ID.


**4. Update Promotion**
- **Endpoint:** `promo/update/<int:id>/`
- **Type:** PUT
- **Permissions:** IsAuthenticated, IsAdministrator
- **Description:** Update the details of a specific promotion by ID.


**5. Delete Promotion**
- **Endpoint:** `promo/delete/<int:id>/`
- **Type:** DELETE
- **Permissions:** IsAuthenticated, IsAdministrator
- **Description:** Delete a specific promotion by ID.


---

#### Token Management

**1. Obtain Token Pair**
- **Endpoint:** `token/`
- **Type:** POST
- **Description:** Obtain a token pair using email and password.
- **JSON Request:**
```json
{
    "email": "string",
    "password": "string"
}
```

**2. Refresh Token**
- **Endpoint:** `token/refresh/`
- **Type:** POST
- **Description:** Refresh the access token.
- **JSON Request:**
```json
{
    "refresh": "string"
}
```
---

### Application: Gestion des cours

**Base URL:** `/api/lesson/`

---

#### CRUD Lesson:

**1. Create Lesson**
- **Endpoint:** `create/`
- **Type:** POST
- **Permissions:** IsAuthenticated, IsAdministrator
- **Description:** Create a new lesson.
- **JSON Request:**
```json
{
    "name": "string",
    "date_debut": "date (YYYY-MM-DD)",
    "date_fin": "date (YYYY-MM-DD)",
    "description": "string (optional)",
    "intervening": "integer (User ID)",
    "classroom": "integer (ClassRoom ID)",
    "promotion": "integer (Promotion ID)"
}
```

**2. List Lessons**
- **Endpoint:** `list/`
- **Type:** GET
- **Permissions:** IsAuthenticated, IsAdministratorOrIntervening
- **Description:** List all lessons.


**3. List Lessons for User**
- **Endpoint:** `user-list/`
- **Type:** GET
- **Permissions:** IsAuthenticated
- **Description:** List all lessons associated with the logged-in user's promotion.


**4. Get Lesson Details**
- **Endpoint:** `detail/<int:id>/`
- **Type:** GET
- **Permissions:** IsAuthenticated, IsAdministratorOrIntervening
- **Description:** Get details of a specific lesson.


**5. Get Lesson Details for User**
- **Endpoint:** `user-detail/<int:id>/`
- **Type:** GET
- **Permissions:** IsAuthenticated
- **Description:** Get details of a specific lesson associated with the logged-in user's promotion.

**6. Update Lesson**
- **Endpoint:** `update/<int:id>/`
- **Type:** PUT/PATCH
- **Permissions:** IsAuthenticated, IsAdministrator
- **Description:** Update a specific lesson.
- **JSON Request (for PUT):**
```json
{
    "name": "string",
    "date_debut": "date (YYYY-MM-DD)",
    "date_fin": "date (YYYY-MM-DD)",
    "description": "string",
    "intervening": "integer (User ID)",
    "classroom": "integer (ClassRoom ID)"
}
```

**7. Delete Lesson**
- **Endpoint:** `delete/<int:id>/`
- **Type:** DELETE
- **Permissions:** IsAuthenticated, IsAdministrator
- **Description:** Delete a specific lesson.


---

#### CRUD ClassRoom:

**1. Create ClassRoom**
- **Endpoint:** `classroom/create/`
- **Type:** POST
- **Permissions:** IsAuthenticated, IsAdministrator
- **Description:** Create a new classroom.
- **JSON Request:**
```json
{
    "name": "string"
}
```

**2. List ClassRooms**
- **Endpoint:** `classroom/list/`
- **Type:** GET
- **Permissions:** IsAuthenticated, IsAdministratorOrIntervening
- **Description:** List all classrooms.


**3. Update ClassRoom**
- **Endpoint:** `classroom/update/<int:id>/`
- **Type:** PUT/PATCH
- **Permissions:** IsAuthenticated, IsAdministrator
- **Description:** Update a specific classroom.
- **JSON Request:**
```json
{
    "name": "string"
}
```


**4. Delete ClassRoom**
- **Endpoint:** `classroom/delete/<int:id>/`
- **Type:** DELETE
- **Permissions:** IsAuthenticated, IsAdministrator
- **Description:** Delete a specific classroom.


---

#### CRUD Presence:

**1. Create Presence**
- **Endpoint:** `presence/create/`
- **Type:** POST
- **Permissions:** IsAuthenticated, IsAdministrator
- **Description:** Mark the presence of a student in a lesson.
- **JSON Request:**
```json
{
    "student": "integer (User ID)",
    "lesson": "integer (Lesson ID)"
}
```

**2. List Presence by Lesson**
- **Endpoint:** `presence/list-by-lesson/<int:lesson_id>/`
- **Type:** GET
- **Permissions:** IsAuthenticated, IsAdministratorOrIntervening
- **Description:** List all presences for a specific lesson.


**3. Get Presence Details**
- **Endpoint:** `presence/detail/<int:id>/`
- **Type:** GET
- **Permissions:** IsAuthenticated, IsAdministratorOrIntervening
- **Description:** Get details of a specific presence entry.


**4. Update Presence**
- **Endpoint:** `presence/update/<int:id>/`
- **Type:** PUT/PATCH
- **Permissions:** IsAuthenticated, IsAdministratorOrIntervening
- **Description:** Update a specific presence entry.
- **JSON Request:**
```json
{
    "is_present": "boolean"
}
```


---

#### Count Presence and Absence:

**1. Count Presence for Self**
- **Endpoint:** `presence/my-lessons-count/`
- **Type:** GET
- **Permissions:** IsAuthenticated, IsStudent
- **Description:** Count the number of lessons attended by the logged-in user.

**2. Count Absences for Self**
- **Endpoint:** `presence/my-absences-count/`
- **Type:** GET
- **Permissions:** IsAuthenticated, IsStudent
- **Description:** Count the number of lessons missed by the logged-in user.


**3. Get Absence Rate for Self**
- **Endpoint:** `presence/my-absence-rate/`
- **Type:** GET
- **Permissions:** IsAuthenticated, IsStudent
- **Description:** Get the absence rate of the logged-in user.

**4. Count Presence for a User**
- **Endpoint:** `presence/user-lessons-count/<int:user_id>/`
- **Type:** GET
- **Permissions:** IsAuthenticated, IsAdministratorOrIntervening
- **Description:** Count the number of lessons attended by a specific user.

**5. Count Absences for a User**
- **Endpoint:** `presence/user-absences-count/<int:user_id>/`
- **Type:** GET
- **Permissions:** IsAuthenticated, IsAdministratorOrIntervening
- **Description:** Count the number of lessons missed by a specific user.

**6. Get Absence Rate for a User**
- **Endpoint:** `presence/user-absence-rate/<int:user_id>/`
- **Type:** GET
- **Permissions:** IsAuthenticated, IsAdministratorOrIntervening
- **Description:** Get the absence rate of a specific user.

---

### Application: Justification des Absences

**Base URL:** `/api/justification/`

---

#### CRUD Justification

**1. Créer une justification**
- **Endpoint:** `create/`
- **Type:** POST
- **Permissions:** IsAuthenticated, IsStudent
- **Description:** Créer une nouvelle justification d'absence.
- **JSON Request:**
```json
{
    "absence_reason": "string (choices: sickness, familydeath, alarmclockfailure, otherreason)",
    "date_debut": "date",
    "date_fin": "date",
    "proof_document": "file (format: pdf)"
}
```

**2. Liste des justifications pour l'étudiant**
- **Endpoint:** `list/student/`
- **Type:** GET
- **Permissions:** IsAuthenticated, IsStudent
- **Description:** Retourne une liste de toutes les justifications soumises par l'étudiant connecté.
- **Response:** 
```json
{
    "id": "integer",
    "date_debut": "date",
    "date_fin": "date",
    "is_validate": "boolean (null si non vérifié, true si validé, false si non validé)"
}
```

**3. Liste des justifications pour l'administrateur**
- **Endpoint:** `list/administrator/`
- **Type:** GET
- **Permissions:** IsAuthenticated, IsAdministrator
- **Description:** Retourne une liste de toutes les justifications pour un administrateur.

**4. Liste des justifications pour un étudiant spécifique par l'administrateur**
- **Endpoint:** `list/administrator/<int:user_id>/`
- **Type:** GET
- **Permissions:** IsAuthenticated, IsAdministrator
- **Description:** Retourne une liste de justifications pour un étudiant spécifique.

**5. Détails d'une justification pour l'étudiant**
- **Endpoint:** `detail/student/<int:id>/`
- **Type:** GET
- **Permissions:** IsAuthenticated, IsStudent
- **Description:** Affiche les détails d'une justification d'absence pour l'étudiant.

**6. Détails d'une justification pour l'administrateur**
- **Endpoint:** `detail/administrator/<int:id>/`
- **Type:** GET
- **Permissions:** IsAuthenticated, IsAdministrator
- **Description:** Affiche les détails d'une justification d'absence pour l'administrateur.

**7. Mise à jour de la justification par l'étudiant**
- **Endpoint:** `update/student/<int:id>/`
- **Type:** PUT/PATCH
- **Permissions:** IsAuthenticated, IsStudent
- **Description:** Permet à l'étudiant de mettre à jour une justification d'absence.
- **JSON Request:**
```json
{
    "absence_reason": "string (choices: sickness, familydeath, alarmclockfailure, otherreason)",
    "date_debut": "date",
    "date_fin": "date",
    "proof_document": "file (format: pdf)"
}
```

**8. Mise à jour de la justification par l'administrateur**
- **Endpoint:** `update/administrator/<int:id>/`
- **Type:** PUT/PATCH
- **Permissions:** IsAuthenticated, IsAdministrator
- **Description:** Mettre à jour la validation d'une justification d'absence par l'administrateur.
- **JSON Request:**
```json
{
    "is_validate": "boolean (true/false)"
}
```

**9. Supprimer une justification**
- **Endpoint:** `delete/<int:id>/`
- **Type:** DELETE
- **Permissions:** IsAuthenticated, IsSelforAdministrator
- **Description:** Supprime une justification d'absence.

---

#### Compter les absences non justifiées

**1. Compter les absences non justifiées pour l'utilisateur connecté**
- **Endpoint:** `unjustified/self/`
- **Type:** GET
- **Permissions:** IsAuthenticated, IsStudent
- **Description:** Renvoie le nombre d'absences non justifiées pour l'utilisateur connecté.
- **JSON Response:**
```json
{
    "unjustified_absence_count": "integer"
}
```

**2. Compter les absences non justifiées pour un étudiant spécifique**
- **Endpoint:** `unjustified/<int:user_id>/`
- **Type:** GET
- **Permissions:** IsAuthenticated, IsAdministratorOrIntervening
- **Description:** Renvoie le nombre d'absences non justifiées pour un étudiant spécifique.
- **JSON Response:**
```json
{
    "unjustified_absence_count": "integer"
}
```

---

### Application: qrcode_check

**Base URL:** `/api/qr-code/`

---

#### QRCode Management

**1. Generate QRCode**
- **Endpoint:** `generate/`
- **Type:** GET
- **Permissions:** IsAuthenticated, IsIntervening
- **Description:** Génère un QR code pour la leçon en cours.
- **JSON Response (example):**
```json
{
    "qr_code": "URL_of_QR_Image",
    "expiration_time": "expiration_datetime"
}
```

**2. Validate QRCode**
- **Endpoint:** `validate/`
- **Type:** POST
- **Permissions:** IsAuthenticated, IsStudent
- **Description:** Valide le QR code scanné pour marquer la présence.
- **JSON Request:**
```json
{
    "scanned_qr": "hashed_qr_content",
    "student": "student_id"
}
```
- **JSON Response (success example):**
```json
{
    "success": "Presence marked successfully."
}
```

---
