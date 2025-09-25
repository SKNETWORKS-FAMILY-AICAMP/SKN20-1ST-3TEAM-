-- 1. 회사 and 대분류 건수 카운트
SELECT
  faq_company, faq_major_category, COUNT(*) AS cnt
FROM sknfirst.faq
GROUP BY faq_company, faq_major_category
ORDER BY faq_company, cnt DESC;

-- 2. 키워드 검색 -- 차량정비는 왜 안 나옴??????
SELECT
  faq_id, faq_company, faq_major_category, faq_sub_category, faq_question, faq_answer
FROM sknfirst.faq
WHERE faq_question LIKE '%차량정비%' OR faq_answer LIKE '%모젠서비스%'
ORDER BY faq_id DESC
LIMIT 50;

