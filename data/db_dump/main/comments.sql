create table comments
(
    id            VARCHAR(0),
    submission_id VARCHAR(0),
    parent_id     VARCHAR(0),
    author        VARCHAR(0),
    created_at    TIMESTAMP WITH TIME ZONE(0),
    subreddit     VARCHAR(0),
    body          VARCHAR(0),
    score         BIGINT(64)
);

