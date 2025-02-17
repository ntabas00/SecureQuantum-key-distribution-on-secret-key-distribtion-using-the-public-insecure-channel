I just added to 6 bit and added a checking if Alice and Bob of same key value without interference:
import random

def generate_fixed_qubits(length=6):
    """Generate a fixed 6-bit binary string."""
    return '0' * length  # Fixed qubit string of zeros

def choose_random_bases(length=4):
    """For each bit, randomly choose a basis ('X' for rectilinear, 'Z' for diagonal)."""
    return ''.join(random.choice('XZ') for _ in range(length))

def simulate_eavesdropping(qubits):
    """Simulate the potential eavesdropping which may alter the qubits."""
    qubits_list = list(qubits)
    num_flips = random.randint(0, 3)  # Flip up to 3 bits to simulate interference
    for _ in range(num_flips):
        idx = random.randint(0, len(qubits) - 1)
        qubits_list[idx] = '1' if qubits_list[idx] == '0' else '0'
    return ''.join(qubits_list)

def send_qubits(qubits, eavesdropper):
    """Simulate sending qubits to Bob, possibly with eavesdropping."""
    if eavesdropper:
        print("Eavesdropper is present. Interfering with the qubits...")
        return simulate_eavesdropping(qubits)
    else:
        print("Sending qubits to Bob without interference.")
        return qubits

def measure_qubits(qubits, bases):
    """Simulate Bob measuring the qubits based on his bases."""
    print(f"Bob received and is measuring qubits with his bases: {bases}")
    return qubits  # In actual QKD, the measurement would depend on alignment with bases

def basis_comparision(alice_bases, bob_bases):
    """Determine indices where Alice's and Bob's bases match."""
    print(f"Alice's bases: {alice_bases}")
    print(f"Bob's bases: {bob_bases}")
    matching_indices = [i for i in range(len(alice_bases)) if alice_bases[i] == bob_bases[i]]
    print(f"Matching bases at positions: {matching_indices}")
    return matching_indices

def qkd_simulation():
    eavesdropper_input = input("Do you want an eavesdropper in the simulation? (yes/no): ").lower()
    eavesdropper = eavesdropper_input == 'yes'
    
    # Generate and encode qubits
    qubits = generate_fixed_qubits()
    print(f"Encoded qubits: {qubits}")
    alice_bases = choose_random_bases()
    bob_bases = choose_random_bases()

    # Send and measure qubits
    received_qubits = send_qubits(qubits, eavesdropper)
    measured_qubits = measure_qubits(received_qubits, bob_bases)

    # Basis comparision and key generation
    matching_indices = basis_comparision(alice_bases, bob_bases)
    key = ''.join(measured_qubits[i] for i in matching_indices if i < len(measured_qubits))
    print(f"Secret key generated (partial due to basis mismatch): {key}")

    #checking that Alice and Bob key match when no evedroping occurs
    if not eavesdropper:
        exppected_key = ''.join(qubits[i] for i in matching_indices if i < len(qubits))
        if key == exppected_key:
            print("No inteference detected. Alice and Bob have matching keys.")
        else:
            print("Keys do not match despite no interferance")
    
    return key

# Run the QKD simulation
qkd_simulation()
