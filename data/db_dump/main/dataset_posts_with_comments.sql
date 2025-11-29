create table dataset_posts_with_comments
(
    post_id          VARCHAR(0),
    post_author      VARCHAR(0),
    post_created_at  TIMESTAMP WITH TIME ZONE(0),
    subreddit        VARCHAR(0),
    title            VARCHAR(0),
    selftext         VARCHAR(0),
    post_score       BIGINT(64),
    upvote_ratio DOUBLE(53),
    num_comments     BIGINT(64),
    url              VARCHAR(0),
    domain           VARCHAR(0),
    comments_content VARCHAR[](0),
    comments_scores  BIGINT[](0)
);

