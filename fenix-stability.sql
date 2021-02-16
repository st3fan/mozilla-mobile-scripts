--
-- *** Do not update this query here - it is automatically generated every night
-- *** using https://github.com/st3fan/mozilla-mobile-scripts/blob/master/fenix-stability.py
--

DECLARE versions ARRAY<STRUCT<version STRING, release_date DATE>> DEFAULT
[
__VERSIONS__
];

DECLARE first_date DATE DEFAULT (SELECT MIN(release_date) FROM UNNEST(versions));

WITH client_durations AS (
  SELECT
    DATE(submission_timestamp) AS submission_date,
    version,
    LEAST(SUM(coalesce(metrics.timespan.glean_baseline_duration.value, 0)), 60 * 60 * 24) AS duration,
  FROM
    `moz-fx-data-shared-prod`.org_mozilla_firefox.baseline
  JOIN
    UNNEST(versions) ON version = client_info.app_display_version
  WHERE
    DATE(submission_timestamp) >= first_date
  GROUP BY
    submission_date,
    client_info.client_id,
    version
), durations AS (
  SELECT
    submission_date,
    version,
    SUM(duration) AS duration,
  FROM
    client_durations
  GROUP BY
    submission_date,
    version
), client_crashes AS (
  SELECT
    DATE(submission_timestamp) AS submission_date,
    version,
    LEAST(SUM(crash_instance.value), 100) AS crash_count,
  FROM
    `moz-fx-data-shared-prod`.org_mozilla_firefox.metrics AS m,
    UNNEST(m.metrics.labeled_counter.crash_metrics_crash_count) AS crash_instance
  JOIN
    UNNEST(versions) ON version = client_info.app_display_version
  WHERE
    DATE(submission_timestamp) >= first_date
    and crash_instance.key in ('native_code_crash','uncaught_exception','fatal_native_code_crash')
  GROUP BY
    submission_date,
    version,
    client_info.client_id
), crashes AS (
  SELECT
    submission_date,
    version,
    SUM(crash_count) AS crash_count
  FROM
    client_crashes
  GROUP BY
    submission_date,
    version
), all_data AS (
SELECT
  version,
  DATE_DIFF(submission_date, release_date, DAY) AS days_since_release,
  COALESCE(crash_count, 0) / (duration / (60 * 60)) AS crashes_per_hour,
FROM
  durations
LEFT JOIN
  crashes USING (submission_date, version)
JOIN
  UNNEST(versions) USING (version)
WHERE
  DATE_DIFF(submission_date, release_date, DAY) <= 31
UNION ALL
SELECT
  'Baseline' AS version,
  days_since_release,
  0.04 AS crashes_per_hour,
FROM
  UNNEST(GENERATE_ARRAY(0, 31, 1)) AS days_since_release
)

SELECT *
FROM all_data
ORDER BY
  IF(version LIKE 'Baseline', 1, 0) DESC,
  SAFE_CAST(SPLIT(version, '.')[SAFE_OFFSET(0)] AS INT64) DESC,
  SAFE_CAST(SPLIT(version, '.')[SAFE_OFFSET(1)] AS INT64) DESC,
  SAFE_CAST(SPLIT(version, '.')[SAFE_OFFSET(2)] AS INT64) DESC,
  days_since_release ASC

