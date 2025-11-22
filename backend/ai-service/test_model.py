# backend/ai-service/test_model.py
import torch
import torch.nn as nn
import torch.optim as optim
import os

MODEL_PATH = os.environ.get("MODEL_PATH", "model.pt")  # Will save in backend/ai-service/
INPUT_SIZE = 3
OUTPUT_SIZE = 1

# Simple linear model
class SimpleModel(nn.Module):
    def __init__(self, input_size=INPUT_SIZE, output_size=OUTPUT_SIZE):
        super().__init__()
        self.linear = nn.Linear(input_size, output_size)

    def forward(self, x):
        return self.linear(x)

# Create model
model = SimpleModel()

# Dummy dataset: y = sum(x)
X = torch.randn(100, INPUT_SIZE)
y = X.sum(dim=1, keepdim=True)

# Train for a few steps
optimizer = optim.SGD(model.parameters(), lr=0.01)
loss_fn = nn.MSELoss()

for epoch in range(50):
    optimizer.zero_grad()
    y_pred = model(X)
    loss = loss_fn(y_pred, y)
    loss.backward()
    optimizer.step()

print(f"✅ Training complete. Final loss: {loss.item():.4f}")

# Save the model as state_dict
torch.save(model.state_dict(), MODEL_PATH)
print(f"✅ Model saved to {MODEL_PATH}")
