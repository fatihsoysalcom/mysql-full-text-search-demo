# MySQL Full Text Search Demo

This Python script demonstrates MySQL's Full-Text Search capabilities, as discussed in the accompanying blog post. It sets up a temporary database and table with a `FULLTEXT` index, inserts sample Turkish article data, and then compares traditional `LIKE` queries with `MATCH AGAINST` queries in both Natural Language and Boolean modes. The example highlights how Full-Text Search improves search performance and relevance for textual data.

## Language

`python`

## How to Run

1. Ensure you have a MySQL server running and `mysql-connector-python` installed (`pip install mysql-connector-python`).
2. Update `DB_CONFIG['password']` in `main.py` with your MySQL root password.
3. Run the script: `python main.py`

## Original Article

This example accompanies the Turkish article: [MySQL 5.6 ve Ubuntu 16.04 Üzerinde Full-Text Search (Tam Metin Arama) ile Veritabanı Aramalarını İyileştirme](https://fatihsoysal.com/blog/?p=43274).

## License

MIT — see [LICENSE](LICENSE).
