import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import random
import os
import constants


class RouteplanningNN(nn.Module):
    def __init__(self, grid_size, hidden_size, output_size):
        super(RouteplanningNN, self).__init__()
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.fc1 = nn.Linear(64 * grid_size * grid_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, output_size)
        self.relu = nn.ReLU()

    def forward(self, grid_state, current_pos, target_pos):
        x = self.relu(self.conv1(grid_state))
        x = self.relu(self.conv2(x))
        x = x.view(x.size(0), -1)
        x = self.relu(self.fc1(x))
        x = self.fc2(x)
        return x

    def save(self, path):
        directory = os.path.dirname(path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        torch.save(self.state_dict(), path)
        print(f"Model saved to {path}")

    @classmethod
    def load(cls, path, grid_size, hidden_size, output_size):
        model = cls(grid_size, hidden_size, output_size)
        model.load_state_dict(torch.load(path))
        model.eval()
        print(f"Model loaded from {path}")
        return model


def create_grid_state(grid, current_pos, target_pos):
    grid_state = np.zeros((3, constants.ROWS, constants.COLS), dtype=np.float32)
    for i in range(constants.ROWS):
        for j in range(constants.COLS):
            grid_state[0, i, j] = 1 if grid[i, j].get("navigable") else 0
    grid_state[1, current_pos[0], current_pos[1]] = 1
    grid_state[2, target_pos[0], target_pos[1]] = 1
    return torch.FloatTensor(grid_state)


def create_training_data(grid, num_samples=constants.NN_TRAINING_SAMPLES):
    print("Creating training data...")
    data = []
    labels = []
    rows, cols = constants.ROWS, constants.COLS

    def get_best_move(current_pos, target_pos):
        best_moves = []
        min_distance = float('inf')
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
            nx, ny = current_pos[0] + dx, current_pos[1] + dy
            if 0 <= nx < rows and 0 <= ny < cols and grid[nx, ny].get("navigable"):
                distance = ((nx - target_pos[0]) ** 2 + (ny - target_pos[1]) ** 2) ** 0.5
                if distance < min_distance:
                    min_distance = distance
                    best_moves = [(dx, dy)]
                elif distance == min_distance:
                    best_moves.append((dx, dy))
        return random.choice(best_moves) if best_moves else (0, 0)

    for i in range(num_samples):
        if i % 1000 == 0:
            print(f"Generated {i} samples")

        current_pos = (random.randint(0, rows - 1), random.randint(0, cols - 1))
        while not grid[current_pos[0], current_pos[1]].get("navigable"):
            current_pos = (random.randint(0, rows - 1), random.randint(0, cols - 1))

        target_pos = (random.randint(0, rows - 1), random.randint(0, cols - 1))
        while not grid[target_pos[0], target_pos[1]].get("navigable") or target_pos == current_pos:
            target_pos = (random.randint(0, rows - 1), random.randint(0, cols - 1))

        grid_state = create_grid_state(grid, current_pos, target_pos)

        dx, dy = get_best_move(current_pos, target_pos)

        move = [0] * 9
        move_index = (dy + 1) * 3 + (dx + 1)
        move[move_index] = 1

        data.append(grid_state)
        labels.append(move)

    print("Training data creation completed.")
    return torch.stack(data), torch.FloatTensor(labels)


def train_network(model, train_data, train_labels, num_epochs=constants.NN_TRAINING_EPOCHS, learning_rate=0.001):
    print("Starting network training...")
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    for epoch in range(num_epochs):
        optimizer.zero_grad()
        outputs = model(train_data)
        loss = criterion(outputs, train_labels)
        loss.backward()
        optimizer.step()

        if (epoch + 1) % 50 == 0:
            print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item():.4f}')

    print("Network training completed.")
    if constants.NN_SAVE_MODEL:
        model.save(constants.NN_SAVE_PATH)


def plan_route(model, grid, boat, target, max_steps=constants.NN_MAX_STEPS, callback=None):
    print("Planning route...")
    route = []
    current_pos = (boat.x, boat.y)
    steps = 0
    visited = set()

    while current_pos != target and steps < max_steps:
        visited.add(current_pos)
        grid_state = create_grid_state(grid, current_pos, target)

        with torch.no_grad():
            output = model(grid_state.unsqueeze(0)).squeeze()

        moves = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1), (0, 0)]
        valid_moves = []
        for i, (dx, dy) in enumerate(moves):
            new_pos = (current_pos[0] + dx, current_pos[1] + dy)
            if (0 <= new_pos[0] < constants.ROWS and
                    0 <= new_pos[1] < constants.COLS and
                    grid[new_pos[0], new_pos[1]].get("navigable") and
                    new_pos not in visited):
                valid_moves.append((i, output[i].item()))

        if not valid_moves:
            print(f"No valid moves from {current_pos}, backtracking...")
            if route:
                route.pop()
                current_pos = route[-1] if route else (boat.x, boat.y)
            else:
                print("Cannot find a valid route.")
                break
        else:
            best_move = max(valid_moves, key=lambda x: x[1])
            dx, dy = moves[best_move[0]]
            new_pos = (current_pos[0] + dx, current_pos[1] + dy)
            route.append(new_pos)
            current_pos = new_pos

        steps += 1
        if callback:
            callback(current_pos, route)

        if steps % 10 == 0:
            print(f"Step {steps}: Current position {current_pos}")

    if current_pos == target:
        print("Route planning successful.")
    else:
        print(f"Route planning stopped: maximum steps ({max_steps}) reached.")

    return route