CREATE TABLE IF NOT EXISTS public.clickstream_events (
  event_id      VARCHAR(64) PRIMARY KEY,
  user_id       VARCHAR(32),
  event_ts      TIMESTAMP,
  url           TEXT,
  referrer      TEXT,
  user_agent    TEXT,
  ip           INET,
  received_at   TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS public.clickstream_agg_minute (
  window_start  TIMESTAMP,
  window_end    TIMESTAMP,
  url           TEXT,
  hits          INTEGER,
  PRIMARY KEY (window_start, url)
);
