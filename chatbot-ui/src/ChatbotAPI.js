const API = {
   GetChatbotResponse: async (message, conversationID) => {
    try {
      const apiUrl = `https://yourAPIurl.com?conversationID=${encodeURIComponent(conversationID)}&question=${encodeURIComponent(message)}`;
      
      // Make a GET request to the API
      const response = await fetch(apiUrl);

      if (!response.ok) {
        throw new Error(`Error fetching data from the API: ${response.statusText}`);
      }

      // Parse the JSON response
      const data = await response.json();

      return data.results; // Assuming the response object has a "results" property
    } catch (error) {
      throw error;
    }
  }
};

export default API;
