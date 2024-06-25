部活動(エレ研)の入室状況管理アプリ

それまで鍵を開けた／閉めた際、そのことをdiscordにチャットする必要があった。
また、誰か居るのならしゃべりながら作業しに行きたいが、居るかわからないため
結局行かなかったということが多かった。

そこで鍵と在室状態をdiscordに掲示するbotを作成した。
![image](https://github.com/kino-n1851/elekenGK/assets/46987400/349eb69c-8800-48eb-8a7d-f80e508abe81)

チャットのように流れてしまうと把握が面倒なため、一つのメッセージを更新し続ける形にした。
入室時にNFCタグを読み込み、idを使用して入室／退室を記録する。
discordボットはレンタルサーバーで、NFC読み取りはRaspberry Piでsystemdを用いて動作させた。

コマンド一覧:
  /help
  /create
  /register
  /register_core
  /fetch_name
--------------
[/help]

ヘルプを表示します。
--------------
[/create]

ボットメッセージの表示を作成します。
すでに表示先がある場合は以前のメッセージは無効となり、以降新しいメッセージ上で状態が更新されます。
入室状態表示が流れてしまった場合などにご利用ください。
--------------
[/register]

discordアカウントのidのみを使用して入室管理アプリに登録します。
メールアドレスなどは使用しておりません。
コマンド受付後は仮登録となりますので、3分以内にNFCリーダーに登録したいデバイスをタッチしてNFC IDとの紐づけをしてください。
この操作で支払いなどが発生することもありません。
--------------
[/register_core]

上記 registerコマンドと同様に登録を行います。
こちらのコマンドで登録したユーザは、非アクティブ時も状態が表示されます。
--------------
[/fetch_name]

discordサーバープロフィールなどの変更後にこのコマンドを使用することで表示名が更新されます。