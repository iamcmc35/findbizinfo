import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta

def search_google_api(keyword, start_date, end_date):
    api_key = "YOUR_API_KEY"  # 구글 API 키 입력
    cx = "YOUR_CX_ID"  # Custom Search Engine ID 입력

    # API 요청 URL
    url = f"https://www.googleapis.com/customsearch/v1"
    params = {
        "key": api_key,
        "cx": cx,
        "q": f"{keyword} 지원사업 filetype:pdf",
        "sort": f"date:r:{start_date}:{end_date}",
        "hl": "ko"
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        st.error("Failed to fetch data from Google API.")
        return []

    results = response.json().get("items", [])
    data = []
    for result in results:
        title = result.get("title")
        link = result.get("link")
        data.append({"Title": title, "Link": link})

    return data

def main():
    st.title("Google Support Project Searcher")
    st.write("Search for support project announcements using Google Custom Search API and download related PDFs.")

    # 키워드 입력
    keyword = st.text_input("Enter keyword to search for:")

    # 날짜 입력
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start date", datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    with col2:
        end_date = st.date_input("End date", datetime.now()).strftime("%Y-%m-%d")

    if st.button("Search"):
        if keyword and start_date and end_date:
            data = search_google_api(keyword, start_date, end_date)

            if data:
                # 결과를 데이터프레임으로 표시
                df = pd.DataFrame(data)
                st.write(df)

                # CSV 다운로드 링크 제공
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download Results as CSV",
                    data=csv,
                    file_name="google_results.csv",
                    mime="text/csv",
                )

                # PDF 파일 다운로드 링크
                for item in data:
                    if item["Link"].endswith(".pdf"):
                        st.write(f"[Download PDF]({item['Link']})")
            else:
                st.warning("No results found for the given keyword and date range.")
        else:
            st.warning("Please enter a keyword and select a date range.")

if __name__ == "__main__":
    main()
