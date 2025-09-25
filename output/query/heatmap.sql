-- 히트맵 시각화: rows=월, columns=시도
-- region_id 순서대로 프레임 만들고 싶었는데 실패했다는  ..
SELECT 
  DATE_FORMAT(c.report_month, '%Y-%m') AS ym,
  SUM(IF(r.sido='서울', c.total_subtotal, 0)) AS 서울,
  SUM(IF(r.sido='부산', c.total_subtotal, 0)) AS 부산,
  SUM(IF(r.sido='경기', c.total_subtotal, 0)) AS 경기,
  SUM(IF(r.sido='인천', c.total_subtotal, 0)) AS 인천,
  SUM(IF(r.sido='강원', c.total_subtotal, 0)) AS 강원,
  SUM(IF(r.sido='경남', c.total_subtotal, 0)) AS 경남,
  SUM(IF(r.sido='경북', c.total_subtotal, 0)) AS 경북,
  SUM(IF(r.sido='전남', c.total_subtotal, 0)) AS 전남,
  SUM(IF(r.sido='전북', c.total_subtotal, 0)) AS 전북,
  SUM(IF(r.sido='대구', c.total_subtotal, 0)) AS 대구,
  SUM(IF(r.sido='대전', c.total_subtotal, 0)) AS 대전,
  SUM(IF(r.sido='충북', c.total_subtotal, 0)) AS 충북,
  SUM(IF(r.sido='충남', c.total_subtotal, 0)) AS 충남,
  SUM(IF(r.sido='제주', c.total_subtotal, 0)) AS 제주
  
FROM car_registeration c
JOIN region r ON r.region_id = c.region_id
WHERE c.report_month BETWEEN '2023-08-01' AND '2025-08-31'
GROUP BY ym
ORDER BY ym; 
