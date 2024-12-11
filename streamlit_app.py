import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_bizinfo_data(keyword):
    url = "https://www.bizinfo.go.kr/web/lay1/bbs/S1T122C128/AS/74/list.do"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    # 검색 결과 가져오기
    params = {"searchType": "title", "keyword": keyword}
    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        st.error("Failed to fetch data from Bizinfo.")
        return []

    soup = BeautifulSoup(response.content, "html.parser")

    # 검색 결과 파싱
    data = []
    results = soup.find_all("tr", class_="board_list")  # 실제 HTML 구조에 맞게 수정 필요
    for item in results:
        title_element = item.find("td", class_="title")
        if title_element:
            title = title_element.get_text(strip=True)
            link = "https://www.bizinfo.go.kr" + title_element.find("a")["href"]
            date = item.find("td", class_="date").get_text(strip=True)
            data.append({"Title": title, "Link": link, "Date": date})

    return data

def main():
    st.title("Bizinfo Support Project Scraper")
    st.write("Search for support project announcements by keyword and download the results.")

    # 키워드 입력
    keyword = st.text_input("Enter keyword to search for:")

    if st.button("Search"):
        if keyword:
            data = fetch_bizinfo_data(keyword)

            if data:
                # 결과를 데이터프레임으로 표시
                df = pd.DataFrame(data)
                st.write(df)

                # CSV 다운로드 링크 제공
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download Results as CSV",
                    data=csv,
                    file_name="bizinfo_results.csv",
                    mime="text/csv",
                )
            else:
                st.warning("No results found for the given keyword.")
        else:
            st.warning("Please enter a keyword to search.")

if __name__ == "__main__":
    main()
