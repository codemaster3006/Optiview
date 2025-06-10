import pandas as pd
import ijson

def parse_large_json(file_path, output_csv):
    """
    Parses a large JSON file to extract CPT codes, contracted rates, and provider info.
    Outputs a CSV file for use in Power BI.
    """
    data = []

    with open(file_path, 'rb') as f:
        parser = ijson.items(f, 'item')  # Assumes top-level JSON array

        for item in parser:
            try:
                cpt = item.get('cpt_code') or item.get('procedureCode')
                rate = item.get('negotiated_rate') or item.get('contractedRate')
                provider = item.get('provider', {}).get('npi') or item.get('provider_id')

                data.append({
                    'CPT Code': cpt,
                    'Contracted Rate': rate,
                    'Provider': provider
                })
            except Exception as e:
                print(f"Error parsing item: {e}")

    df = pd.DataFrame(data)
    df.to_csv(output_csv, index=False)
    print(f"Saved {len(df)} rows to {output_csv}")
