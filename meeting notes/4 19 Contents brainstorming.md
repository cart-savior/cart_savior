# [4/19] Contents brainstorming

Created: Apr 19, 2020 3:11 PM
Created By: Lana Chung
Last Edited Time: Apr 20, 2020 3:02 PM
Participants: SoHyun Park, Jiyoung Lim
Type: brainstorming

- 지금까지 한 것
    - 팀, 프로젝트 이름
    - 주제 정하기 → 장 볼 때 시세 알리기
    - 대략적인 개요 (ppt)

## 오늘 해야 할 것

- 서비스에 들어갈 구체적인 컨텐츠 == 대시보드 구성요소
- 깃헙 파기

[honeybeat1/cart_savior](https://github.com/honeybeat1/cart_savior)

## 대시보드 구성 요소

- **현 시점 기준 평균가 (기준 규격 포함) (가장 최신 데이터)**
    - 가장 적은 단위 (10개, 1kg 등)
    - 최근 조사일자
    - 상품 분류/카테고리
- 원본데이터 필드명
    - product_cls_code (01 소매, 02 도매)
    - category_name (부류명)
    - productName (품목명)
    - unit (단위)
    - day1 (최근 조사일자)
    - dpr1 (최근 조사일자 가격)
    - day3 (1개월전 일자)
    - dpr3 (1개월전 가격)
    - day4 (1년전 일자)
    - dpr4 (1년전 가격)
    - direction (등락여부) (0: 가격하락, 1:가격상승, 2:등락없음)
- More?
    - 지난 달, 작년 같은 달 평균가 비교?
    - 일년치 등락 데이터?
    - 판매처 종류, 지역별 평균가

## 데이터 뜯어보기

1. 출처 - 서울시 공공데이터
    - 서울시 것만 나옴
    - 품목 76개 (고등어 수입산, 고등어 국산 이렇게 나눠진거 포함)
    - 다양한 품목을 볼 수 없음
    - 마트 이름 (롯데마트, 이마트 등)이 나와 있고 자치구별로 나눠져 있어서 그 분류로 가격 비교는 할 수 있음
2. 농수산물 유통정보
    - 농수산물 밖에 없음.
    - 고기는 알아서 → 고기도 있음!
    - 가격 최근 조사일, 1달전, 1년전 비교 쉽게 가능
    - 단위 - 소매 가격만
    - 컨텐츠에 추가할만한 요소가 많아서 참고하기 좋음. [https://www.kamis.or.kr/customer/trend/economic/economic.do](https://www.kamis.or.kr/customer/trend/economic/economic.do)

[농산물유통정보:::KAMIS](https://www.kamis.or.kr/customer/reference/openapi_list.do)

![4%2019%20Contents%20brainstorming/Untitled.png](4%2019%20Contents%20brainstorming/Untitled.png)

카미스 샘플 데이터 

## When to meet

📆수요일 (4/22) 오후 12시

## To - do

- [ ]  @SoHyun Park 카미스 api 데이터 까보기, 장고 강의 듣기 (https, css)
- [ ]  @Jiyoung Lim 카트세이버 ux/ui 디자인
- [ ]  @Lana Chung 카미스 데이터 태블로로 뜯어보기, 원본 데이터 info 정리하기, 장고 튜토리얼 읽기

## 장고 & 리액트 참고 사이트

[[서버부터 프론트까지] React와 Django로 웹 서비스 뚝딱 세팅하기 (feat. Webpack, Redux, django rest framework, PWA) | Today Yurim Learned](http://milooy.github.io/TIL/Django/react-with-django-rest-framework.html#%EB%AA%A9%ED%91%9C)