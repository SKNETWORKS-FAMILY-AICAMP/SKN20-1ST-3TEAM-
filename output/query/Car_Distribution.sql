-- 1. 차종별 합계(파이차트로 만들 수 있나?)
SELECT
  SUM(passenger_subtotal) AS passenger,
  SUM(van_subtotal)       AS van,
  SUM(truck_subtotal)     AS truck,
  SUM(special_subtotal)   AS special
FROM sknfirst.car_registeration
WHERE report_month BETWEEN '2023-08-01' AND '2025-08-31';

-- 2. 차종 비중(%)
SELECT
  ROUND(100 * SUM(passenger_subtotal)/NULLIF(SUM(total_subtotal),0), 2) AS pct_passenger,
  ROUND(100 * SUM(van_subtotal)      /NULLIF(SUM(total_subtotal),0), 2) AS pct_van,
  ROUND(100 * SUM(truck_subtotal)    /NULLIF(SUM(total_subtotal),0), 2) AS pct_truck,
  ROUND(100 * SUM(special_subtotal)  /NULLIF(SUM(total_subtotal),0), 2) AS pct_special
FROM sknfirst.car_registeration
WHERE report_month BETWEEN '2023-08-01' AND '2025-08-31';
