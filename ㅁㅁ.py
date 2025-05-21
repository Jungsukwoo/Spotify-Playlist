# 0. (필수) 라이브러리 설치 확인 (터미널에서 실행):
# pip install openai

import openai
import os # 환경 변수 사용을 위해 추가 (권장)

# 1. (필수) OpenAI API 키 설정
# 방법 1: 직접 코드에 입력 (보안상 권장되지 않음! 테스트용으로만 사용)
# openai.api_key = "sk-YOUR_OPENAI_API_KEY_HERE" 
# 방법 2: 환경 변수에서 API 키 가져오기 (더 안전하고 권장되는 방법)
# 실행 전에 터미널에서 'export OPENAI_API_KEY="your_api_key_here"' (Linux/macOS)
# 또는 'set OPENAI_API_KEY=your_api_key_here' (Windows) 명령으로 환경 변수를 설정해야 합니다.
openai.api_key = ""

if openai.api_key is None:
    print("OpenAI API 키가 설정되지 않았습니다. 환경 변수 OPENAI_API_KEY를 설정해주세요.")
    print("또는 코드 내 'openai.api_key' 부분에 직접 키를 임시로 입력할 수 있으나 권장되지 않습니다.")
    # API 키가 없으면 이후 코드 실행이 어려우므로, 여기서 멈추거나 기본값을 설정할 수 있습니다.
    # exit() # 또는 테스트를 위해 기본값으로 계속 진행하도록 할 수 있습니다. (실제 API 호출은 실패함)

# 2. 가상의 아주 간단한 지식 베이스 (실제로는 DB나 파일 시스템, 검색 엔진 등에서 로드)
mock_knowledge_base = {
    "doc1_economy": "최근 발표된 정부 보고서에 따르면, 올해 경제 성장률은 2.5%로 전망됩니다.",
    "doc2_employment": "통계청은 지난 분기 실업률이 3.0%로 소폭 하락했다고 발표했습니다.",
    "doc3_candidate_A_promise": "A 후보는 주요 공약으로 청년 일자리 50만 개 창출을 내걸었습니다.",
    "doc4_candidate_A_record": "A 후보가 시장으로 재임했던 시기, 해당 시의 청년 일자리는 연평균 1만 개 증가했습니다.",
    "doc5_expert_opinion_economy": "B 경제 연구소는 현재 경제 상황을 고려할 때, 급격한 일자리 증가는 어려울 수 있다고 분석했습니다."
}

# 3. 매우 간단한 증거 검색기 함수 (실제로는 BERT 임베딩 기반 유사도 검색 등 사용)
def retrieve_evidence_simple(claim, knowledge_base, max_evidence=3):
    """
    간단한 키워드 매칭으로 관련 증거를 검색합니다.
    실제 시스템에서는 훨씬 정교한 의미론적 검색이 필요합니다.
    """
    relevant_evidence_texts = []
    claim_keywords = [kw for kw in claim.split() if len(kw) > 1] # 한 글자 이상 키워드

    for doc_id, content in knowledge_base.items():
        if any(keyword in content for keyword in claim_keywords):
            relevant_evidence_texts.append(f"출처 [{doc_id}]: {content}")
    
    if not relevant_evidence_texts:
        return "관련된 명확한 증거를 지식 베이스에서 찾지 못했습니다."
        
    # 간단히 최대 개수 제한 (실제로는 관련도 순으로 정렬 후 선택)
    return "\n".join(relevant_evidence_texts[:max_evidence])

# 4. LLM (GPT) API 호출을 통한 분석 함수
def analyze_claim_with_llm(claim, evidence, model_name="gpt-4.1-mini"):
    """
    주장과 증거를 바탕으로 LLM에게 분석을 요청합니다.
    """
    # 프롬프트 구성: LLM에게 역할을 부여하고 명확한 지시를 내리는 것이 중요합니다.
    system_prompt = "당신은 객관적이고 논리적인 사실 확인 전문가입니다. 제공된 주장과 증거만을 바탕으로 다음 지시사항에 따라 분석 결과를 제시해주세요."
    user_prompt = f"""
    [주장]: {claim}

    [제공된 증거]:
    {evidence}

    [지시사항]:
    1. 주장의 핵심 내용을 파악하십시오.
    2. 제공된 증거들이 주장의 핵심 내용과 얼마나 관련이 있는지 평가하십시오.
    3. 각 증거가 주장을 지지하는지, 반박하는지, 아니면 중립적인지 분석하십시오.
    4. 위의 분석을 종합하여, 제공된 증거에 기반했을 때 주장에 대한 잠정적인 판단(예: 사실에 가까움, 대체로 거짓, 정보 부족 등)을 내리고, 그 이유를 구체적인 증거를 인용하여 단계별로 설명해주십시오.
    5. 판단을 내리기에 정보가 불충분하다면 명확히 밝히십시오.

    [분석 결과]:
    """

    if not openai.api_key: # API 키가 설정되지 않았다면 실제 호출을 시도하지 않음
        return "[API 키 미설정] LLM 분석을 수행할 수 없습니다."

    try:
        response = openai.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2 # 낮은 온도로 설정하여 좀 더 일관되고 사실 기반의 답변 유도
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"OpenAI API 호출 중 오류 발생: {e}"

# 5. 메인 실행 부분
if __name__ == "__main__":
    # 예시 주장
    user_claim_to_verify = "A 후보는 청년 일자리 50만 개 공약을 이미 달성했다."
    
    print(f"--- 검증할 주장 ---\n{user_claim_to_verify}\n")

    # 1단계: 증거 검색
    print("--- 증거 검색 중 ---")
    retrieved_evidence = retrieve_evidence_simple(user_claim_to_verify, mock_knowledge_base)
    print(f"[검색된 증거]:\n{retrieved_evidence}\n")

    # 2단계: LLM을 통한 분석
    if "찾지 못했습니다" in retrieved_evidence or not openai.api_key:
        print("--- LLM 분석 (SKIP) ---")
        if not openai.api_key:
             print("API 키가 설정되지 않아 LLM 분석을 건너뜁니다.")
        else:
            print("관련 증거가 충분하지 않아 LLM 분석을 건너뜁니다.")
    else:
        print("--- LLM 분석 중 ---")
        llm_analysis_result = analyze_claim_with_llm(user_claim_to_verify, retrieved_evidence)
        print(f"[LLM 분석 결과]:\n{llm_analysis_result}")



# ==============================
# --- 검증할 주장 ---
# A 후보는 청년 일자리 50만 개 공약을 이미 달성했다.

# --- 증거 검색 중 ---
# [검색된 증거]:
# 출처 [doc3_candidate_A_promise]: A 후보는 주요 공약으로 청년 일자리 50만 개 창출을 내걸었습니다.
# 출처 [doc4_candidate_A_record]: A 후보가 시장으로 재임했던 시기, 해당 시의 청년 일자리는 연평균 1만 개 증가했습니다.
# 출처 [doc5_expert_opinion_economy]: B 경제 연구소는 현재 경제 상황을 고려할 때, 급격한 일자리 증가는 어려울 수 있다고 분석했습니다.

# --- LLM 분석 중 ---
# [LLM 분석 결과]:
# [분석 결과]:

# 1. 주장의 핵심 내용 파악
#    - A 후보가 내건 청년 일자리 50만 개 창출 공약을 이미 달성했다는 점이 핵심 내용이다.

# 2. 제공된 증거와 주장의 관련성 평가
#    - [doc3_candidate_A_promise]: A 후보가 청년 일자리 50만 개 창출을 공약으로 내걸었다는 점에서 주장의 배경과 관련이 있다.
#    - [doc4_candidate_A_record]: A 후보 재임 시 청년 일자리가 연평균 1만 개 증가했다는 기록은 공약 달성 여부 판단에 직접적인 관련이 있다.
#    - [doc5_expert_opinion_economy]: 경제 상황이 급격한 일자리 증가를 어렵게 한다는 분석은 공약 달성 가능성에 대한 간접적 관련성을 가진다.

# 3. 각 증거의 주장 지지 여부 분석
#    - [doc3_candidate_A_promise]: 중립적. 공약 내용만 밝히고 달성 여부는 언급하지 않음.
#    - [doc4_candidate_A_record]: 반박하는 경향. 연평균 1만 개 증가라는 수치는 공약 50만 개 달성에 미치지 못함.
#    - [doc5_expert_opinion_economy]: 반박하는 경향. 경제 상황이 급격한 일자리 증가를 어렵게 한다는 점은 공약 달성 가능성을 낮춤.

# 4. 종합 판단 및 이유
#    - A 후보가 청년 일자리 50만 개 공약을 내걸었다는 점은 명확하나([doc3_candidate_A_promise])
#    - 재임 기간 동안 연평균 1만 개 증가라는 기록([doc4_candidate_A_record])만으로는 50만 개 달성 여부를 판단하기 어렵지만, 단순 계산 시 50만 개 달성에는 상당한 시간이 필요함을 시사한다.     
#    - 또한, 경제 전문가의 분석([doc5_expert_opinion_economy])은 급격한 일자리 증가가 현실적으로 어려움을 나타내어 공약 달성 가능성을 낮춘다.
#    - 따라서 제공된 증거에 근거하면, A 후보가 청년 일자리 50만 개 공약을 이미 달성했다는 주장은 대체로 거짓에 가깝다고 판단된다.

# 5. 정보 부족 여부
#    - 다만, 정확한 재임 기간과 총 청년 일자리 증가 수치, 그리고 최근 일자리 통계가 제공되지 않아 완전한 확증은 어렵다.
#    - 따라서 추가적인 구체적 데이터가 필요하다는 점은 인정한다.

# 결론: 제공된 증거를 바탕으로 볼 때, A 후보가 청년 일자리 50만 개 공약을 이미 달성했다는 주장은 대체로 거짓에 가깝다. 이는 연평균 1만 개 증가 기록과 경제 상황 분석에 근거한 판단이다. 다만,  완전한 판단을 위해서는 더 구체적인 일자리 증가 총량과 기간에 대한 정보가 필요하다.
