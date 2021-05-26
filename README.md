`AssemblyDataReader`는 열린국회정보의 API를 이용해 데이터를 쉽게 받아올 수 있게 만든 오픈소스 라이브러리입니다. 이 라이브러리를 사용하기 위해서는 key를 발급 받아야 합니다.



# Installation

`pip install assemblydatareader`



# Quick Start

```python
import AssemblyDataReader

# https://open.assembly.go.kr/portal/openapi/main.do에서 key 발급
api_key = 'xxxx'
adr = AssemblyDataReader(api_key)

# 21대 국회의원 발의법률안 가져오기
adr.read('국회의원 발의법률안', daesu=21)

# 10대 국회의원 인적사항 가져오기
adr.read('역대 국회의원 인적사항', daesu=10)

# 21대 2020년 8월 18일 의정활동 가져오기
adr.read('날짜별 의정활동', daesu=21, date='2020-08-18')

# NABO 경제재정수첩 가져오기
# 참고: https://open.assembly.go.kr/portal/data/service/selectAPIServicePage.do/OZN379001174FW17905
adr.read('ncnpwqimabagvdmky')

# 전체 API 목록 가져오기
adr.listing()

# {영어_컬럼명: 한국어_컬럼명} 보기 (일부만 있음)
adr.en_kor_field

# 데이터 출력에 대한 더 자세한 사항은 아래에서 확인
# https://open.assembly.go.kr/portal/openapi/openApiNaListPage.do
```

