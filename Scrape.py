import requests
import concurrent.futures
import time
import os
import json

config_path = os.path.join("conf", "group_ids.json")
with open(config_path, "r") as file:
    group_ids = [int(group_id) for group_id in json.load(file)]

blacklist_path = os.path.join("conf", "blacklist.json")
with open(blacklist_path, "r") as file:
    blacklist_group_ids = set(int(group_id) for group_id in json.load(file))

group_ids = [group_id for group_id in group_ids if group_id not in blacklist_group_ids]

def get_group_members(group_id):
      user_ids = set()
      cursor = None
      while True:
          url = f"https://groups.roblox.com/v1/groups/{group_id}/users"
          params = {'limit': 100, 'cursor': cursor} if cursor else {'limit': 100}
          response = requests.get(url, params=params)
          if response.status_code == 200:
              data = response.json()
              user_ids.update(member['user']['userId'] for member in data['data'])
              cursor = data.get("nextPageCursor")
              if not cursor:
                  break
          else:
              # Handle errors or rate limiting here
              break
      return user_ids

def get_user_groups(user_id):
      group_ids = []
      try:
          response = requests.get(f"https://groups.roblox.com/v1/users/{user_id}/groups/roles")
          if response.status_code == 200:
              groups = response.json()['data']
              group_ids = [group['group']['id'] for group in groups]
      except Exception as e:
          # Handle exceptions appropriately
          pass
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
      members = get_group_members(group_id)
      all_members.update(members)
      print(f"Collected {len(members)} members from group {group_id}. Total unique members so far: {len(all_members)}")

print("Fetching groups for all aggregated members...")
start_time = time.time()

members_processed = 0
members_groups = []

with concurrent.futures.ThreadPoolExecutor() as executor:
      futures = {executor.submit(get_user_groups, user_id): user_id for user_id in all_members}
      for future in concurrent.futures.as_completed(futures):
          members_groups.append(future.result())
          members_processed += 1
          if members_processed % 100 == 0:
              elapsed_time = time.time() - start_time
              estimated_total_time = (elapsed_time / members_processed) * len(all_members)
              remaining_time = estimated_total_time - elapsed_time
              print(f"Processed {members_processed}/{len(all_members)} members. Estimated time remaining: {remaining_time:.2f} seconds.")

group_counts = count_group_ids(members_groups, exclude_group_ids=group_ids)

with open('group_counts_output.txt', 'w') as outfile:
      for gid, count in group_counts:
          outfile.write(f"https://www.roblox.com/groups/{gid}/x - {count}\n")

print("Processing complete. Results saved to group_counts_output.txt")
