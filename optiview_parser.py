import pandas as pd
import ijson
import os

def parse_large_json(file_path, output_csv):
    """
    Parses a large JSON file to extract CPT codes, contracted rates, and provider info.
    Outputs a CSV file for use in Power BI.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    data = []

    with open(file_path, 'rb') as f:
        parser = ijson.items(f, 'item')  # Update this key path if needed

        for item in parser:
            try:
                # Adjust these keys based on the actual JSON structure
                code = item.get('billing_code') or item.get('cpt_code') or item.get('procedureCode')
                rate = item.get('negotiated_rate') or item.get('contractedRate') or item.get('grossCharge')
                provider = item.get('provider', {}).get('npi') or item.get('provider_id') or item.get('providerName')

                data.append({
                    'CPT Code': code,
                    'Contracted Rate': rate,
                    'Provider': provider
                })

            except Exception as e:
                print(f"Error parsing item: {e}")

    df = pd.DataFrame(data)
    df.to_csv(output_csv, index=False)
    print(f"✅ Saved {len(df)} rows to {output_csv}")

if __name__ == "__main__":
    file_path = '/Users/taylorhale/Documents/Sterling/Sterling/Business Development/*Pricing Transparency/82-0436622_EASTERN-IDAHO-REGIONAL-MEDICAL-CENTER_standardcharges.json'
    output_csv = 'eirmc_contract_rates.csv'
    parse_large_json(file_path, output_csv)
