# cart_savior
A repository for 42 project related to grocery shopping
![](https://scontent-gmp1-1.xx.fbcdn.net/v/t1.0-9/68523665_920286595013777_8017496360037122048_n.jpg?_nc_cat=103&_nc_sid=8024bb&_nc_ohc=1nx5ANFV5MoAX9Cg5am&_nc_ht=scontent-gmp1-1.xx&oh=54e9a9a3083ff4ae8aa14cc5f796d79e&oe=5EC10CA4)
김치 짜다고 친구 머리 떼먹는 양파쿵야 인성 

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
