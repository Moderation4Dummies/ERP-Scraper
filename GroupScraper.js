const axios = require("axios");
const { setTimeout } = require("timers");
const fs = require("fs").promises;
require("node:timers");

let groupId = 0;
const limit = 100;
let allUserLinks = [];
let allUserNames = [];
let UserData = []
let fullUserNames = [];
let StoredIDs = [];
let intervalID = 0;

const BlacklistedWords = ["Force"]; // Put commonly used bypassed words into here, it'll be used to filter out potentially harmful usernames/display names

const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms)); // Add a delay

async function getAllUserIds() {
  let nextPageCursor = null;

  do {
    try {
      const response = await axios.get(
        `https://groups.roblox.com/v1/groups/${groupId}/users?sortOrder=Asc&limit=${limit}${
          nextPageCursor ? `&cursor=${nextPageCursor}` : ""
        }`
      );

      const currentPageMembers = response.data.data;
      const userLinks = currentPageMembers.map(
        (member) => `https://www.roblox.com/users/${member.user.userId}/profile`
      );
      const Usernames = await currentPageMembers.map((member) => {
        allUserNames.push({
          Username: member.user.username,
          Displayname: member.user.displayName,
          UserLink: `https://www.roblox.com/users/${member.user.userId}/profile`
        });
      });

      fullUserNames = BlacklistedWords.map((word) => {
        return allUserNames.filter(
          (username) =>
            username.Username.includes(word) ||
            username.Displayname.includes(word)
        );
      }); // Filter the users by the blacklisted word provided
      currentPageMembers.map((member) => StoredIDs.push(member.user.userId));

      allUserLinks = allUserLinks.concat(userLinks);
      UserData = currentPageMembers

      nextPageCursor = response.data.nextPageCursor;
    } catch (error) {
      console.error("Error making API request:", error);
      break;
    }
  } while (nextPageCursor);

  try {
    const FilteredUserLinks = allUserLinks.filter(
      (link, index, self) => self.findIndex((l) => l === link) === index
    ); // Make sure there are no duplicates, considering this script re-runs for every 'big' group.
    const filteredUserNames = fullUserNames.filter(
      (link, index, self) => self.findIndex((l) => l === link) === index
    ); // Do the same here

    let UsernamesList = []

    fullUserNames
      .map(async (currentEntry) => {
        currentEntry.map(entry =>
            {
            UsernamesList.push(`${entry.Username}, ${entry.Displayname}, ${entry.UserLink}`)
            }
        )
      })


    await fs.writeFile(
      "user_ids.txt",
      `${FilteredUserLinks.join("\n")} \nFlagged users:\n${UsernamesList.join('\n')}`
    );
    console.log("User profile URLs written to user_ids.txt");
    return StoredIDs;
  } catch (error) {
    console.error("Error writing to file:", error);
  }
}

async function ScrapeGroups() {
  const BaseResponse = await axios.get(
    `https://groups.roblox.com/v1/groups/${groupId}`
  ); // Grab the info of the basegroup
  const BaseGroup = BaseResponse.data.name;
  const UserIDs = await getAllUserIds();
  let Groups = [];
  let GroupsIDs = [];

  let GroupCache = await fs.readFile('cache/groupscache.txt')
  let UserCache = await JSON.parse(await fs.readFile('cache/user_cache.txt', 'utf-8')) // Read caches

  await Promise.all(
    UserIDs.map(async (id) => {
      const CachedUser = await UserCache.find(user => user.user.userId == id)
      if(CachedUser) {
        return // If there is already an entry in the cache, exit
      }
      try {
        const response = await axios.get(
          `https://groups.roblox.com/v1/users/${id}/groups/roles`
        );
        if (response.ok) {
          await delay(1000); // Anti-rate limiting system
        }
        const groupIDs = response.data.data.map((group) => {
          return { Name: group.group.name, ID: group.group.id };
        });
        const groups = response.data.data.map((group) => group.group.name);

        GroupsIDs = GroupsIDs.concat(groupIDs);
        Groups = Groups.concat(groups);
      } catch (err) {
        console.log(err);
        await delay(1000); // Tries to run the code again if it experiences an error, 1 second interval
      }
    })
  );

  let MappedGroups = Groups.map((groupName) => {
    return {
      Name: groupName,
      Amount: Groups.reduce((count, currentGroup) => {
        return currentGroup === groupName ? count + 1 : count;
      }, 0),
    };
  })
    ?.filter(
      (group, index, self) =>
        self.findIndex((g) => g.Name === group.Name) === index
    )
    ?.filter(
      (group) =>
        group.Amount >
        3 /* Minimum required of appearances to be listed, change as needed*/
    )
    ?.filter(
      (group) =>
        group.Name !=
        BaseGroup /* Makes sure you don't get the basegroup (Yes, it's not efficient, but it works for now).*/
    );

  const HighestValue = MappedGroups.reduce(
    (max, current) => (current.Amount > max.Amount ? current : max),
    MappedGroups[0]
  );

  const Values = MappedGroups.map((entry) =>
    Object.entries(entry)
      .map(([key, value]) => `${key}: ${value}`)
      .join(", ")
  )?.join("\n");

  const ID = await GroupsIDs.find((group) => group.Name === HighestValue.Name);

  groupId = ID.ID; // This changes it to match the most common group (and it filters out the base group itself)
  
    // Write all the caches
    await fs.writeFile("common_groups.txt", Values);
    await fs.writeFile('cache/groupscache.txt', JSON.stringify(MappedGroups))
    await fs.writeFile('cache/user_cache.txt', JSON.stringify(UserData))

  ScrapeGroups() // Re-run the function again. It won't stop itself, you have to do so manually. (Using Node.js, that'd be Control + C)
  console.log(`Times ran: ${intervalID}`) // Tells you how many times the function has ran
  intervalID++
}

ScrapeGroups();
