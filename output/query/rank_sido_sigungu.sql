-- 1. 기간 내 시군구 TOP 20 (승용만)
SELECT
  r.sido, r.sigungu,
  SUM(c.passenger_subtotal) AS passenger_total
FROM sknfirst.car_registeration c
JOIN sknfirst.region r ON r.region_id = c.region_id
WHERE c.report_month BETWEEN '2023-01-01' AND '2025-12-31'
GROUP BY r.sido, r.sigungu
ORDER BY passenger_total DESC
LIMIT 20;


-- 2. 기간 내 시도 TOP 10 (영업용 총계 기준)
SELECT  r.sido,
		SUM(c.total_commercial) AS commercial_total
FROM sknfirst.car_registeration c
JOIN sknfirst.region r
	ON r.region_id = c.region_id
WHERE c.report_month
	BETWEEN '2023-08-01' AND '2025-08-31'
GROUP BY r.sido
ORDER BY commercial_total DESC
LIMIT 10;
