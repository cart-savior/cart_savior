![](https://github.com/pje1740/cart_savior/blob/master/flask/static/images/team_banner.jpg?raw=true)  
내가 집어든 이 양파, 싼 걸까, 비싼걸까? 그 기준을 제시해 드립니다.

>서비스 개요 및 기획의도  
>참조 https://github.com/pje1740/cart_savior/wiki
![](https://github.com/pje1740/cart_savior/blob/master/sources/usage.gif?raw=true)  
---
### 협업 도구
- Messaging: Slack, Kakaotalk
- Code sharing: Github, Slack
- Productivity: Notion

### 개발 환경 및 언어
- Python: Flask, Pandas
- HTML, CSS, Javascript

### 배포 플랫폼
- AWS Beanstalk
- [AWS live url link](http://cartsavior-env.eba-8yqpfip2.ap-northeast-2.elasticbeanstalk.com/)

### 사용 데이터
농산물유통정보:::KAMIS

https://www.kamis.or.kr/customer/reference/openapi_list.do

---
## 기타 

### File Naming Convention
파일 업로드 시, 파일명 뒤에 작성자 아이디 추가. 소스코드는 제외.

ex) data_set_sohpark

ex) design_ui_jilim

ex) data_eda_dachung

### Kamis api url
기본 url 뒤에 옵션을 붙여서 필요한 정보를 추출할 수 있음. 
```
"http://www.kamis.or.kr/service/price/xml.do?action=dailyPriceByCategoryList" +\
"&p_cert_key=bceaf385-9d34-4a75-9c6f-0607eb325485&p_cert_id=pje1740&p_returntype=json" +\
```
여기까지는 수정할 필요 없음. 단, 데이터셋을 바꾸려면 action= 뒤를 변경해야 함.
```
"&p_product_cls_code=01" +\
"&p_regday=" + today_date +\
"&p_country_code=1101" +\
"&p_item_category_code=100"
```

참고 사이트
https://www.kamis.or.kr/customer/reference/openapi_list.do?action=detail&boardno=1


### Flask app 실행방법
1. flask 디렉토리 안의 app.py 를 실행시킨다 (python app.py)
2. 백그라운드에 실행시켜둔 채로 터미널에 뜬 주소로 접속하여 메인 페이지로 접속한다. 
3. 검색어를 입력해가며 테스트한다. 
4. 종료하는 경우 실행시킨 app.py를 ctrl+c로 종료시킨다. 
