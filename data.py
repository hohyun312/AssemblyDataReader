import requests
import pandas as pd


class AssemblyDataReader:
    def __init__(self, key):
        self.api_key = key
        
    def __read(self, url, kargs):
        api_id = url.split('/')[-1]
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
            if 'RESULT' in j:
                return j['RESULT']['MESSAGE']
            total_count = j[api_id][0]['head'][0]['list_total_count']
            df = df.append(pd.DataFrame(j[api_id][1]['row']))
            params['pIndex'] += 1
        return df.reset_index(drop=True)
    
    def read(self, daesu, key, bill_id=None, **kargs): 
        '''
        * daesu (int): 대수
        * key (str): 
            '국회의원 발의법률안'
            '본회의 처리안건_법률안'
            '본회의 처리안건_예산안' 
            '본회의 처리안건_결산'
            '본회의 처리안건_기타'
            '역대 국회의원 현황'
            '역대 국회의원 인적사항'
            '역대 국회의원 위원회 경력'
            '의안별 표결현황'
            '국회의원 본회의 표결정보': bill_id 인자 필요
                    
        '''
        if key == '국회의원 발의법률안':
            url = 'https://open.assembly.go.kr/portal/openapi/nzmimeepazxkubdpn'
            param = {'AGE':daesu, **kargs}
        elif key == '본회의 처리안건_법률안':
            url = 'https://open.assembly.go.kr/portal/openapi/nwbpacrgavhjryiph'
            param = {'AGE':daesu, **kargs}
        elif key == '본회의 처리안건_예산안':
            url = 'https://open.assembly.go.kr/portal/openapi/nzgjnvnraowulzqwl'
            param = {'AGE':daesu, **kargs}
        elif key == '본회의 처리안건_결산':
            url = 'https://open.assembly.go.kr/portal/openapi/nkalemivaqmoibxro'
            param = {'AGE':daesu, **kargs}
        elif key == '본회의 처리안건_기타':
            url = 'https://open.assembly.go.kr/portal/openapi/nbslryaradshbpbpm'
            param = {'AGE':daesu, **kargs} 
        elif key == '역대 국회의원 현황':
            url = 'https://open.assembly.go.kr/portal/openapi/nprlapfmaufmqytet'
            param = {'DAESU':daesu, **kargs}    
        elif key == '역대 국회의원 인적사항':
            UNIT_CD = '1'+str(daesu).zfill(5)
            url = 'https://open.assembly.go.kr/portal/openapi/npffdutiapkzbfyvr'
            param = {'UNIT_CD':UNIT_CD, **kargs}   
        elif key == '역대 국회의원 위원회 경력':
            PROFILE_UNIT_CD = '1'+str(daesu).zfill(5)
            url = 'https://open.assembly.go.kr/portal/openapi/nqbeopthavwwfbekw'
            param = {'PROFILE_UNIT_CD':PROFILE_UNIT_CD, **kargs}   
        elif key == '의안별 표결현황':
            url = 'https://open.assembly.go.kr/portal/openapi/ncocpgfiaoituanbr'
            param = {'AGE':daesu, **kargs} 
        elif key == '국회의원 본회의 표결정보':
            assert bill_id is not None, 'bill_id 정보가 필요합니다.'
            url = 'https://open.assembly.go.kr/portal/openapi/nojepdqqaweusdfbi'
            param = {'AGE':daesu, 'BILL_ID':bill_id, **kargs} 
        else:
            assert False, 'key가 올바르지 않습니다.'
            
        return self.__read(url, param)