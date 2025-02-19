DROP TABLE IF EXISTS jobs;

CREATE TABLE jobs (
    l_id BIGINT PRIMARY KEY,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    posted TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    company TEXT NOT NULL,
    title TEXT NOT NULL,
    location TEXT NOT NULL,
    level TEXT NOT NULL,
    url TEXT NOT NULL,
    description TEXT NOT NULL,
    yoe TEXT NOT NULL,
    arrangement TEXT NOT NULL,
    pay TEXT NOT NULL DEFAULT 'Pay not stated',
    applied BOOLEAN DEFAULT false,
    rejected BOOLEAN DEFAULT false,
    saved BOOLEAN DEFAULT false,
    not_interested BOOLEAN DEFAULT false
);

DROP TABLE IF EXISTS job_ids;

CREATE TABLE job_ids (
    l_id BIGINT PRIMARY KEY,
    processed BOOLEAN DEFAULT false
)