import hashlib
import numpy as np

# Constants
BIT_ARRAY_SIZE = 1000  # Size of the bit array for the Bloom filter
NUM_HASH_FUNCTIONS = 15  # Number of hash functions to use
THRESHOLD = 0.3  # Similarity threshold based on empirical testing

# Function to create an MD5 hash value
def hash_md5(value):
    return int(hashlib.md5(value.encode()).hexdigest(), 16)

# Function to create a SHA256 hash value
def hash_sha256(value):
    return int(hashlib.sha256(value.encode()).hexdigest(), 16)

# Generate 15 hash values using MD5 and SHA256
def generate_hashes(value):
    hash_list = []
    for i in range(NUM_HASH_FUNCTIONS):
        combined = f"{value}{i}"
        hash_list.append(hash_md5(combined) % BIT_ARRAY_SIZE)
        hash_list.append(hash_sha256(combined) % BIT_ARRAY_SIZE)
    return hash_list[:NUM_HASH_FUNCTIONS]

# Create bigrams from a password
def bigrams(password):
    return [password[i:i+2] for i in range(len(password)-1)]

# Create a Bloom filter for a password using bigrams and hash functions
def create_bloom_filter(password):
    bit_array = np.zeros(BIT_ARRAY_SIZE, dtype=bool)
    for bigram in bigrams(password):
        hash_values = generate_hashes(bigram)
        for hash_val in hash_values:
            bit_array[hash_val] = True
    return bit_array

# Calculate Jaccard coefficient between two Bloom filters
def jaccard_coefficient(filter1, filter2):
    intersection = np.sum(np.logical_and(filter1, filter2))
    union = np.sum(np.logical_or(filter1, filter2))
    return intersection / union

# Read datasets from the rockyou.txt file
def read_datasets():
    with open('rockyou.txt', 'r', encoding='latin-1') as file:
        passwords = file.readlines()
    
    dataset1 = sorted([pw.strip() for pw in passwords if len(pw.strip()) == 8])[:100]
    dataset2 = sorted([pw.strip() for pw in passwords if len(pw.strip()) == 10])[:100]
    dataset3 = dataset1.copy()
    
    return dataset1, dataset2, dataset3

# Generate Beta files containing Bloom filters for each dataset
def generate_beta_files(datasets):
    for i, dataset in enumerate(datasets, 1):
        with open(f'Beta{i}.txt', 'w') as file:
            for password in dataset:
                bit_array = create_bloom_filter(password)
                bit_array_str = ''.join(['1' if bit else '0' for bit in bit_array])
                file.write(f"{password} {bit_array_str}\n")

# Given a password, produce its Bloom filter
def get_bloom_filter(password):
    return create_bloom_filter(password)

# Compare two passwords from the beta files
def compare_passwords(beta_file, password1, password2):
    with open(beta_file, 'r') as file:
        lines = file.readlines()
    
    filter1 = filter2 = None
    
    for line in lines:
        pw, bit_array_str = line.split()
        bit_array = np.array([bool(int(bit)) for bit in bit_array_str], dtype=bool)
        if pw == password1:
            filter1 = bit_array
        elif pw == password2:
            filter2 = bit_array
    
    if filter1 is not None and filter2 is not None:
        similarity = jaccard_coefficient(filter1, filter2)
        return similarity >= THRESHOLD, similarity
    return False, 0

# Test the similarity of a password and its modifications
def test_modifications(password, modifications):
    original_filter = create_bloom_filter(password)
    results = []
    for mod in modifications:
        mod_filter = create_bloom_filter(mod)
        similarity = jaccard_coefficient(original_filter, mod_filter)
        results.append((mod, similarity))
    return results

# Main function to test the implementation
def main():
    # Read and generate datasets
    datasets = read_datasets()
    generate_beta_files(datasets)
    
    # Example password and its modifications for testing
    password = "examplepassword"
    mod_passwords = ["examplepassworD", "examplepasswOrd", "examplepassWOrd"]
    
    # Print the Bloom filter of the original password
    print("Bloom filter of original password:")
    print(get_bloom_filter(password))
    
    # Compare two passwords in each Beta file
    for i in range(1, 4):
        beta_file = f'Beta{i}.txt'
        similar, similarity = compare_passwords(beta_file, "password1", "password2")
        print(f"Similarity between 'password1' and 'password2' in Beta{i}: {similar} (Jaccard: {similarity})")
    
    # Test similarity of the password with its modifications
    results = test_modifications(password, mod_passwords)
    for mod, similarity in results:
        print(f"Similarity between '{password}' and '{mod}': {similarity}")

if __name__ == "__main__":
    main()
