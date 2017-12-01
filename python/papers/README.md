## Scripts for starting research

```
python 1_find_papers.py --pdf [xxx.pdf]
```
Search references in xxx.pdf and filter record using **keywords** specified in [1_find_paper.py](https://github.com/DuinoDu/scripts/blob/master/python/papers/1_find_papers.py#L11). Results are saved in _papers.json_


```
2_fetch_papers.py
```
Fetch paper's download url using selenium and [BING](https://cn.bing.com). Refer [install_selenium.sh](https://github.com/DuinoDu/scripts/blob/master/shell/install/install_selenium.sh) to install selenium and webdriver. Results are saved in _papers.json_


```
3_download_papers.py
```
Download papers recorded in _papers.json_ using url. Papers are downloaded in _papers_ folder.


```
4_refine_title.py
```
Refine paper pdf filename using PDFMiner to parse pdf and get title.


```
5_fetch_bib.py
```
Fetch bibliography using selenium and [scirate](https://scirate.com). Only support arxiv papers now.
