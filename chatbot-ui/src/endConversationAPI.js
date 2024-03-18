// api.js

const EndConversation={ 
    
    MakeAPIRequestOnUnload : async (conversationID) => {
    // Make the API request to your endpoint when the page is about to be unloaded
    // You can use fetch or any library to make the API call here
    // Example:
    try {
      const response = await fetch(`https://yourAPIurl.com/end_conversation?conversationID=${conversationID}`, {
        method: 'POST', // or 'GET', 'PUT', etc.
        // Add headers if needed
      });
      const data = await response.json();
      console.log('API response:', data);
    } catch (error) {
      console.error('Error making API request:', error);
    }
  }
};

export default EndConversation;