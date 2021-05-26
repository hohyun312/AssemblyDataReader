`AssemblyDataReader`는 열린국회정보의 API를 이용해 데이터를 쉽게 받아올 수 있게 만든 오픈소스 라이브러리입니다. 이 라이브러리를 사용하기 위해서는 key를 발급 받아야 합니다.



# Installation

다음과 같이 입력하여 설치합니다.

`pip install assemblydatareader`

다음과 같이 입력하여 업그레이드합니다.

`pip install --upgrade assemblydatareader`



# Quick Start

```python
import AssemblyDataReader

# https://open.assembly.go.kr/portal/openapi/main.do에서 key 발급
api_key = 'xxxx'
adr = AssemblyDataReader(api_key)

# 가져오고 싶은 데이터 입력
adr.read('국회사무처 업무추진비 집행현황')
adr.read('국회도서관 업무추진비 집행현황')
adr.read('국회입법조사처 업무추진비 집행현황')
adr.read('국회예산정책처 업무추진비 집행현황')
adr.read('국회의원 세미나 일정')

# 대수를 입력해야 하는 데이터 목록
adr.read('국회의원 발의법률안', daesu=21)
adr.read('본회의 처리안건_법률안', daesu=21)
adr.read('본회의 처리안건_예산안', daesu=21)
adr.read('본회의 처리안건_결산', daesu=21)
adr.read('본회의 처리안건_기타', daesu=21)
adr.read('역대 국회의원 현황', daesu=21)
adr.read('역대 국회의원 인적사항', daesu=21)
adr.read('역대 국회의원 위원회 경력', daesu=21)
adr.read('의안별 표결현황', daesu=21)
adr.read('국회의원 소규모 연구용역 결과보고서', daesu=21)
adr.read('본회의 일정', daesu=21)

# 표결정보는 의안ID 입력 필요
adr.read('국회의원 본회의 표결정보', daesu=21, bill_id='PRC_A2H1K0K4I1G4X1Z7Q4W4S4N7E1W1F7')

# 날짜 입력 필요
adr.read('날짜별 의정활동', daesu=21, date='2020-08-18')

# 위 목록에 없는 API도 요청주소 뒷자리를 이용해 데이터를 가져올 수도 있습니다.
# 참고: https://open.assembly.go.kr/portal/data/service/selectAPIServicePage.do/OZN379001174FW17905
# NABO 경제재정수첩 가져오기
adr.read('ncnpwqimabagvdmky')

# 전체 API 목록 가져오기
adr.listing()

# {영어_컬럼명: 한국어_컬럼명} 보기
adr.en2kor

# 데이터 출력에 대한 더 자세한 사항은 아래에서 확인
# https://open.assembly.go.kr/portal/openapi/openApiNaListPage.do
```

