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
        self.en2kor = {'MEETINGSESSION': '회기',
                     'CHA': '차수',
                     'TITLE': '제목',
                     'MEETTING_DATE': '일자',
                     'MEETTING_TIME': '일시',
                     'UNIT_CD': '대별코드',
                     'UNIT_NM': '대',
                     'SEQ': '순번',
                     'DT': '일자',
                     'BILL_KIND': '의안활동구분',
                     'AGE': '대수',
                     'BILL_NO': '의안번호',
                     'BILL_NM': '의안명',
                     'STAGE': '단계',
                     'DTL_STAGE': '세부단계',
                     'COMMITTEE': '소관위원회',
                     'ACT_STATUS': '활동상태',
                     'BILL_ID': '의안ID',
                     'LINK_URL': '링크URL',
                     'COMMITTEE_ID': '소관위원회ID',
                     'RPT_NO': '다운로드',
                     'YEAR': '년도',
                     'FILE_ID': '파일ID',
                     'RPT_TITLE': '보고서제목',
                     'RG_DE': '등록일',
                     'ASBLM_NM': '의원명',
                     'QUARTER': '분기',
                     'DIV_NM': '구분명',
                     'LINK': '의원실링크',
                     'DESCRIPTION': '설명',
                     'SDATE': '개최일',
                     'STIME': '개최시간',
                     'NAME': '이름',
                     'LOCATION': '개최장소',
                     'PRDC_YM_NM': '생산년월',
                     'OPB_FL_NM': '공개파일명',
                     'INST_CD': '기관코드',
                     'INST_NM': '기관명',
                     'OPB_FL_PH': '공개파일경로',
                     'HG_NM': '이름',
                     'HJ_NM': '한자명',
                     'POLY_NM': '정당명',
                     'MEMBER_NO': '의원번호',
                     'POLY_CD': '소속정당코드',
                     'ORIG_CD': '선거구코드',
                     'VOTE_DATE': '의결일자',
                     'BILL_NAME': '의안명',
                     'LAW_TITLE': '법률명',
                     'CURR_COMMITTEE': '소관위',
                     'RESULT_VOTE_MOD': '표결결과',
                     'DEPT_CD': '부서코드(사용안함)',
                     'CURR_COMMITTEE_ID': '소관위원회ID',
                     'DISP_ORDER': '표시정렬순서',
                     'BILL_URL': '의안URL',
                     'BILL_NAME_URL': '의안링크',
                     'SESSION_CD': '회기',
                     'CURRENTS_CD': '차수',
                     'MONA_CD': '국회의원코드',
                     'PROC_DT': '처리일',
                     'PROC_RESULT_CD': '의결결과',
                     'BILL_KIND_CD': '의안종류',
                     'MEMBER_TCNT': '재적의원',
                     'VOTE_TCNT': '총투표수',
                     'YES_TCNT': '찬성',
                     'NO_TCNT': '반대',
                     'BLANK_TCNT': '기권',
                     'PROFILE_CD': '구분코드',
                     'PROFILE_NM': '구분',
                     'FRTO_DATE': '활동기간',
                     'PROFILE_SJ': '위원회 경력',
                     'PROFILE_UNIT_CD': '경력대수코드',
                     'PROFILE_UNIT_NM': '경력대수',
                     'ENG_NM': '영문명칭',
                     'BTH_GBN_NM': '음/양력',
                     'BTH_DATE': '생년월일',
                     'SEX_GBN_NM': '성별',
                     'REELE_GBN_NM': '재선',
                     'UNITS': '당선',
                     'ORIG_NM': '선거구',
                     'ELECT_GBN_NM': '선거구구분',
                     'PROPOSE_DT': '제안일',
                     'PROC_RESULT': '처리상태',
                     'DETAIL_LINK': '상세페이지',
                     'PROPOSER': '제안자',
                     'MEMBER_LIST': '제안자목록링크',
                     'RST_PROPOSER': '대표발의자',
                     'PUBL_PROPOSER': '공동발의자',
                     'COMMITTEE_NM': '소관위원회',
                     'COMMITTEE_SUBMIT_DT': '위원회심사_회부일',
                     'COMMITTEE_PRESENT_DT': '위원회심사_상정일',
                     'COMMITTEE_PROC_DT': '위원회심사_의결일',
                     'LAW_SUBMIT_DT': '법사위체계자구심사_회부일',
                     'LAW_PRESENT_DT': '법사위체계자구심사_상정일',
                     'LAW_PROC_DT': '법사위체계자구심사_의결일',
                     'RGS_PRESENT_DT': '본회의심의_상정일',
                     'RGS_PROC_DT': '본회의심의_의결일',
                     'CURR_TRANS_DT': '정부이송일',
                     'ANNOUNCE_DT': '공포일',
                     'BDG_SUBMIT_DT': '예결위심사_회부일',
                     'BDG_PRESENT_DT': '예결위심사_상정일',
                     'BDG_PROC_DT': '예결위심사_의결일',
                     'PROPOSER_KIND_CD': '제안자구분',
                     'DAESU': '대수',
                     'DAE': '대별 및 소속정당(단체)',
                     'DAE_NM': '대별',
                     'NAME_HAN': '이름(한자)',
                     'JA': '자',
                     'HO': '호',
                     'BIRTH': '생년월일',
                     'BON': '본관',
                     'POSI': '출생지',
                     'HAK': '학력 및 경력',
                     'HOBBY': '종교 및 취미',
                     'BOOK': '저서',
                     'SANG': '상훈',
                     'DEAD': '기타정보(사망일)',
                     'URL': '회원정보 확인 헌정회 홈페이지 URL'}
            
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