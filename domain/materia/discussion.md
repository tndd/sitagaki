# domain modelの分類
enumというtype系とmdoel系は分類したい。
## 分類例
しっかり分けるならこうなるんだろうが、  
細かすぎ？

model
- const
- value
- entity

# domain/materiaのディレクトリ構成変更
bar,quote,...という分類はあまりに細かすぎ？  
このままだと区分けの粒度が細かくなりすぎる。

## materia編成例
将来的にざっと思いつくだけでこれだけある。  
従来のbar,quote,...という分類は荒すぎる。
- stock
  - bar
  - quote
  - ...
- news
  - XXX
  - ...
- docs
  - XXX
  - ...
- trend
  - XXX
  - ...
- ...

### stock
チャート情報が格納される。

### news
ニュース情報が格納される。

### docs
ドキュメントが格納される。
経済レポート、政府の発表などなど。

### trend
検索結果の傾向などの世間の反応系（？）
gogoletrendやtwitterのトレンドなど。

