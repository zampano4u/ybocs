import streamlit as st
import streamlit.components.v1 as components

# 참고문헌:
# Goodman, W. K., Price, L. H., Rasmussen, S. A., Mazure, C., Fleischmann, R. L.,
# Hill, C. L., Heninger, G. R., & Charney, D. S. (1989). The Yale-Brown Obsessive Compulsive Scale: I.
# Development, use, and reliability. Archives of General Psychiatry, 46(11), 1006-1011.

# 도입 증상 체크리스트용 한영 매핑 구조 (Y-BOCS 데이터 기반)
ybo_cs_mapping = {
    "aggressive_obsessions": {
        "question_ko": "공격 관련 강박사고",
        "question_en": "AGGRESSIVE OBSESSIONS",
        "items": [
            {"ko": "자신에게 해를 입힐지도 모른다는 두려움", "en": "Fear might harm self"},
            {"ko": "타인에게 해를 입힐지도 모른다는 두려움", "en": "Fear might harm others"},
            {"ko": "폭력적이거나 끔찍한 이미지", "en": "Violent or horrific images"},
            {"ko": "욕설이나 모욕적인 말을 갑자기 내뱉을지도 모른다는 두려움", "en": "Fear of blurting out obscenities or insults"},
            {"ko": "다른 당혹스러운 행동을 할지도 모른다는 두려움", "en": "Fear of doing something else embarrassing"},
            {"ko": "원치 않는 충동(예: 친구를 찌를 것 같은 충동)을 실행할지도 모른다는 두려움", "en": "Fear will act on unwanted impulses (e.g., to stab friend)"},
            {"ko": "물건을 훔칠지도 모른다는 두려움", "en": "Fear will steal things"},
            {"ko": "자신이 충분히 조심하지 않아 타인에게 해를 입힐지도 모른다는 두려움 (예: 뺑소니 사고)", "en": "Fear will harm others because not careful enough (e.g., hit/run MVA)"},
            {"ko": "자신이 어떤 끔찍한 일(예: 화재, 도난 등)에 책임이 있을지도 모른다는 두려움", "en": "Fear will be responsible for something else terrible happening (e.g., fire, burglary)"},
            {"ko": "기타", "en": "Other"}
        ]
    },
    "contamination_obsessions": {
        "question_ko": "오염 관련 강박사고",
        "question_en": "CONTAMINATION OBSESSIONS",
        "items": [
            {"ko": "체액이나 분비물(예: 소변, 대변, 침 등)에 대한 혐오감 또는 염려", "en": "Concerns or disgust with bodily waste or secretions (e.g., urine, feces, saliva)"},
            {"ko": "먼지나 세균에 대한 걱정", "en": "Concern with dirt or germs"},
            {"ko": "환경 오염물질(예: 석면, 방사능, 유독 폐기물 등)에 대한 과도한 걱정", "en": "Excessive concern with environmental contaminants (e.g., asbestos, radiation, toxic waste)"},
            {"ko": "가정용 물품(예: 세정제, 용제 등)에 대한 과도한 걱정", "en": "Excessive concern with household items (e.g., cleansers, solvents)"},
            {"ko": "동물(예: 곤충 등)에 대한 과도한 걱정", "en": "Excessive concern with animals (e.g., insects)"},
            {"ko": "끈적끈적한 물질이나 잔여물에 대한 불쾌감", "en": "Bothered by sticky substances or residues"},
            {"ko": "오염물질로 인해 병에 걸릴지도 모른다는 걱정", "en": "Concerned will get ill because of contaminant"},
            {"ko": "자신이 오염을 퍼뜨려 타인을 병들게 할지도 모른다는 걱정 (공격적)", "en": "Concerned will get others ill by spreading contaminant (Aggressive)"},
            {"ko": "오염의 결과보다는 그 느낌 자체에 대해 불쾌감을 느끼는 경우", "en": "No concern with consequences of contamination other than how it might feel"},
            {"ko": "기타", "en": "Other"}
        ]
    },
    "sexual_obsessions": {
        "question_ko": "성적 강박사고",
        "question_en": "SEXUAL OBSESSIONS",
        "items": [
            {"ko": "금기되거나 일탈적인 성적 생각, 이미지 또는 충동", "en": "Forbidden or perverse sexual thoughts, images, or impulses"},
            {"ko": "아동이나 근친상간을 포함한 내용", "en": "Content involves children or incest"},
            {"ko": "동성애와 관련된 내용", "en": "Content involves homosexuality"},
            {"ko": "타인을 대상으로 한 성적 행동 (공격적)", "en": "Sexual behavior toward others (Aggressive)"},
            {"ko": "기타", "en": "Other"}
        ]
    },
    "hoarding_saving_obsessions": {
        "question_ko": "저장/보존 강박사고",
        "question_en": "HOARDING/SAVING OBSESSIONS",
        "items": [
            {"ko": "저장/보존 강박사고 [취미나 금전적 또는 정서적 가치가 있는 물건에 대한 관심과 구별해야 합니다]", 
             "en": "HOARDING/SAVING OBSESSIONS [distinguish from hobbies and concern with objects of monetary or sentimental value]"}
        ]
    },
    "religious_obsessions": {
        "question_ko": "종교적 강박사고",
        "question_en": "RELIGIOUS OBSESSIONS",
        "items": [
            {"ko": "(신앙적 엄격성) 신성모독이나 불경에 대한 걱정", "en": "(Scrupulosity) Concerned with sacrilege and blasphemy"},
            {"ko": "옳고 그름, 도덕성에 대한 과도한 걱정", "en": "Excess concern with right/wrong, morality"},
            {"ko": "기타", "en": "Other"}
        ]
    },
    "symmetry_exactness_obsession": {
        "question_ko": "대칭 또는 정확성에 대한 강박사고",
        "question_en": "OBSESSION WITH NEED FOR SYMMETRY OR EXACTNESS",
        "items": [
            {"ko": "마법적 사고를 동반하는 경우 (예: 물건이 제자리에 놓이지 않으면 어머니에게 사고가 날 것 같은 생각)", 
             "en": "Accompanied by magical thinking (e.g., concerned the mother will have accident unless things are in the right place)"},
            {"ko": "마법적 사고를 동반하지 않는 경우", "en": "Not accompanied by magical thinking"}
        ]
    },
    "miscellaneous_obsessions": {
        "question_ko": "기타 강박사고",
        "question_en": "MISCELLANEOUS OBSESSIONS",
        "items": [
            {"ko": "알아야 한다거나 기억해야 한다는 필요성", "en": "Need to know or remember"},
            {"ko": "특정 말을 말하는 것에 대한 두려움", "en": "Fear of saying certain things"},
            {"ko": "정확하게 말을 하지 않으면 안 된다는 두려움", "en": "Fear of not saying just the right thing"},
            {"ko": "물건을 잃어버릴지도 모른다는 두려움", "en": "Fear of losing things"},
            {"ko": "침습적인(비폭력적) 이미지", "en": "Intrusive (non-violent) images"},
            {"ko": "침습적인 무의미한 소리, 단어 또는 음악", "en": "Intrusive nonsense sounds, words, or music"},
            {"ko": "특정 소리나 소음에 대한 불쾌감 *", "en": "Bothered by certain sounds/noises *"},
            {"ko": "행운/불운을 상징하는 숫자", "en": "Lucky/unlucky numbers"},
            {"ko": "특별한 의미가 있는 색깔", "en": "Colors with special significance"},
            {"ko": "미신적 공포", "en": "Superstitious fears"}
        ]
    },
    "somatic_obsessions": {
        "question_ko": "신체 관련 강박사고",
        "question_en": "SOMATIC OBSESSIONS",
        "items": [
            {"ko": "질병이나 병에 대한 걱정 *", "en": "Concern with illness or disease *"},
            {"ko": "신체 일부나 외모에 대한 과도한 걱정 (예: 신체이형장애) *", "en": "Excessive concern with body part or aspect of appearance (e.g., dysmorphophobia) *"},
            {"ko": "기타", "en": "Other"}
        ]
    },
    "cleaning_washing_compulsions": {
        "question_ko": "청결/세척 강박행동",
        "question_en": "CLEANING/WASHING COMPULSIONS",
        "items": [
            {"ko": "과도하거나 의례적인 손 씻기", "en": "Excessive or ritualized handwashing"},
            {"ko": "과도하거나 의례적인 샤워, 목욕, 양치, 미용 또는 화장실 습관", "en": "Excessive or ritualized showering, bathing, toothbrushing, grooming, or toilet routine"},
            {"ko": "가정용 물품이나 무생물에 대한 청소", "en": "Involves cleaning of household items or other inanimate objects"},
            {"ko": "오염 물질과의 접촉을 방지하거나 제거하기 위한 기타 행동", "en": "Other measures to prevent or remove contact with contaminants"},
            {"ko": "기타", "en": "Other"}
        ]
    },
    "checking_compulsions": {
        "question_ko": "확인 강박행동",
        "question_en": "CHECKING COMPULSIONS",
        "items": [
            {"ko": "자물쇠, 가스레인지, 가전제품 등을 확인", "en": "Checking locks, stove, appliances, etc."},
            {"ko": "타인에게 해를 끼치지 않았는지 또는 끼치지 않을 것인지 확인", "en": "Checking that did not/will not harm others"},
            {"ko": "자신에게 해를 끼치지 않았는지 또는 끼치지 않을 것인지 확인", "en": "Checking that did not/will not harm self"},
            {"ko": "끔찍한 일이 발생하지 않았는지 또는 발생하지 않을 것인지 확인", "en": "Checking that nothing terrible did/will happen"},
            {"ko": "실수를 하지 않았는지 확인", "en": "Checking that did not make mistake"},
            {"ko": "신체 관련 강박사고와 연관된 확인", "en": "Checking tied to somatic obsessions"},
            {"ko": "기타", "en": "Other"}
        ]
    },
    "repeating_rituals": {
        "question_ko": "반복 의례행동",
        "question_en": "REPEATING RITUALS",
        "items": [
            {"ko": "다시 읽기 또는 다시 쓰기", "en": "Re-reading or re-writing"},
            {"ko": "일상 활동을 반복해야 하는 필요성 (예: 문을 들어갔다 나왔다, 의자에서 일어났다 앉았다)", "en": "Need to repeat routine activities (e.g., in/out door, up/down from chair)"},
            {"ko": "기타", "en": "Other"}
        ]
    },
    "counting_compulsions": {
        "question_ko": "숫자 세기 강박행동",
        "question_en": "COUNTING COMPULSIONS",
        "items": [
            {"ko": "숫자 세기 강박행동", "en": "COUNTING COMPULSIONS"}
        ]
    },
    "ordering_arranging_compulsions": {
        "question_ko": "정리/배열 강박행동",
        "question_en": "ORDERING/ARRANGING COMPULSIONS",
        "items": [
            {"ko": "정리/배열 강박행동", "en": "ORDERING/ARRANGING COMPULSIONS"}
        ]
    },
    "hoarding_collecting_compulsions": {
        "question_ko": "저장/수집 강박행동",
        "question_en": "HOARDING/COLLECTING COMPULSIONS",
        "items": [
            {"ko": "저장/수집 강박행동 [취미나 금전적 또는 정서적 가치가 있는 물건에 대한 관심과 구별되어야 함 (예: 광고지를 꼼꼼히 읽기, 오래된 신문을 쌓아두기, 쓰레기를 분류하기, 쓸모없는 물건을 모으기 등)]",
             "en": "HOARDING/COLLECTING COMPULSIONS [distinguish from hobbies and concern with objects of monetary or sentimental value (e.g., carefully reads junk mail, piles up old newspapers, sorts through garbage, collects useless objects)]"}
        ]
    },
    "miscellaneous_compulsions": {
        "question_ko": "기타 강박행동",
        "question_en": "MISCELLANEOUS COMPULSIONS",
        "items": [
            {"ko": "확인이나 숫자 세기를 제외한 정신적 의례행동", "en": "Mental rituals (other than checking/counting)"},
            {"ko": "과도한 목록 작성", "en": "Excessive listmaking"},
            {"ko": "말하기, 질문하기, 고백해야 할 필요성", "en": "Need to tell, ask, or confess"},
            {"ko": "만지기, 두드리기, 문지르기 등의 필요성 *", "en": "Need to touch, tap, or rub *"},
            {"ko": "깜박이거나 응시하는 의례행동 *", "en": "Rituals involving blinking or staring *"},
            {"ko": "자신에게 해를 입히는 것, 타인에게 해를 입히는 것, 끔찍한 결과 발생을 방지하기 위한 행동 (확인 행동 제외)", "en": "Measures (not checking) to prevent: harm to self, harm to others, terrible consequences"},
            {"ko": "의례적인 식사 행동 *", "en": "Ritualized eating behaviors *"},
            {"ko": "미신적 행동", "en": "Superstitious behaviors"}
        ]
    }
}

# 평가 문항 및 선택지 데이터 구조 (Y-BOCS 평가 척도)
y_bocs_scale = [
    {
        "id": 1,
        "question_ko": "강박 사고에 소비되는 시간",
        "question_en": "TIME OCCUPIED BY OBSESSIVE THOUGHTS",
        "description_ko": "귀하의 강박 사고가 귀하의 시간을 얼마나 많이 차지하고 있습니까?",
        "description_en": "How much of your time is occupied by obsessive thoughts?",
        "options": [
            {"score": 0, "response_text_ko": "전혀 없음", "response_text_en": "None"},
            {"score": 1, "response_text_ko": "하루에 1시간 미만 또는 가끔 발생함", "response_text_en": "Less than 1 hr/day or occasional occurrence"},
            {"score": 2, "response_text_ko": "하루 1~3시간 또는 자주 발생함", "response_text_en": "1 to 3 hrs/day or frequent"},
            {"score": 3, "response_text_ko": "하루 3시간 초과 8시간 이하 또는 매우 자주 발생함", "response_text_en": "Greater than 3 and up to 8 hrs/day or very frequent occurrence"},
            {"score": 4, "response_text_ko": "하루 8시간 초과 또는 거의 지속적으로 발생함", "response_text_en": "Greater than 8 hrs/day or nearly constant occurrence"}
        ]
    },
    {
        "id": 2,
        "question_ko": "강박 사고로 인한 기능적 방해",
        "question_en": "INTERFERENCE DUE TO OBSESSIVE THOUGHTS",
        "description_ko": "귀하의 강박 사고가 귀하의 업무, 학업, 사회생활 또는 기타 중요한 역할 수행에 얼마나 방해가 됩니까? 그로 인해 하지 못하는 일이 있습니까?",
        "description_en": "How much do your obsessive thoughts interfere with your work, school, social, or other important role functioning? Is there anything that you don’t do because of them?",
        "options": [
            {"score": 0, "response_text_ko": "전혀 없음", "response_text_en": "None"},
            {"score": 1, "response_text_ko": "사회적 또는 기타 활동에 약간의 방해가 있으나, 전반적인 수행에는 지장이 없음", "response_text_en": "Slight interference with social or other activities, but overall performance not impaired"},
            {"score": 2, "response_text_ko": "사회적 또는 직업적 수행에 명확한 방해가 있으나, 여전히 감당 가능함", "response_text_en": "Definite interference with social or occupational performance, but still manageable"},
            {"score": 3, "response_text_ko": "사회적 또는 직업적 수행에 상당한 손상이 있음", "response_text_en": "Causes substantial impairment in social or occupational performance"},
            {"score": 4, "response_text_ko": "수행 능력이 완전히 마비될 정도로 심각한 방해가 있음", "response_text_en": "Incapacitating"}
        ]
    },
    {
        "id": 3,
        "question_ko": "강박 사고로 인한 고통의 정도",
        "question_en": "DISTRESS ASSOCIATED WITH OBSESSIVE THOUGHTS",
        "description_ko": "귀하의 강박 사고는 귀하에게 어느 정도의 고통을 유발합니까?",
        "description_en": "How much distress do your obsessive thoughts cause you?",
        "options": [
            {"score": 0, "response_text_ko": "전혀 없음", "response_text_en": "None"},
            {"score": 1, "response_text_ko": "그다지 괴롭지 않음", "response_text_en": "Not too disturbing"},
            {"score": 2, "response_text_ko": "괴롭긴 하나 여전히 감당 가능함", "response_text_en": "Disturbing, but still manageable"},
            {"score": 3, "response_text_ko": "매우 괴로움", "response_text_en": "Very disturbing"},
            {"score": 4, "response_text_ko": "거의 지속적으로 심각한 고통을 유발하며 일상 기능을 저해함", "response_text_en": "Near constant and disabling distress"}
        ]
    },
    {
        "id": 4,
        "question_ko": "강박 사고에 대한 저항 노력",
        "question_en": "RESISTANCE AGAINST OBSESSIONS",
        "description_ko": "귀하가 강박 사고에 저항하려는 노력은 어느 정도입니까? 이러한 사고가 떠오를 때, 얼마나 자주 이를 무시하거나 주의를 다른 데로 돌리려고 하십니까?",
        "description_en": "How much of an effort do you make to resist the obsessive thoughts? How often do you try to disregard or turn your attention away from these thoughts as they enter your mind?",
        "options": [
            {"score": 0, "response_text_ko": "항상 저항하려고 노력함", "response_text_en": "Try to resist all the time"},
            {"score": 1, "response_text_ko": "대부분의 시간에 저항하려고 노력함", "response_text_en": "Try to resist most of the time"},
            {"score": 2, "response_text_ko": "어느 정도 저항하려는 노력을 함", "response_text_en": "Make some effort to resist"},
            {"score": 3, "response_text_ko": "저항하려 하지 않고 모든 강박 사고에 굴복하나, 약간의 꺼림칙함은 있음", "response_text_en": "Yield to all obsessions without attempting to control them, but with some reluctance"},
            {"score": 4, "response_text_ko": "완전히 자발적으로 모든 강박 사고에 굴복함", "response_text_en": "Completely and willingly yield to all obsessions"}
        ]
    },
    {
        "id": 5,
        "question_ko": "강박 사고에 대한 통제력",
        "question_en": "DEGREE OF CONTROL OVER OBSESSIVE THOUGHTS",
        "description_ko": "귀하는 자신의 강박 사고를 얼마나 통제할 수 있습니까? 강박적인 생각을 중단하거나 다른 데로 돌리는 데 어느 정도 성공하십니까? 이러한 생각을 떨쳐낼 수 있습니까?",
        "description_en": "How much control do you have over your obsessive thoughts? How successful are you in stopping or diverting your obsessive thinking? Can you dismiss them?",
        "options": [
            {"score": 0, "response_text_ko": "완전히 통제 가능함", "response_text_en": "Complete control"},
            {"score": 1, "response_text_ko": "약간의 노력과 집중을 통해 대체로 중단하거나 방향 전환이 가능함", "response_text_en": "Usually able to stop or divert obsessions with some effort and concentration"},
            {"score": 2, "response_text_ko": "때때로 중단하거나 방향 전환이 가능함", "response_text_en": "Sometimes able to stop or divert obsessions"},
            {"score": 3, "response_text_ko": "거의 중단하거나 떨쳐내지 못하며, 주의 전환에도 큰 어려움을 느낌", "response_text_en": "Rarely successful in stopping or dismissing obsessions, can only divert attention with difficulty"},
            {"score": 4, "response_text_ko": "강박 사고는 완전히 비자발적으로 일어나며, 순간적으로라도 이를 변화시키는 것이 거의 불가능함", "response_text_en": "Obsessions are completely involuntary, rarely able to even momentarily alter obsessive thinking."}
        ]
    },
    {
        "id": 6,
        "question_ko": "강박 행동에 소비되는 시간",
        "question_en": "TIME SPENT PERFORMING COMPULSIVE BEHAVIORS",
        "description_ko": "귀하가 강박 행동을 수행하는 데 어느 정도의 시간을 쓰고 있습니까? 일상적인 활동을 마치는 데 다른 사람보다 시간이 얼마나 더 걸립니까? 의례적 행동(ritual)을 얼마나 자주 수행하십니까?",
        "description_en": "How much time do you spend performing compulsive behaviors? How much longer than most people does it take to complete routine activities because of your rituals? How frequently do you do rituals?",
        "options": [
            {"score": 0, "response_text_ko": "전혀 없음", "response_text_en": "None"},
            {"score": 1, "response_text_ko": "하루에 1시간 미만 또는 가끔 강박 행동을 수행함", "response_text_en": "Less than 1 hr/day or occasional performance of compulsive behaviors"},
            {"score": 2, "response_text_ko": "하루 1~3시간 또는 자주 강박 행동을 수행함", "response_text_en": "1 to 3 hrs/day or frequent performance of compulsive behaviors"},
            {"score": 3, "response_text_ko": "하루 3시간 초과 8시간 이하 또는 매우 자주 수행함", "response_text_en": "More than 3 and up to 8 hrs/day, or very frequent performance of compulsive behaviors"},
            {"score": 4, "response_text_ko": "하루 8시간 초과 또는 거의 지속적으로 수행하며, 횟수를 셀 수 없을 정도임", "response_text_en": "More than 8 hrs/day, or near constant performance of compulsive behaviors (too numerous to count)"}
        ]
    },
    {
        "id": 7,
        "question_ko": "강박 행동으로 인한 기능적 방해",
        "question_en": "INTERFERENCE DUE TO COMPULSIVE BEHAVIOR",
        "description_ko": "귀하의 강박 행동이 귀하의 업무, 학업, 사회생활 또는 기타 중요한 역할 수행에 얼마나 방해가 됩니까? 강박 행동 때문에 하지 못하는 일이 있습니까?",
        "description_en": "How much do your compulsive behaviors interfere with your work, school, social, or other important role functioning? Is there anything that you don’t do because of the compulsions?",
        "options": [
            {"score": 0, "response_text_ko": "전혀 없음", "response_text_en": "None"},
            {"score": 1, "response_text_ko": "사회적 또는 기타 활동에 약간의 방해가 있으나, 전반적인 수행에는 지장이 없음", "response_text_en": "Slight interference with social or other activities, but overall performance not impaired"},
            {"score": 2, "response_text_ko": "사회적 또는 직업적 수행에 명확한 방해가 있으나, 여전히 감당 가능함", "response_text_en": "Definite interference with social or occupational performance, but still manageable"},
            {"score": 3, "response_text_ko": "사회적 또는 직업적 수행에 상당한 손상이 있음", "response_text_en": "Causes substantial impairment in social or occupational performance"},
            {"score": 4, "response_text_ko": "수행 능력이 완전히 마비될 정도로 심각한 방해가 있음", "response_text_en": "Incapacitating"}
        ]
    },
    {
        "id": 8,
        "question_ko": "강박 행동과 관련된 고통의 정도",
        "question_en": "DISTRESS ASSOCIATED WITH COMPULSIVE BEHAVIOR",
        "description_ko": "강박 행동을 하지 못하게 되었을 경우, 어떤 기분이 드시겠습니까? 불안 수준은 어느 정도로 증가하겠습니까?",
        "description_en": "How would you feel if prevented from performing your compulsion(s)? How anxious would you become?",
        "options": [
            {"score": 0, "response_text_ko": "전혀 없음", "response_text_en": "None"},
            {"score": 1, "response_text_ko": "강박 행동을 하지 못하더라도 약간의 불안만 느낌", "response_text_en": "Only slightly anxious if compulsions prevented"},
            {"score": 2, "response_text_ko": "강박 행동을 못 하면 불안이 증가하나, 여전히 감당 가능함", "response_text_en": "Anxiety would mount but remain manageable if compulsions prevented"},
            {"score": 3, "response_text_ko": "강박 행동이 중단되면 뚜렷하고 매우 괴로운 불안이 발생함", "response_text_en": "Prominent and very disturbing increase in anxiety if compulsions interrupted"},
            {"score": 4, "response_text_ko": "활동을 수정하려는 어떠한 개입으로 인해도 심각한 불안이 유발되어 기능이 마비됨", "response_text_en": "Incapacitating anxiety from any intervention aimed at modifying activity"}
        ]
    },
    {
        "id": 9,
        "question_ko": "강박 행동에 대한 저항 노력",
        "question_en": "RESISTANCE AGAINST COMPULSIONS",
        "description_ko": "귀하는 강박 행동에 대해 어느 정도 저항하려고 노력하십니까?",
        "description_en": "How much of an effort do you make to resist the compulsions?",
        "options": [
            {"score": 0, "response_text_ko": "항상 저항하려고 노력함", "response_text_en": "Always try to resist"},
            {"score": 1, "response_text_ko": "대부분의 시간에 저항하려고 노력함", "response_text_en": "Try to resist most of the time"},
            {"score": 2, "response_text_ko": "어느 정도 저항하려는 노력을 함", "response_text_en": "Make some effort to resist"},
            {"score": 3, "response_text_ko": "거의 모든 강박 행동에 저항하지 않고 굴복하나, 약간의 꺼림칙함은 있음", "response_text_en": "Yield to almost all compulsions without attempting to control them, but with some reluctance"},
            {"score": 4, "response_text_ko": "완전히 자발적으로 모든 강박 행동에 굴복함", "response_text_en": "Completely and willingly yield to all compulsions"}
        ]
    },
    {
        "id": 10,
        "question_ko": "강박 행동에 대한 통제력",
        "question_en": "DEGREE OF CONTROL OVER COMPULSIVE BEHAVIOR",
        "description_ko": "강박 행동을 수행하고자 하는 충동은 어느 정도로 강합니까? 귀하는 이러한 충동을 얼마나 잘 통제하실 수 있습니까?",
        "description_en": "How strong is the drive to perform the compulsive behavior? How much control do you have over the compulsions?",
        "options": [
            {"score": 0, "response_text_ko": "완전히 통제 가능함", "response_text_en": "Complete control"},
            {"score": 1, "response_text_ko": "행동을 수행하고자 하는 압박은 있으나, 대체로 자발적 통제를 유지할 수 있음", "response_text_en": "Pressure to perform the behavior but usually able to exercise voluntary control over it"},
            {"score": 2, "response_text_ko": "행동을 수행하고자 하는 압박이 강하며, 통제가 어렵긴 해도 어느 정도는 가능함", "response_text_en": "Strong pressure to perform behavior, can control it only with difficulty"},
            {"score": 3, "response_text_ko": "행동에 대한 강한 충동이 있어 반드시 끝까지 수행해야 하며, 지연시키는 것조차 어렵습니다", "response_text_en": "Very strong drive to perform behavior, must be carried to completion, can only delay with difficulty"},
            {"score": 4, "response_text_ko": "행동에 대한 충동은 완전히 비자발적이고 압도적이며, 순간적으로라도 지연시키는 것이 거의 불가능합니다", "response_text_en": "Drive to perform behavior experienced as completely involuntary and overpowering, rarely able to even momentarily delay activity."}
        ]
    }
]

# 메인 함수: 앱 상태(증상 체크리스트 / 평가 문항 / 결과 출력)에 따라 화면 전환
def main():
    st.title("Y-BOCS 평가 웹앱")
    
    # st.session_state 초기화
    if "confirmed" not in st.session_state:
        st.session_state["confirmed"] = False
    if "submitted" not in st.session_state:
        st.session_state["submitted"] = False
    if "selected_symptoms_current" not in st.session_state:
        st.session_state["selected_symptoms_current"] = []
    if "selected_symptoms_past" not in st.session_state:
        st.session_state["selected_symptoms_past"] = []
    if "answers" not in st.session_state:
        st.session_state["answers"] = {}  # key: 문항 id, value: 선택한 옵션 인덱스

    # 1단계: 도입 증상 체크리스트 화면
    if not st.session_state["confirmed"]:
        st.header("도입 증상 체크리스트")
        st.write("아래 항목에서 해당하는 증상을 선택해주세요. 각 항목마다 '없음', '현재(최근 일주일간)', '과거' 중 하나를 선택하실 수 있습니다.")
        # ybo_cs_mapping의 각 카테고리별로 라디오 버튼 렌더링
        for category_key, category in ybo_cs_mapping.items():
            st.subheader(category["question_ko"])
            for idx, item in enumerate(category["items"]):
                # "기타" 항목이면 카테고리의 제목에서 첫 번째 단어를 추출하여 수정
                display_ko = item["ko"]
                display_en = item["en"]
                if item["ko"] == "기타":
                    cat_keyword_ko = category["question_ko"].split()[0]
                    cat_keyword_en = category["question_en"].split()[0]
                    display_ko = f"기타: {cat_keyword_ko}"
                    display_en = f"Other: {cat_keyword_en}"
                # 라디오 버튼 생성: 옵션 - "없음", "현재(최근 일주일간)", "과거"
                st.radio(
                    label=f"{display_ko}",
                    options=["없음", "현재(최근 일주일간)", "과거"],
                    index=0,
                    key=f"{category_key}_{idx}"
                )
        if st.button("증상 선택 완료"):
            # 각 증상별로 선택된 값을 확인하여 현재 증상, 과거 증상 리스트에 추가
            for category_key, category in ybo_cs_mapping.items():
                for idx, item in enumerate(category["items"]):
                    key_name = f"{category_key}_{idx}"
                    if key_name in st.session_state:
                        selection = st.session_state[key_name]
                        display_en = item["en"]
                        if item["ko"] == "기타":
                            cat_keyword_en = category["question_en"].split()[0]
                            display_en = f"Other: {cat_keyword_en}"
                        if selection == "현재(최근 일주일간)":
                            st.session_state["selected_symptoms_current"].append(display_en)
                        elif selection == "과거":
                            st.session_state["selected_symptoms_past"].append(display_en)
            st.session_state["confirmed"] = True

    # 2단계: 평가 문항 화면
    elif not st.session_state["submitted"]:
        st.header("Y-BOCS 평가 문항")
        st.write("아래 문항에 대해 해당하는 선택지를 선택해주세요.")
        for question in y_bocs_scale:
            options_list = [option["response_text_ko"] for option in question["options"]]
            selected = st.selectbox(
                f"{question['id']}. {question['question_ko']}\n{question['description_ko']}",
                options_list,
                key=f"q_{question['id']}"
            )
            score_index = options_list.index(selected)
            st.session_state["answers"][question["id"]] = score_index
        if st.button("제출"):
            st.session_state["submitted"] = True

    # 3단계: 결과 출력 화면 (영어로만 출력)
    else:
        st.header("Evaluation Results")
        total_score = 0
        results_text = "Yale-Brown Obsessive Compulsive Scale (Y-BOCS)\n\n"
        for question in y_bocs_scale:
            qid = question["id"]
            selected_index = st.session_state["answers"].get(qid, 0)
            total_score += question["options"][selected_index]["score"]
            results_text += f"{qid}. {question['question_en']}\n"
            results_text += f"   ({selected_index}) {question['options'][selected_index]['response_text_en']}\n\n"
        results_text += f"Total Score: {total_score}\n"
        # 임상적 해석 함수 (점수 구간에 따라 해석을 제공합니다.)
        def interpret_score(score):
            if score <= 7:
                return "Minimal symptoms (0-7 points)"
            elif score <= 15:
                return "Mild symptoms (8-15 points)"
            elif score <= 23:
                return "Moderate symptoms (16-23 points)"
            elif score <= 31:
                return "Severe symptoms (24-31 points)"
            else:
                return "Extreme symptoms (32-40 points)"
        interpretation = interpret_score(total_score)
        results_text += f"Interpretation: {interpretation}\n\n"
        
        # 선택한 증상을 현재와 과거로 별도 결합
        current_symptoms = ", ".join(st.session_state["selected_symptoms_current"]) if st.session_state["selected_symptoms_current"] else "None"
        past_symptoms = ", ".join(st.session_state["selected_symptoms_past"]) if st.session_state["selected_symptoms_past"] else "None"
        results_text += f"Selected Symptoms (Current): {current_symptoms}\n"
        results_text += f"Selected Symptoms (Past): {past_symptoms}\n"
        
        # 마크다운 코드 블록 내에서 결과 텍스트 출력
        st.markdown(f"```\n{results_text}\n```")

if __name__ == "__main__":
    main()
