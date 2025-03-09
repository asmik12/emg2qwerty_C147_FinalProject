import re
import sys
import pandas as pd

def extract_epoch_losses(log_text):
    # This dictionary will store the final loss for each epoch.
    epoch_losses = {}
    # Regex to match lines that show the final training status (100% progress) and a loss value.
    pattern = re.compile(r"Epoch (\d+):.*100%\|██████████\|.*loss=([\d\.]+)")

    for line in log_text.splitlines():
        match = pattern.search(line)
        if match:
            epoch = int(match.group(1))
            loss = float(match.group(2))
            # For each epoch, we update the loss so that the last occurrence is used.
            epoch_losses[epoch] = loss
    return epoch_losses

def main():
    # If a filename is passed as an argument, read the log from that file.
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        try:
            with open(filename, "r", encoding="utf-8") as f:
                log_text = f.read()
        except UnicodeDecodeError:
            # If utf-8 fails, try utf-16 encoding
            print(f"Failed to read {filename} with utf-8 encoding. Trying utf-16...")
            with open(filename, "r", encoding="utf-16") as f:
                log_text = f.read()
    else:
        # Otherwise, read the log from standard input.
        log_text = sys.stdin.read()

    losses = extract_epoch_losses(log_text)

    # Convert the losses dictionary to a pandas DataFrame.
    df = pd.DataFrame(list(losses.items()), columns=['Epoch', 'Loss'])

    # Write the DataFrame to an Excel file.
    df.to_excel('epoch_losses.xlsx', index=False)

    print("Losses have been written to 'epoch_losses.xlsx'.")

if __name__ == "__main__":
    main()
