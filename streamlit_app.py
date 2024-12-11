import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta

def search_bing(keyword, start_date, end_date):
    url = "https://www.bing.com/search"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    params = {
        "q": f"{keyword} 지원사업 filetype:pdf",  # PDF 파일 검색
        "filters": f"ex1:date:r:{start_date}..{end_date}"  # 날짜 범위 필터
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        st.error("Failed to fetch data from Bing.")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    data = []
    results = soup.find_all("li", class_="b_algo")  # Bing search result container
    for result in results:
        title_element = result.find("h2")
        if title_element:
            title = title_element.get_text(strip=True)
            link = title_element.find("a")["href"]
            snippet = result.find("p").get_text(strip=True) if result.find("p") else ""
            data.append({"Title": title, "Link": link, "Description": snippet})

    return data

def main():
    st.title("Bing Support Project Searcher")
    st.write("Search for support project announcements using Bing and download related PDFs.")

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
            data = search_bing(keyword, start_date, end_date)

            if data:
                # 결과를 데이터프레임으로 표시
                df = pd.DataFrame(data)
                st.write(df)

                # CSV 다운로드 링크 제공
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download Results as CSV",
                    data=csv,
                    file_name="bing_results.csv",
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
