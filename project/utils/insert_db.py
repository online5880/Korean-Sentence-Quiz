### DB 에 저장import pandas as pd
import sqlite3
import pandas as pd

# CSV 파일 경로
csv_file_path = "/Users/mane/Desktop/한국어 문법 2/korean/utils/korean.csv"

# CSV 파일 읽기
data = pd.read_csv(csv_file_path)

# CSV 파일 읽기
try:
    data = pd.read_csv(csv_file_path)
    print(data.head())
except FileNotFoundError:
    print(f"CSV 파일을 찾을 수 없습니다: {csv_file_path}")
    exit(1)

# SQLite 데이터베이스 연결
conn = sqlite3.connect("/Users/mane/Desktop/한국어 문법 2/korean/db.sqlite3")

try:
    # 'text' 컬럼만 선택 (Django 모델과 일치)
    data_to_insert = data[["text"]]

    # 데이터베이스에 테이블 생성 및 데이터 삽입
    data_to_insert.to_sql("korean_app_sentence",
                          conn,
                          if_exists="replace",
                          index=True,
                          index_label="id")
    print("데이터베이스가 성공적으로 생성되었습니다.")
except Exception as e:
    print(f"데이터베이스 생성 중 오류 발생: {e}")
finally:
    # 연결 종료
    conn.close()
