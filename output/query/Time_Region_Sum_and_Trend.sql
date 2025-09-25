-- 기간/지역 합계 & 추이
-- 1. 특정 기간 전체 합계
SELECT
  SUM(total_subtotal) AS total_new_regs
FROM sknfirst.car_registeration
WHERE report_month BETWEEN '2023-08-01' AND '2025-08-31';

-- 2. 시도 합계 TOP 10
SELECT
  r.sido,
  SUM(c.total_subtotal) AS total_new_regs
FROM sknfirst.car_registeration c
JOIN sknfirst.region r ON r.region_id = c.region_id
WHERE c.report_month BETWEEN '2023-08-01' AND '2025-08-31'
GROUP BY r.sido
ORDER BY total_new_regs DESC
LIMIT 10;

-- (3) 특정 시군구 월별 추이(라인차트)
SELECT
  DATE_FORMAT(c.report_month, '%Y-%m') AS ym,
  SUM(c.total_subtotal) AS total_new_regs
FROM sknfirst.car_registeration c
JOIN sknfirst.region r ON r.region_id = c.region_id
WHERE r.sido='서울' AND r.sigungu='강남구'
  AND c.report_month BETWEEN '2024-01-01' AND '2024-12-31'
GROUP BY ym
ORDER BY ym;

-- (3) 특정 시군구 월별 추이
SELECT
  DATE_FORMAT(c.report_month, '%Y-%m') AS ym,
  SUM(c.total_subtotal) AS total_new_regs
FROM sknfirst.car_registeration c
JOIN sknfirst.region r ON r.region_id = c.region_id
WHERE r.sido='서울' AND r.sigungu='강남구'
  AND c.report_month BETWEEN '2024-01-01' AND '2024-12-31'
GROUP BY ym
ORDER BY ym;
