R1. Identify problem trying to solve

R2. Why is it a problem needing solving

# R3. Why have chsen this database system waht are the drawbacks compared to others
PostgreSQL is an open-source relational database management system (RDBMS) known for its robustness, scalability, and stability. It supports a wide range of data types, and its advanced indexing techniques ensure efficient data retrieval even in large datasets.
One key strength of PostgreSQL is its extensibility, allowing developers to create custom data types, functions, and extensions to tailor the database to specific needs. Additionally, it adheres to ACID (Atomicity, Consistency, Isolation, Durability) principles, ensuring data integrity and reliability.
When comparing with other systems, PostgreSQL stands out for its active community, which means regular updates, security patches, and extensive documentation. It also provides better support for complex queries and is often favored for geospatial data handling.
However, PostgreSQL may have higher memory usage compared to some NoSQL databases, and its replication setup can be complex. Some developers may find it less suitable for certain high-speed, write-intensive applications.

# R4. Identify and discuss key functionalities and benefits of an ORM
Object-Relational Mapping (ORM) is a software technique that allows developers to interact with a relational database using object-oriented programming paradigms. It bridges the gap between the relational database and the application's object model, enabling a seamless and efficient way to manage data. 
Key Functionalities:
Database Abstraction: ORMs abstract CRUD operations, allowing Python code to interact with the database without raw SQL queries.
Object-Relational Mapping: Maps database tables to Python classes, simplifying data management and relationships.
Relationship Management: Simplifies handling one-to-one, one-to-many, and many-to-many relationships, including foreign key constraints.
Query Abstraction: Provides a query language/API, allowing complex queries in Python code for readability and maintainability.
Database Agnostic: Supports different databases, handling SQL dialect differences and optimizations.
Key Benefits:
Productivity: Accelerates development by reducing boilerplate code and simplifying database interactions.
Maintainability: Organizes and improves code readability through Python classes and objects.
SQL Injection Prevention: Mitigates SQL injection risks with automated parameterized queries and input escaping.
Database Optimization: Enhances application performance with query optimization features.
Data Consistency: Ensures data integrity through automated transaction and constraint handling.

# R5. Document all endpoints for your API
POST /auth/register : Create new user
POST /auth/login : Login as user/admin - create access token 
GET /users : retrieve list of users
GET /users/{id}: retrieve specific user by id
DELETE /users/{id} : Delete specific user (admin only)
GET /companies : retrieve list of companies
GET /companies/{id}: retrieve specific company by id
POST /companies: Create company (admin only)
DELETE /companies/{id}: delete specific company by id (admin only)
PATCH /companies/{id}: Update company details by id (admin only)
GET /performances : retrieve list of perfromances
GET /performances/{id}: retrieve specific performance by id
POST /performances: Create performance (admin only)
PATCH /performances/{id}: Update performance inforamtion by id (admin only)
DELETE /performances/{id}: delete specific performance by id (admin only)
GET /reviews: retrieve list of reviews
GET /reviews/{id}: retrieve specific review by id
POST /reviews: Create review (User required)
PATCH /reviews/{id}: Edit specific review by id (User or review only)
DELETE / reviews{id}: Delete specific review by id (Admin only)


# R6. ERD for api

# R7. Detail of Third party services
SQLAlchemy is an open-source Python SQL toolkit and ORM library. It simplifies database interactions, abstracts operations, and enables database-agnostic code. In a Flask-based API connected to PostgreSQL, SQLAlchemy defines database models and handles interactions, allowing CRUD operations in a Pythonic and efficient manner. Its abstraction layer makes switching databases easy without major code changes.

JWT Extended is a Flask extension that enhances the JSON Web Token (JWT) library. JWT, commonly used for authentication and authorization, securely transmits user data as a JSON object between client and server. In a Flask-based API, JWT Extended enables token-based authentication and authorization. It generates and signs JWT tokens upon user login, which are then sent with subsequent requests for user identification and authorization. JWT Manager is another Flask extension designed to work with Flask-JWT-Extended. It offers additional features, such as configuring token expiration, refresh, and customizing payload data. Additionally, JWT Manager allows defining checks and callbacks for custom authentication and authorization logic.

Marshmallow is a widely-used Python library for object serialization and deserialization. It converts complex data types like objects and database models into JSON and vice versa, with a simple and expressive structure definition. In a Flask-based API, Marshmallow plays a vital role in validating incoming data (request payload) and serializing the response data (API output). It seamlessly integrates with SQLAlchemy and other ORMs, allowing you to create schemas that represent database models and map them to JSON objects. Utilizing Marshmallow ensures properly formatted and validated incoming data and consistently structured outgoing data for your API.

Bcrypt is a password-hashing library commonly used in Flask-based APIs to securely store user passwords in databases. It employs a computationally expensive cryptographic hash function, making it tough for attackers to crack passwords through brute-force attacks. Bcrypt hashes and verifies passwords before saving them in the PostgreSQL database. This, along with other third-party services, creates a strong and secure foundation for web applications, ensuring robust authentication, authorization, and database interactions.

Psycopg2 is a popular PostgreSQL adapter for Python, facilitating efficient and secure communication between Python applications and PostgreSQL databases using the Python Database API (PEP 249). Within a Flask-based API connected to PostgreSQL, Psycopg2 acts as a bridge, enabling connections, executing SQL statements, fetching query results, and managing transactions. By using Psycopg2, your Flask application can seamlessly interact with the PostgreSQL database, performing all necessary CRUD operations with ease.

R8. Describe projects Models in terms of the relationships they have with each other

R9. Discuss the database relations to be implemented in the app

R10. describe the way tasks are allocated and tracked in project