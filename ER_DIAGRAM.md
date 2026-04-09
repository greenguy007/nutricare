# Entity Relationship Diagram (ERD)

```
+---------------------+       +---------------------+
|       LOGIN         |       |      CUSTOMER       |
+---------------------+       +---------------------+
| id (PK)             |<-----<| login_id (FK)       |
| username            |       | id (PK)             |
| password            |       | full_name           |
| usertype            |       | phone               |
| otp                 |       | address             |
| is_verified         |       | email               |
+---------------------+       | image               |
        ^                        +---------------------+
        |                                  
        | 1:1                   +---------------------+
        |                        |      DIETICIAN      |
        |                      +---------------------+
        |                      | id (PK)             |
        +--------------------<| login_id (FK)       |
                      |      | full_name           |
                      |      | phone               |
                      |      | address             |
                      |      | email               |
                      |      | image               |
                      |      | license_file        |
                      |      +---------------------+
                      |                ^
                      |                |
         1:N           |           1:N
                      |                |
+---------------------+|     +---------+---------+
|     DIETPLAN        |<----+  WORKOUTPLAN        |
+---------------------+     +---------------------+
| id (PK)             |     | id (PK)              |
| dietician_id (FK)   |----<| dietician_id (FK)    |
| plan_name           |     | title                |
| image               |     | description          |
| description         |     | image                |
| created_at          |     | video                |
| plan_type           |     | is_free              |
| price               |     | price                |
+---------------------+     +----------+----------+
         |                            |
         | 1:N                      | 1:N
         |                          |
+--------+--------+      +---------+---------+
|    DIETSTEP      |      |   WORKOUTSTEP     |
+----------------+      +-------------------+
| id (PK)         |      | id (PK)            |
| diet_plan_id(FK)|      | plan_id (FK)      |
| step_text       |      | step_number       |
+----------------+      | title             |
                        | description       |
                        | image             |
                        +-------------------+


+---------------------+       +---------------------+
|  CUSTOMERDIETPLAN   |       |  WORKOUTPURCHASE   |
+---------------------+       +---------------------+
| id (PK)             |       | id (PK)             |
| customer_id (FK)    |<-----<| customer_id (FK)   |
| diet_plan_id (FK)   |       | plan_id (FK)        |
| joined_date         |       | purchased_at       |
+---------------------+       +---------------------+
         |
         | 1:N
         |
+--------+--------+
| CUSTOMERDIETSTEP |
+-----------------+
| id (PK)         |
| customer_diet_  |
|   plan_id (FK)  |
| diet_step_id(FK)|
| is_completed    |
+-----------------+


+---------------------+       +---------------------+
|   CUSTOMIZATION    |       |    CUSTOMDIETPLAN   |
|     REQUEST        |       +---------------------+
+---------------------+       | id (PK)             |
| id (PK)             |       | customer_id (FK)   |
| customer_id (FK)   |<------| dietician_id (FK)   |
| dietician_id (FK)  |       | request_id (FK)    |
| diet_plan_id (FK)  |       | title               |
| notes              |       | description         |
| status             |       | created_at          |
| created_at         |       +----------+----------+
+---------------------+                |
         ^                                 | 1:N
         |                                 |
         | OneToOne                       |
         +--------------------------------+

+---------------------+       +---------------------+
|     DIETFEEDBACK   |       |   WORKOUTFEEDBACK   |
+---------------------+       +---------------------+
| id (PK)            |       | id (PK)             |
| customer_id (FK)   |<------<| customer_id (FK)   |
| diet_plan_id (FK)  |       | plan_id (FK)        |
| rating             |       | rating              |
| feedback           |       | comment            |
| created_at         |       | created_at         |
+---------------------+       +---------------------+


+---------------------+       +---------------------+
|     CUSTOMBMI      |       |    CUSTOMERBMR      |
+---------------------+       +---------------------+
| id (PK)            |       | id (PK)             |
| customer_id (FK)   |<------<| customer_id (FK)   |
| height_cm          |       | age                 |
| weight_kg          |       | gender              |
| bmi                |       | height_cm           |
| created_at         |       | weight_kg           |
+---------------------+       | bmr                 |
                            | created_at          |
                            +---------------------+


+---------------------+       +---------------------+
|        FOOD         |       |    CUSTOMERMEAL     |
+---------------------+       +---------------------+
| id (PK)            |       | id (PK)             |
| dietician_id (FK)  |<------<| customer_id (FK)   |
| name               |       | food_id (FK)        |
| meal_type          |       | date                |
| calories           |       | is_completed        |
| carbs              |       +---------------------+
| protein            |
| fat                |       +---------------------+
| zinc               |       |     DIETPLANPDF     |
| created_at         |       +---------------------+
+---------------------+       | id (PK)             |
                            | dietician_id (FK)   |
+---------------------+       | title               |
|        CHAT         |       | pdf_file            |
+---------------------+       | uploaded_at         |
| id (PK)            |       +---------------------+
| sender_id (FK)     |
| receiver_id (FK)  |
| message           |
| date              |
+---------------------+
```

## Relationship Legend

```
| Notation  | Meaning           |
|-----------|-------------------|
| <        | Many side         |
| >        | One side         |
| -----    | Direct relationship|
| 1:1      | One-to-One       |
| 1:N      | One-to-Many     |
| N:M      | Many-to-Many    |
```

## Key Entities

| Entity       | Description                    |
|--------------|--------------------------------|
| Login        | Base user (admin/customer/dietician) |
| Customer     | App user who joins diets/workouts |
| Dietician    | Nutrition expert who creates plans |
| DietPlan     | Diet meal plan (free/paid)       |
| WorkoutPlan  | Exercise plan (free/paid)          |
| Food         | Food items with nutrition data       |
| Chat         | Messages between customer & dietician |