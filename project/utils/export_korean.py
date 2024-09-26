# 한국어 대화 컬럼 추출
import pandas as pd
def export_korean(path="/Users/mane/Desktop/한국어 문법/data/2_대화체.xlsx", count=100):
    df = pd.read_excel(path)
    df['원문'].iloc[:count].to_csv('data/korean.csv',index=False)
    print("완료")
    
export_korean(count=100)

