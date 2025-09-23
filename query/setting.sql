-- 조회 기본 조인 뷰(임시): 월, 지역명 포함
SELECT
  c.car_id, c.report_month,
  r.sido, r.sigungu, c.region_id,
  c.passenger_subtotal, c.van_subtotal, c.truck_subtotal, c.special_subtotal,
  c.total_official, c.total_private, c.total_commercial, c.total_subtotal
FROM sknfirst.car_registeration c
JOIN sknfirst.region r ON r.region_id = c.region_id;

-- 권장 인덱스 (자주 쓰는 필터/그룹)
CREATE INDEX ix_car_month                 ON sknfirst.car_registeration (report_month);
CREATE INDEX ix_car_region_month          ON sknfirst.car_registeration (region_id, report_month);
CREATE INDEX ix_region_sido_sigungu       ON sknfirst.region (sido, sigungu);
