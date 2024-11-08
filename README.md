# Bloom Filter Password Comparison

This repository contains a Python implementation for comparing password similarities using Bloom filters. The Bloom filter uses bigrams of passwords and generates multiple hash values from MD5 and SHA256 algorithms. It allows for testing the similarity between passwords, including their modified versions, by computing the Jaccard coefficient.

## Key Features:
- **Bloom Filter Creation**: Generates Bloom filters for passwords based on bigrams and hash functions (MD5, SHA256).
- **Jaccard Coefficient**: Measures the similarity between Bloom filters of two passwords.
- **Modification Testing**: Tests password modifications for similarity based on a threshold.
- **Datasets**: Utilizes the `rockyou.txt` dataset and generates several datasets for testing.
- **Beta Files**: Generates Beta files containing Bloom filters for each password in the datasets for comparison.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/Bloom-Filter-Password-Comparison.git
    ```

2. Navigate to the project folder:

    ```bash
    cd Bloom-Filter-Password-Comparison
    ```

3. Install the necessary dependencies:

    ```bash
    pip install numpy
    ```

## Usage

1. **Create Bloom filters and compare passwords**:  
   The `main.py` file can be run directly to create Bloom filters, generate Beta files, and test password similarity.

    ```bash
    python Bloom-Filter-Password-Comparison.py
    ```

2. **Password modification testing**:  
   You can test the similarity of a password with its modified versions. Adjust the list of modifications as required in the script.

## Structure

- `Bloom-Filter-Password-Comparison.py`: The main script for generating Bloom filters and comparing passwords.
- `rockyou.txt`: The dataset file (assumed to be present) containing passwords for testing.
- `Beta1.txt`, `Beta2.txt`, `Beta3.txt`: Generated Beta files containing Bloom filters for datasets.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

