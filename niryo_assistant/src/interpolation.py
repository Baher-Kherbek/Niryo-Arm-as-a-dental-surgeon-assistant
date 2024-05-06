def linear_interpolation(yaw_data, x_data, y_data, yaw_new):

  # Check if data lengths are equal
  if len(x_data) != len(y_data) or len(x_data) != len(yaw_data):
    raise ValueError("Lengths of x_data, y_data, and yaw_data must be equal")

  # Find indices of the two yaw values between which the new yaw falls
  yaw_data = sorted(yaw_data)  # Ensure data is sorted for easier indexing
  try:
    i = yaw_data.index(yaw_new)
    return x_data[i], y_data[i]  # Exact match, return existing values
  except ValueError:
    if yaw_new < yaw_data[0] or yaw_new > yaw_data[-1]:
      print(f"Warning: new_yaw ({yaw_new}) is outside the data range.")
      return None, None  # Outside data range, return None

    # Find the indices of the surrounding yaw values
    i = next(j for j, yaw in enumerate(yaw_data) if yaw > yaw_new) - 1
    i_next = min(i + 1, len(yaw_data) - 1)

  # Perform linear interpolation for x and y
  x1, x2 = x_data[i], x_data[i_next]
  y1, y2 = y_data[i], y_data[i_next]
  yaw_new_rel = (yaw_new - yaw_data[i]) / (yaw_data[i_next] - yaw_data[i])
  estimated_x = x1 + (x2 - x1) * yaw_new_rel
  estimated_y = y1 + (y2 - y1) * yaw_new_rel

  return estimated_x, estimated_y


