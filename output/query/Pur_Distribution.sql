-- 1. 용도 비중(%)
SELECT
  ROUND(100 * SUM(total_official)   /NULLIF(SUM(total_subtotal),0), 2) AS pct_official,
  ROUND(100 * SUM(total_private)    /NULLIF(SUM(total_subtotal),0), 2) AS pct_private,
  ROUND(100 * SUM(total_commercial) /NULLIF(SUM(total_subtotal),0), 2) AS pct_commercial
FROM sknfirst.car_registeration
WHERE report_month BETWEEN '2023-08-01' AND '2025-08-31';

-- 2. 월별 용도 추이
SELECT
  DATE_FORMAT(report_month, '%Y-%m') AS ym,
  SUM(total_official)   AS official_total,
  SUM(total_private)    AS private_total,
  SUM(total_commercial) AS commercial_total
FROM sknfirst.car_registeration
WHERE report_month BETWEEN '2023-08-01' AND '2025-08-31'
GROUP BY ym
ORDER BY ym;
