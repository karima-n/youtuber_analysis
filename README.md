# youtuber_analysis

## 使い方
1. 日本のYoutuberランキング(https://ytranking.net)より1〜200位のチャンネル名をリストcnames.txtを作る。
2. apiキーは.envファイルに入れておく。
3. cnames.txtからcreate_idlist.pyを用いて1~200位のIDリストcids.txtを作る。
4. cnames.txtとcids.txtからcreate_relationlist.pyを用いて交友関係リストyoutuber.txtを作る。
5. kadai2-1.pyやkadai3-1.pyを用いてクラスタリングや中心性解析を行う。
