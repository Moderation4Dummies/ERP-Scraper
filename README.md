# WHAT IS THIS?
This is a python script designed to uncover violative Roblox groups and help Roblox's Trust & Safety team remove them. Roblox has a serious problem with users creating accounts for sexual purposes, commonly referred to as ERP (erotic roleplay) accounts. Many of these accounts create or hijack groups hosted on the website in order to find each other by using the members lists as directories. Most ERP accounts are in several of these violative groups.

# HOW DOES IT WORK?
This script uses Roblox's API to list out each unique member of one or more groups listed in group_ids. From here, it gathers a list of all the groups each member is in and sorts the groups by how often they appear. This technique has proven to be very effective at uncovering groups with high concentrations of ERP accounts.

# HOW DO I FIND SAMPLE GROUPS?
Finding a group to use as a sample is easy. The most effective method is to use Roblox's website to search for users with explicit usernames like "czm" until you find obvious ERP accounts. From here you can find violative groups through their profile, or the profiles of other ERP accounts in their friends lists.

To ensure the results are accurate, I recommend using groups that are created by and for ERP accounts, and not groups created by normal users that were later hijacked by them. Hijacked groups often contain a lot of innocent users that can introduce false positives into the results, like the Blade Ball development group "Wiggity" or the Flamingo Fan Group. You can confirm that a group was created for ERP accounts if the owner is an ERP account, if the roles/name/description/icon are sexual, or if the very first members of the group are ERP accounts.

# WHAT DO I DO WITH THE RESULTS?
Results are output to a json file that sorts the groups by the highest to lowest number of appearences in the sample groups. We suggest looking through the members lists of these groups to see if they're mostly being joined by ERP accounts, and reporting them using Roblox's support form if they are. https://www.roblox.com/support
