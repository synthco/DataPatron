create table submissions
(
    id           VARCHAR(0),
    author       VARCHAR(0),
    created_at   TIMESTAMP WITH TIME ZONE(0),
    subreddit    VARCHAR(0),
    title        VARCHAR(0),
    selftext     VARCHAR(0),
    score        BIGINT(64),
    upvote_ratio DOUBLE(53),
    num_comments BIGINT(64),
    url          VARCHAR(0),
    domain       VARCHAR(0)
);

