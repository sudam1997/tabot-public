const API_initiate = {
    InitiateSession: async () => {
      try {
        const apiUrl = " uyour "; // Correct API endpoint
        const response = await fetch(apiUrl);
  
        if (!response.ok) {
          throw new Error(`Error fetching data from the API: ${response.statusText}`);
        }
  
        const data = await response.json();
        return data; // You can return the entire response data object
      } catch (error) {
        throw error;
      }
    },
  
    // Other API functions, if you have any
  };
  
  export default API_initiate;
  