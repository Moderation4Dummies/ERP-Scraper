import requests
import concurrent.futures
import time
import json
from tqdm import tqdm

group_ids = [8923350, 11891341, 17150723]  # Replace with your desired group IDs

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
    future_to_user_id = {executor.submit(get_user_groups, user_id): user_id for user_id in all_members}
    for future in tqdm(concurrent.futures.as_completed(future_to_user_id), total=len(all_members), unit="member"):
        members_groups.append(future.result())

group_counts = count_group_ids(members_groups, exclude_group_ids=group_ids)


format_data = [{"group_url": f"https://www.roblox.com/groups/{gid}/x", "count": count} for gid, count in group_counts]
# snake_case naming convention is cursed

with open('group_counts_output.json', 'w') as outfile:
    json.dump(format_data, outfile, indent=4)

print("Processing complete. Results saved to group_counts_output.json")
