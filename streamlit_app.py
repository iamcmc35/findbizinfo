import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta

def search_google(keyword, start_date, end_date):
    url = "https://www.google.com/search"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    params = {
        "q": f"{keyword} 지원사업 filetype:pdf",
        "tbs": f"cdr:1,cd_min:{start_date},cd_max:{end_date}",
        "hl": "ko"
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        st.error("Failed to fetch data from Google.")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    data = []
    results = soup.find_all("div", class_="tF2Cxc")  # Google search result container
    for result in results:
        title = result.find("h3").get_text(strip=True)
        link = result.find("a")["href"]
        data.append({"Title": title, "Link": link})

    return data

def main():
    st.title("Google Support Project Searcher")
    st.write("Search for support project announcements on Google and download related PDFs.")

    # 키워드 입력
    keyword = st.text_input("Enter keyword to search for:")

    # 날짜 입력
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start date", datetime.now() - timedelta(days=7))
    with col2:
        end_date = st.date_input("End date", datetime.now())

    if st.button("Search"):
        if keyword and start_date and end_date:
            data = search_google(keyword, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))

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
