# [4/20] data EDA

Created: Apr 20, 2020 4:29 PM
Created By: Lana Chung
Last Edited Time: Apr 20, 2020 6:01 PM
Participants: SoHyun Park
Type: EDA

# What did we do yesterday?

- 한국농수산식품유통공사(aT)에서 제공하는 api 신청
- 오늘 certificate key 발급 받음

# What will we do today?

- 제공하는 10가지 데이터 중 가장 우리 서비스에 이용할 수 있는 api 선정
- `일별 부류별 도.소매가격정보` 가 가장 우리 서비스에 적합하다고 판단 (`action=dailyPriceByCategoryList`)
    - 기존에 뜯어보려고 했던 `최근일자 도.소매가격정보(상품 기준)` 는 축산, 수산물 등의 자료가 누락되어 있기 때문에 웬만하면 다 들어있는 전자 자료로 선택
- 요청 url [`http://www.kamis.or.kr/service/price/xml.do?action=dailyPriceByCategoryList`](http://www.kamis.or.kr/service/price/xml.do?action=dailyPriceByCategoryList)

요청 parameter 중 `p_regday` 일요일 날짜는 조사 **내용이 없음**

- 일요일에 검색시 그 전날 데이터가 뜨도록 할 것
- 품목 수 (Unique) **75개**
    - 대분류) 식량작물(8개), 채소류(31개), 특용작물(8개), 과일류(16개), 축산물(5개), 수산물(17개)

 

# Potential blockers?

- 검색 기능?
    - 품목 수가 적기 때문에 어떻게 해야할까
    - 우리 서비스의 목적은 `이게 싸냐 비싸냐` 알 수 있게 하는 것
    - 검색 기능을 넣되 + `달래` 라고 쳤을 경우 `채소류`에서 랜덤하게 띄우게 해야 함 (뭘 쳤는데 맨날 너굴맨 나오면 안됨)
- 마켓컬리, SSG 등의 사이트 가격과 비교해보는 재미 (확실히 마켓컬리는 2배 가량이나 비싸다.)
- 대분류 별로 아이콘, 도트? (6가지)

# Action items

- [ ]  장고 튜토리얼