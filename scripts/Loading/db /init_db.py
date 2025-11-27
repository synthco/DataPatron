import duckdb
import os
from pathlib import Path


data_dir = Path("/Users/ivantyshchenko/Projects/Python/DataPatron/data")
SUBMISSIONS_CSV = data_dir / "filtered_submissions.csv"
COMMENTS_CSV = data_dir / "filtered_comments.csv"
DB_FILE = data_dir / "reddit.duckdb"

con =duckdb.connect(DB_FILE)

print("Creating table submissions")
con.sql(f"""
    CREATE OR REPLACE TABLE submissions AS 
    SELECT 
        id,
        author,
        -- Конвертація epoch seconds в datetime
        to_timestamp(CAST(created_utc AS BIGINT)) as created_at,
        subreddit,
        title,
        selftext,
        score,
        upvote_ratio,
        num_comments,
        url,
        domain
    FROM read_csv_auto('{SUBMISSIONS_CSV}', ignore_errors=true)
    WHERE id IS NOT NULL
""")

print("Crate table comments")

con.sql(f"""
    CREATE OR REPLACE TABLE comments AS 
    SELECT 
        id,
        -- Прибираємо 't3_' якщо воно є, залишаючи чистий ID поста
        CASE WHEN link_id LIKE 't3_%' THEN substr(link_id, 4) ELSE link_id END as submission_id,
        parent_id,
        author,
        to_timestamp(CAST(created_utc AS BIGINT)) as created_at,
        subreddit,
        body,
        score
    FROM read_csv_auto('{COMMENTS_CSV}', ignore_errors=true)
    WHERE id IS NOT NULL
""")

print("Indexing...")
con.sql("CREATE UNIQUE INDEX idx_sub_id ON submissions(id)")
con.sql("CREATE INDEX idx_com_sub_id ON comments(submission_id)")
con.sql("CREATE INDEX idx_sub_subreddit ON submissions(subreddit)")
con.sql("CREATE INDEX idx_com_author ON comments(author)")








