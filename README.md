# Database Technology

This project uses SQLite as the database engine.

Although the database is stored in a .db file (loja1.db), it does not use MySQL.
SQLite is a lightweight, file-based relational database, suitable for local analytics, prototyping, and demonstrations.

Key characteristics:

- Embedded database stored in a single .db file
- No server, user, password, or network configuration required
- SQL syntax compatible with most relational databases

  SQLite was intentionally chosen to simplify setup and focus on SQL queries, KPI generation, and data analysis logic.
  The same schema and queries can be easily migrated to MySQL or PostgreSQL for production environments.
