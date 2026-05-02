import time

user_requests = {}

WINDOW = 60

def get_user_limit(plan):
  if plan == "pro":
    return 100
  return 10

def check_rate_limit(user_id, plan):
  LIMIT = get_user_limit(plan)
  now = time.time()

  if user_id not in user_requests:
    user_requests[user_id] = []

  # Remove old requests
  user_requests[user_id] = [
    t for t in user_requests[user_id] if now - t < WINDOW
  ]


  if len(user_requests[user_id]) >= LIMIT:
    return False
  
  user_requests[user_id].append(now)
  return True