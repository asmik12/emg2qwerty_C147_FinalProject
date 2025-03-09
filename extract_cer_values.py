import re
import json

def extract_metrics(file_path):
    metrics = {
        'val_metrics': [],
        'test_metrics': []
    }
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # Read through the file to extract the metrics
            content = file.read()

            # Look for the 'val_metrics' block
            val_loss_match = re.findall(r"'val/loss':\s*([\d\.]+)", content)
            val_cer_match = re.findall(r"'val/CER':\s*([\d\.]+)", content)
            
            # Add val_metrics to the dictionary
            if val_loss_match and val_cer_match:
                metrics['val_metrics'].append({
                    'val/loss': float(val_loss_match[0]),
                    'val/CER': float(val_cer_match[0]),
                })

            # Look for the 'test_metrics' block
            test_loss_match = re.findall(r"'test/loss':\s*([\d\.]+)", content)
            test_cer_match = re.findall(r"'test/CER':\s*([\d\.]+)", content)
            
            # Add test_metrics to the dictionary
            if test_loss_match and test_cer_match:
                metrics['test_metrics'].append({
                    'test/loss': float(test_loss_match[0]),
                    'test/CER': float(test_cer_match[0]),
                })
        
    except UnicodeDecodeError:
        print(f"UnicodeDecodeError encountered, trying with 'latin-1' encoding.")
        with open(file_path, 'r', encoding='latin-1') as file:
            content = file.read()

            # Repeat the extraction logic as described above

            val_loss_match = re.findall(r"'val/loss':\s*([\d\.]+)", content)
            val_cer_match = re.findall(r"'val/CER':\s*([\d\.]+)", content)
            if val_loss_match and val_cer_match:
                metrics['val_metrics'].append({
                    'val/loss': float(val_loss_match[0]),
                    'val/CER': float(val_cer_match[0]),
                })

            test_loss_match = re.findall(r"'test/loss':\s*([\d\.]+)", content)
            test_cer_match = re.findall(r"'test/CER':\s*([\d\.]+)", content)

            if test_loss_match and test_cer_match:
                metrics['test_metrics'].append({
                    'test/loss': float(test_loss_match[0]),
                    'test/CER': float(test_cer_match[0]),
                })
    
    return metrics

# Example usage
file_path = 'log/29870_0_log.out'  # replace with your .out file path
metrics = extract_metrics(file_path)

# Print the extracted metrics in JSON format for clarity
print(json.dumps(metrics, indent=4))
