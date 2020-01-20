# Video Downloader of NTU Cool

This tool is a Python3 web crawler that can download the videos of a course on [NTU Cool](https://cool.ntu.edu.tw/). This script works only on [演算法設計與分析 (CSIE2136-01,02)](https://cool.ntu.edu.tw/courses/368) currently. You have to change the `course_id` as well as the parameter of `link_name.startswith()` in function `video_filter()` to make this script work in your case.

This tool may be improved in the future to make it automatically detect the type of the link with title `External Tool`. In this way, we need not hard code the pattern of the link of videos in `video_filter()`.


# NTU Cool 影片下載器

這個 Python3 的爬蟲腳本可以用來下載 [NTU Cool](https://cool.ntu.edu.tw/) 某個課程的影片。目前是作用在 [演算法設計與分析 (CSIE2136-01,02)](https://cool.ntu.edu.tw/courses/368) 課程，如果你想要用來下載你的課程的影片的話，需要更改 `course_id` 和 `video_filter()` 函數裡面那個 `'[單班]'` 的參數。

這個爬蟲腳本在未來可能可以自動偵測 NTU Cool 上的連結是否為影片連結，如果是的話就下載該影片，如果連結的內容是課程 pdf 或其他參考資料的話就忽略。如此一來，使用者就不需要為每個課程手動更改 `video_filter()` 裡面的內容。
