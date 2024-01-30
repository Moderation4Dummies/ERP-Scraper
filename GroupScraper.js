const axios = require('axios');
const fs = require('fs').promises;
/*
Author: StiizzyCat (Juulfeen_
I tested this on a 22k member roblox group and it got them all lol
*/
const groupId = 17167949;
const limit = 100;
let allUserIds = [];

async function getAllUserIds() {
  let nextPageCursor = null;

  do {
    try {
      const response = await axios.get(
        `https://groups.roblox.com/v1/groups/${groupId}/users?sortOrder=Asc&limit=${limit}${nextPageCursor ? `&cursor=${nextPageCursor}` : ''}`
      );

      const currentPageMembers = response.data.data;
      const userIds = currentPageMembers.map(member => `https://www.roblox.com/users/${member.user.userId}/profile`);
      allUserIds = allUserIds.concat(userIds);

      nextPageCursor = response.data.nextPageCursor;
    } catch (error) {
      console.error('Error making API request:', error);
      break;
    }
  } while (nextPageCursor);

  try {
    await fs.writeFile('user_ids.txt', allUserIds.join('\n'));
    console.log('User profile URLs written to user_ids.txt');
  } catch (error) {
    console.error('Error writing to file:', error);
  }
}

getAllUserIds();
