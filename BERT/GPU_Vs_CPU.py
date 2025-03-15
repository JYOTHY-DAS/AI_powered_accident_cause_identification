import torch
import torch_directml
import time

device = torch_directml.device()
print(f"Using device: {device}")

# Create a large tensor
x = torch.randn(10000, 10000)

# CPU Computation
start = time.time()
y_cpu = x @ x  # Matrix multiplication on CPU
end = time.time()
print(f"CPU Time: {end - start:.4f} seconds")

# GPU Computation
x = x.to(device)
start = time.time()
y_gpu = x @ x  # Matrix multiplication on GPU
end = time.time()
print(f"GPU Time: {end - start:.4f} seconds")
