import { Link } from "react-router-dom";

export default function TypeSetting() {
  return (
    <div className="bg-blue-100">
      <h2>スクレイピング設定</h2>
      <p>新規追加ボタン押下後、以下選択を⾏う</p>
      <div>
        <Link to={"/from-file"}>サイトから取込</Link>
      </div>
      <div>
        <Link to={"/from-site"}>エクセルから取込</Link>
      </div>
    </div>
  );
}
