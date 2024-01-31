import requests
import concurrent.futures
import time
import os
import json

from datetime import datetime

cache_dir = 'cache'
user_cache_file = 'user_cache.json'
group_cache_file = 'group_cache.json'

def load_cache(cache_dir, filename):
    file_path = os.path.join(cache_dir, filename)
    try:
        with open(file_path, 'r') as file:
            return set(json.load(file))
    except FileNotFoundError:
        return set()

def save_cache(cache_dir, filename, cache_set):
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    file_path = os.path.join(cache_dir, filename)
    with open(file_path, 'w') as file:
        json.dump(list(cache_set), file)

processed_users = load_cache(cache_dir, user_cache_file)
processed_groups = load_cache(cache_dir, group_cache_file)

group_ids = [8923350, 11891341, 17150723]  # Replace with your desired group IDs

def get_group_members(group_id, processed_users, cache_dir, user_cache_file):
      user_ids = set()
      cursor = None
      while True:
          url = f"https://groups.roblox.com/v1/groups/{group_id}/users"
          params = {'limit': 100, 'cursor': cursor} if cursor else {'limit': 100}
          response = requests.get(url, params=params)
          if response.status_code == 200:
              data = response.json()
              new_users = [member['user']['userId'] for member in data['data'] if member['user']['userId'] not in processed_users]
              user_ids.update(new_users)
              cursor = data.get("nextPageCursor")
              if not cursor:
                  break
          else:
              # Handle errors or rate limiting here
              break
      processed_users.update(user_ids)
      save_cache(cache_dir, user_cache_file, processed_users)
      return user_ids

def get_user_groups(user_id, processed_users, cache_dir, user_cache_file):
      if user_id in processed_users:
          return []
      group_ids = []
      try:
          response = requests.get(f"https://groups.roblox.com/v1/users/{user_id}/groups/roles")
          if response.status_code == 200:
              groups = response.json()['data']
              group_ids = [group['group']['id'] for group in groups]
      except Exception as e:
          # Handle exceptions appropriately
          pass
      processed_users.add(user_id)
      save_cache(cache_dir, user_cache_file, processed_users)
      return group_ids

def count_group_ids(members_groups, exclude_group_ids):
      group_count = {}
      for groups in members_groups:
          for gid in groups:
              if gid not in exclude_group_ids:
                  group_count[gid] = group_count.get(gid, 0) + 1
      return sorted(group_count.items(), key=lambda x: x[1], reverse=True)

all_members = set()
for group_id in group_ids:
      print(f"Collecting members from group {group_id}...")
      members = get_group_members(group_id, processed_groups, cache_dir, group_cache_file)
      all_members.update(members)
      print(f"Collected {len(members)} members from group {group_id}. Total unique members so far: {len(all_members)}")

print("Fetching groups for all aggregated members...")
start_time = time.time()

members_processed = 0
members_groups = []

with concurrent.futures.ThreadPoolExecutor() as executor:
      futures = {executor.submit(get_user_groups, user_id, processed_users, cache_dir, user_cache_file): user_id for user_id in all_members}
      for future in concurrent.futures.as_completed(futures):
          members_groups.append(future.result())
          members_processed += 1
          if members_processed % 100 == 0:
              elapsed_time = time.time() - start_time
              estimated_total_time = (elapsed_time / members_processed) * len(all_members)
              remaining_time = estimated_total_time - elapsed_time
              print(f"Processed {members_processed}/{len(all_members)} members. Estimated time remaining: {remaining_time:.2f} seconds.")

group_counts = count_group_ids(members_groups, exclude_group_ids=group_ids)

outputs_dir = 'outputs'
if not os.path.exists(outputs_dir):
      os.makedirs(outputs_dir)

current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
filename = f"group_counts_output_{current_time}.txt"
file_path = os.path.join(outputs_dir, filename)

with open(file_path, 'w') as outfile:
      for gid, count in group_counts:
          outfile.write(f"https://www.roblox.com/groups/{gid}/x - {count}\n")

print(f"Processing complete. Results saved to {file_path}")
