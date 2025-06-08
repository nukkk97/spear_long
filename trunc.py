import os

input_dir = "/tmp2/b10902112/openwebtext/cleaned_texts"
output_dir = "/tmp2/b10902112/openwebtext/shortened_texts"
os.makedirs(output_dir, exist_ok=True)

for i in range(1, 1001):
    filename = f"urlsf_subset00-{i}_data_clean.txt"
    input_path = os.path.join(input_dir, filename)
    output_path = os.path.join(output_dir, filename)

    try:
        with open(input_path, "r", encoding="utf-8") as f:
            text = f.read()

        # 取前 1/5 的文字
        cutoff = len(text) // 5
        shortened_text = text[:cutoff]

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(shortened_text)

    except Exception as e:
        print(f"Error processing file {filename}: {e}")