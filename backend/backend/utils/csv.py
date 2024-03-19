import app, mongo
import csv


def make_csv(username, id):
    query = {'$and': [{'username': username}, {'id': (id)}]}
    all_datas = mongo.db.scp_alldatas.find_one(query)
    # MongoDB data
    mongo_data = [
        {
            "_id": {"$oid": "65f811780108e561f20ae83f"},
            "id": "65f70165fb2e2cd614635117",
            "username": "5rfujikawa",
            "data": {
                "物件名称": "江良2丁目　中古住宅",
                "現況": "空家",
                "価格（最安値）": "1,500万円",
                "交通（駅・バス停）": "山口線「上山口」駅 徒歩18分",
                "駐車場": "有/-",
                "間取り": "5DK/122.54㎡",
                "建物面積": "122.54㎡",
                "土地面積": "187.22坪(618.94㎡)",
                "完成年月（築年月）": "1972年4月（築52年）",
                # Other fields...
            },
            "title": "江良2丁目　中古住宅"
        },
        {
            "_id": {"$oid": "65f811780108e561f20ae840"},
            "id": "65f70165fb2e2cd614635117",
            "username": "5rfujikawa",
            "data": {
                "物件名称": "フェスティオ堂の前",
                "現況": "空家",
                "価格（最安値）": "2,180万円",
                "交通（駅・バス停）": "山口線「山口」駅 徒歩11分\n山口線「上山口」駅 徒歩8分",
                "駐車場": "空有/5,000円 (税込)",
                "間取り": "Unknown",
                "建物面積": "Unknown",
                "土地面積": "Unknown",
                "完成年月（築年月）": "2004年7月（築19年）",
                # Other fields...
            },
            "title": "フェスティオ堂の前"
        }
    ]

    # Specify CSV file path
    csv_file = "output.csv"


    # Extract headers dynamically from the first document
    headers = list(mongo_data[0]["data"].keys())

    # Add additional headers if needed
    # headers.extend(["_id", "id", "username", "title"])

    # Write MongoDB data to CSV file
    with open(csv_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        
        # Write header
        writer.writeheader()
        
        # Write data rows
        for item in mongo_data:
            # Extract data from "data" field
            data = item.pop("data")
            
            # Combine "data" with other fields
            row = {**data}
            
            writer.writerow(row)
