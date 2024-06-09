import os
import jiwer
import re
import chardet


def read_file(filepath):
    with open(filepath, 'rb') as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']
        if encoding is None:
            encoding = 'utf-8'
        return raw_data.decode(encoding).strip()


def preprocess(text):
    return re.sub(r'[^\w\s]', '', text).lower()


def calculate_wer(reference, hypothesis):
    wer_with_punct = jiwer.wer(reference=reference, hypothesis=hypothesis)
    reference_no_punct = preprocess(reference)
    hypothesis_no_punct = preprocess(hypothesis)
    wer_without_punct = jiwer.wer(
        reference=reference_no_punct, hypothesis=hypothesis_no_punct)
    measures = jiwer.compute_measures(
        truth=reference_no_punct, hypothesis=hypothesis_no_punct)
    return wer_with_punct, wer_without_punct, measures


def process_directory(model_dir, test_dir):
    total_wer_with_punct = 0
    total_wer_without_punct = 0
    total_insertions = 0
    total_substitutions = 0
    total_deletions = 0
    total_correct_words = 0
    file_count = 0

    for file_name in os.listdir(test_dir):
        if file_name.endswith('.txt'):
            reference_path = os.path.join(test_dir, file_name)
            hypothesis_path = os.path.join(model_dir, file_name)

            if os.path.exists(hypothesis_path):
                reference = read_file(reference_path)
                hypothesis = read_file(hypothesis_path)

                wer_with_punct, wer_without_punct, measures = calculate_wer(
                    reference, hypothesis)

                total_wer_with_punct += wer_with_punct
                total_wer_without_punct += wer_without_punct
                total_insertions += measures['insertions']
                total_substitutions += measures['substitutions']
                total_deletions += measures['deletions']
                total_correct_words += measures['hits']
                file_count += 1

    if file_count == 0:
        return None

    avg_wer_with_punct = total_wer_with_punct / file_count
    avg_wer_without_punct = total_wer_without_punct / file_count

    return {
        'avg_wer_with_punct': avg_wer_with_punct,
        'avg_wer_without_punct': avg_wer_without_punct,
        'insertions': total_insertions,
        'substitutions': total_substitutions,
        'deletions': total_deletions,
        'total_correct_words': total_correct_words
    }


def main():
    root_dir = '.'
    test_dir = os.path.join(root_dir, 'test')

    for dir_name in os.listdir(root_dir):
        if dir_name.startswith('model'):
            model_dir = os.path.join(root_dir, dir_name)
            if os.path.isdir(model_dir):
                results = process_directory(model_dir, test_dir)
                if results:
                    print(f"Results for {dir_name}:")
                    print(
                        f"  Average WER with punctuation: {results['avg_wer_with_punct']:.2f}")
                    print(
                        f"  Average WER without punctuation: {results['avg_wer_without_punct']:.2f}")
                    print(f"  Total insertions (I): {results['insertions']}")
                    print(
                        f"  Total substitutions (S): {results['substitutions']}")
                    print(f"  Total deletions (D): {results['deletions']}")
                    print(
                        f"  Total correct words (H): {results['total_correct_words']}")


if __name__ == "__main__":
    main()
