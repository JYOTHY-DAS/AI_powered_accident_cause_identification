import torch
import torch_directml

device = torch_directml.device()
print(f"Using device: {device}")

# Move a simple tensor to the DirectML device
x = torch.tensor([1.0, 2.0, 3.0]).to(device)
print(x)


# Set DirectML as the default backend
torch.set_default_tensor_type('torch.FloatTensor')  # This works only for float tensors
device = torch_directml.device()