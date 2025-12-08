create table final_verified
(
    id            VARCHAR(0),
    title         VARCHAR(0),
    selftext      VARCHAR(0),
    embedding     VARCHAR(0),
    embedding_vec DOUBLE[](0),
    score         FLOAT(24),
    full_text_zsc VARCHAR(0),
    zsc_label     VARCHAR(0),
    zsc_score DOUBLE(53)
);

