const API_URL = "http://127.0.0.1:8001/api/";

export const api = {
  async getStatus() {
    try {
      const response = await fetch(API_URL);

      if (!response.ok) {
        throw new Error(`HTTP Error: ${response.status}`);
      }

      return await response.json();

    } catch (error) {
      console.log(
        "Something went wrong:",
        error instanceof Error ? error.message : String(error),
      );

      throw error;
    }
  },
};