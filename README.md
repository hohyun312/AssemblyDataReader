`AssemblyDataReader`는 열린국회정보의 API를 이용해 데이터를 쉽게 받아올 수 있게 만든 오픈소스 라이브러리입니다. 이 라이브러리를 사용하기 위해서는 key를 발급 받아야 합니다.



# Installation

`pip install assemblydatareader`



# Quick Start

```
import AssemblyDataReader

# https://open.assembly.go.kr/portal/openapi/main.do에서 key 발급
api_key = 'xxxx'
adr = AssemblyDataReader(api_key)

# 21대 국회의원 발의법률안 보기
adr.read(21, '국회의원 발의법률안')

# 10대 국회의원 인적사항 보기
adr.read(10, '역대 국회의원 인적사항')

# 데이터 출력에 대한 더 자세한 사항은 아래에서 확인
# https://open.assembly.go.kr/portal/openapi/openApiNaListPage.do
```

