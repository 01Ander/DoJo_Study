def load_to_bronze(raw_api_response: list) -> list:
    return raw_api_response

def process_to_silver(bronze_data: list) -> list:
    silver_data = []
    for item in bronze_data:
        if "ingredient" in item:
            amount = item.get("amount")
            if amount is None:
                amount = 0
            
            clean_item = {
                "ingredient": item["ingredient"].strip().lower(),
                "amount": amount
            }
            silver_data.append(clean_item)
    return silver_data

def aggregate_to_gold(silver_data: list) -> dict:
    gold_data = {}
    for item in silver_data:
        name = item["ingredient"]
        amount = item["amount"]
        
        if name in gold_data:
            gold_data[name] += amount
        else:
            gold_data[name] = amount
    return gold_data
