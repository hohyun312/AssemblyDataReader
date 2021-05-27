import requests
import pandas as pd
import json


class AssemblyDataReader:
    def __init__(self, key):
        self.api_key = key
        self.__api_ids = {
            '국회의원 발의법률안':'nzmimeepazxkubdpn',
            '본회의 처리안건_법률안':'nwbpacrgavhjryiph',
            '본회의 처리안건_예산안':'nzgjnvnraowulzqwl',
            '본회의 처리안건_결산':'nkalemivaqmoibxro',
            '본회의 처리안건_기타':'nbslryaradshbpbpm',
            '역대 국회의원 현황':'nprlapfmaufmqytet',
            '역대 국회의원 인적사항':'npffdutiapkzbfyvr',
            '역대 국회의원 위원회 경력':'nqbeopthavwwfbekw',
            '의안별 표결현황':'ncocpgfiaoituanbr',
            '국회의원 본회의 표결정보':'nojepdqqaweusdfbi',
            '국회사무처 업무추진비 집행현황':'nalacaiwauxiynsxt',
            '국회도서관 업무추진비 집행현황':'ngqoyjbkaxutcpmot',
            '국회입법조사처 업무추진비 집행현황':'nlmqzojlayoicbxhw',
            '국회예산정책처 업무추진비 집행현황':'nknmvzexapgiarqcd',
            '국회의원 세미나 일정':'nfcoioopazrwmjrgs',
            '국회의원 소규모 연구용역 결과보고서':'nfvmtaqoaldzhobsw',
            '날짜별 의정활동':'nqfvrbsdafrmuzixe',
            '본회의 일정':'nekcaiymatialqlxr'
        }
        with open('field.json', 'r') as f:
            self.en2kor = json.load(f)
            
    def __read(self, api_id, **kargs):
        url = 'https://open.assembly.go.kr/portal/openapi/' + api_id
        params = {
            'KEY':self.api_key,
            'pIndex':1,
            'Type':'json',
            'pSize':1000,
        }
        params.update(kargs)
        df = pd.DataFrame()
        total_count = float('inf')
        while len(df) < total_count:
            j = requests.get(url, params=params).json()
            assert 'RESULT' not in j, j['RESULT']['MESSAGE']
                
            total_count = j[api_id][0]['head'][0]['list_total_count']
            df = df.append(pd.DataFrame(j[api_id][1]['row']))
            params['pIndex'] += 1
        return df.reset_index(drop=True)
    
    def __get_params(self, key, daesu=None, **kargs):
        params = {}
        if key in {'국회의원 발의법률안', 
                   '본회의 처리안건_법률안', 
                   '본회의 처리안건_예산안', 
                   '본회의 처리안건_결산', 
                   '본회의 처리안건_기타',
                   '국회의원 본회의 표결정보',
                   '의안별 표결현황',
                   '날짜별 의정활동'}:
            assert not daesu is None, 'daesu 인자가 필요합니다.'
            params.update({'AGE':daesu})
            
        elif key in {'역대 국회의원 현황'}:
            assert not daesu is None, 'daesu 인자가 필요합니다.'
            params.update({'DAESU':daesu})
            
        elif key in {'역대 국회의원 인적사항',
                   '국회의원 소규모 연구용역 결과보고서',
                   '본회의 일정'}:
            assert not daesu is None, 'daesu 인자가 필요합니다.'
            UNIT_CD = '1'+str(daesu).zfill(5)
            params.update({'UNIT_CD':UNIT_CD})   
            
        elif key in {'역대 국회의원 위원회 경력'}:
            assert daesu is not None, 'daesu 인자가 필요합니다.'
            PROFILE_UNIT_CD = '1'+str(daesu).zfill(5)
            params.update({'PROFILE_UNIT_CD':PROFILE_UNIT_CD})   
        
        args = {k.lower() for k in kargs.keys()}
        if key in {'날짜별 의정활동'}:
            assert 'dt' in args, 'DT 인자가 필요합니다.'

        elif key in {'국회의원 본회의 표결정보'}:
            assert 'bill_id' in args, 'BILL_ID 인자가 필요합니다.'
        
        params.update(**kargs)    
            
        return params
    
    def read(self, key, daesu=None, **kargs): 
        '''
        가져오고 싶은 데이터 이름을 key에 적어주세요. 
        데이터에 따라 추가적인 인자가 필요할 수도 있습니다.
        
        21대 국회의원 발의법률안 가져오기
        >>> adr.read('국회의원 발의법률안', daesu=21)
        
        21대 2020년 8월 18일 의정활동 가져오기
        >>> adr.read('날짜별 의정활동', daesu=21, dt='2020-08-18')

        NABO 경제재정수첩 가져오기
        >>> adr.read('ncnpwqimabagvdmky')
        
        다음 링크에서 전체 예시를 볼 수 있습니다.
        https://github.com/hohyun321/AssemblyDataReader
        
        * key (str): 다음 중에서 선택. 또는 요청 주소 뒷자리 입력.
            '국회사무처 업무추진비 집행현황'
            '국회도서관 업무추진비 집행현황'
            '국회입법조사처 업무추진비 집행현황'
            '국회예산정책처 업무추진비 집행현황'
            '국회의원 세미나 일정'
            '국회의원 발의법률안'
            '본회의 처리안건_법률안'
            '본회의 처리안건_예산안'
            '본회의 처리안건_결산'
            '본회의 처리안건_기타'
            '역대 국회의원 현황'
            '역대 국회의원 인적사항'
            '역대 국회의원 위원회 경력'
            '의안별 표결현황'
            '국회의원 소규모 연구용역 결과보고서'
            '본회의 일정'    
            '국회의원 본회의 표결정보'
            '날짜별 의정활동'
        * daesu (int): 대수
        
        선택적으로 추가 인자를 줄 수 있습니다. API 제공 사이트를 참조하세요.
        https://open.assembly.go.kr/portal/openapi/openApiNaListPage.do
        '''
        if key in self.__api_ids:
            api_id = self.__api_ids[key]
        else:
            api_id = key
        params = self.__get_params(key, daesu=daesu, **kargs)
        return self.__read(api_id, **params)
    
    def listing(self):
        '''
        API 전체 목록을 가져옵니다.
        
        https://open.assembly.go.kr/portal/openapi/openApiNaListPage.do
        '''
        url  = 'https://open.assembly.go.kr/portal/openapi/selectInfsOpenApiListPaging.do'
        headers = {'User-Agent': 'Mozilla/5.0'}
        form_data = {'rows': 500, 'page':1}
        r = requests.post(url, data=form_data, headers=headers)
        data = r.json()['data']
        df = pd.DataFrame(data)
        col = ['infaNm', 'cateNm', 'orgNm', 'infaExp', 'openYmd']
        return df[col]