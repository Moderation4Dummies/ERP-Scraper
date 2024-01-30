<p align="center" style="margin-bottom: 0px !important;">
<img src="https://github.com/Reposits/ERP-Scraper/blob/5f1b104892f439a3b3b815becaa5ad0c513c9ffc/Images/ERP-Scraper.png" width="175" alt="ERP-Scraper Logo" align="center"/> 
</p>
<h1 align="center" style="margin-top: 0px;">ERP Scraper</h1>

<p align="center" >Effective ERP group scraping</p>

<div align="center">
  
[![Twitter](https://img.shields.io/twitter/url/https/twitter.com/modfordummies.svg?style=social&label=Follow%20%40ModForDummies)](https://twitter.com/ModForDummies)
[![Static Badge](https://img.shields.io/badge/Join%20our-Discord-5865F2?logo=discord)](https://discord.com/invite/W3ggjxpXKS)
<!--- [![Discord](https://img.shields.io/discord/1151950861312991252?logo=discord&logoColor=white&label=discord&color=4d3dff)](https://discord.com/invite/W3ggjxpXKS) --> 

</div>

This is a [Python](https://www.python.org/) script designed to uncover violative Roblox groups and help Roblox's [Trust & Safety](https://en.help.roblox.com/hc/en-us/articles/4407444339348-Safety-Civility-at-Roblox) team remove them. 

Roblox has a [serious problem](https://youtu.be/RxJvvP2erDE?si=gCO-cn-jKvgKWa-c&t=134) with users creating accounts for sexual purposes, commonly referred to as ERP (erotic roleplay) accounts. 

Many of these accounts create or hijack groups hosted on the website in order to find each other by using the members lists as directories. Most ERP accounts are in several of these violative groups.

<h2 align="center" style="margin-top: 0px;">How does it work?</h1>

This script uses Roblox's Group API to list out each unique member of one or more groups listed in group_ids. From here, it gathers a list of all the groups each member is in and sorts the groups by how often they appear. This technique has proven to be very effective at uncovering groups with high concentrations of ERP accounts.

<h2 align="center" style="margin-top: 0px;">How do I find sample groups?</h1>

Finding a group to use as a sample is easy. The most effective method is to use Roblox's website to [search](https://www.roblox.com/search/users) for users with explicit usernames like "czm" until you find obvious ERP accounts. From here you can find violative groups through their profile, or the profiles of other ERP accounts in their friends lists.

> [!CAUTION]
>To ensure the results are accurate, I recommend using groups that are created by and for ERP accounts, and not groups created by normal users that were later hijacked by them. Hijacked groups often contain a lot of innocent users that can introduce false positives into the results, like the Blade Ball development group "Wiggity" or the Flamingo Fan Group.
>
> You can confirm that a group was created for ERP accounts if the owner is an ERP account, if the roles/name/description/icon are sexual, or if the very first members of the group are ERP accounts.

<h2 align="center" style="margin-top: 0px;">What do I do with the results?</h1>

Results are output to a txt file format that sorts the groups by the highest to lowest number of appearences in the sample groups. 

> [!TIP]
> We suggest looking through the members lists of these groups to see if they're mostly being joined by ERP accounts, and reporting them using Roblox's [support form](https://www.roblox.com/support) if they are.
