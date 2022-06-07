# Cloud Native Deployment Final Project (Group 12)

網頁連結：https://ying0409.github.io/Final_Project_12/index.html
Docker image：https://hub.docker.com/r/yychang0409/crawler

* 爬蟲 (crawler_sample.py)
  * 爬取從今年6月至去年5月，台積電及3家供應商 (ASML、Applied Materials、SUMCO) 的所有中文網頁URL。
  * 爬取結果含有 3 個欄位：Date、Query、Link
    * Date: 今年5月-去年6月
    * Query: 以 "台積電 ASML", "台積電 Applied Materials", "台積電 SUMCO" 3種 query 至 Google 進行查詢
    * Link: 該月以該Query至Google上查詢得到的中文網頁URL

* 資料分析 (analysis.py)
  * 將爬取到的URL獲得網頁中的文字
  * 將網頁中的文字使用ckip進行斷詞 (需下載data: https://drive.google.com/drive/folders/105IKCb88evUyLKlLondvDBoh7Dy_I1tm)
  * 統計網頁中台積電及3家供應商的文字出現次數
  * 結果含有 4 個欄位：Date、Company、Count、Text
    * Date: 今年5月-去年6月
    * Company: 台積電、ASML、Applied Materials、SUMCO
    * Count: 出現次數
    * Text: 該月以台積電和該供應商作為Query後爬取到的網頁文字
