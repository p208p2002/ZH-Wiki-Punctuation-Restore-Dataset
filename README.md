# 中文標點符號預測資料集
<!-- ZH-Wiki Punctuation Restore Dataset -->
[資料集下載](https://github.com/p208p2002/ZH-Wiki-Punctuation-Restore-Dataset/releases/)
## 資料集描述
### 資料來源
中文維基百科

### 數量
- 訓練集：30000篇
- 測試集：3000篇
- 開發集：3000篇

### 使用符號
共六種全形符號
```
，、。？！；
```

## 使用
1. 下載[zh-wiki data](https://dumps.wikimedia.org/zhwiki)
2. 解壓縮檔案（若有需要）
3. 使用 [wikiextractor](https://github.com/attardi/wikiextractor)抽取資料
```bash
$ wikiextractor -b 20M --json zhwiki-20220601-pages-articles-multistream.xml
```
4. 執行`make_dataset.py`
