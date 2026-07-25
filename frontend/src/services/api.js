
const API_BASE_URL = "http://127.0.0.1:8000/api";

export const sendChatQuery = async (query, threadId = null, clarification = null) => { 
    const payload = {
        query: query,
        thread_id: threadId,
        human_clarification_response: clarification
    };

    try {
        const response = await fetch(`${API_BASE_URL}/chat`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(payload),
        });
 
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `Server Error: ${response.status} ${response.statusText}`);
        }

        return await response.json();
    } catch (error) {
        console.error("API Error in sendChatQuery:", error);
        throw error;  
    }
};