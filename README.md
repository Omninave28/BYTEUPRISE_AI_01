**FAQ Chatbot for Customer Support**

## Project Description
This is an intelligent FAQ Chatbot developed for customer support, built with FastAPI as the backend and React + Vite for the frontend. The system uses intent classification, entity recognition, and decision tree logic to respond to user queries efficiently. Users can interact with the chatbot, browse categorized FAQs, and submit feedback on responses.
## Features

- **Real-time Chat Interaction**: Conversational interface to handle customer queries in real-time.
- **FAQ Categorization**: Organized FAQ categories accessible via sidebar filter.
- **User Feedback Logging**: Tracks user feedback with a "Was this helpful?" button.
- **CSV Upload**: Users can upload FAQ datasets in CSV format for dynamic updates.
- **Dark Mode**: Toggle between light and dark modes for improved user experience.
- **Frontend & Backend Integration**: A smooth interaction between FastAPI backend and React + Vite frontend.## How to Run the Code

1. Clone the repository:
<<<<<<< HEAD
```bash
git clone https://github.com/Omninave28/faq-chatbot.git
cd faq-chatbot
```
=======
   ```bash
   git clone https://github.com/Omninave28/faq-chatbot.git
   cd faq-chatbot
   ```
>>>>>>> cf2456f (Initial commit: FAQ Chatbot with FastAPI backend and React frontend)
   
2.  Set up the backend:
- Install the Python dependencies:

```bash
pip install -r requirements.txt
```
- Start the FastAPI backend:

```bash
uvicorn app.main:app --reload
```
- The backend will be running at http://127.0.0.1:8000.

3. Set up the frontend:
- Navigate to the frontend directory:

```bash
cd frontend
```

- Install Node.js dependencies:

```bash
npm install
```

- Start the React frontend:

```bash
npm run dev
```
- The frontend will be running at http://127.0.0.1:5173.

4. Open your browser and interact with the chatbot!
## Sample Output

- Chatbot interface with real-time responses.

- FAQ categories listed in the sidebar.

- User feedback prompt after each answer.
## Credits

- BYTEUPRISE for providing the guidance and resources to make this project a success.

- React, FastAPI, and Tailwind CSS for the powerful frameworks used.

- Uvicorn for serving the FastAPI application.
## License

[MIT](https://choosealicense.com/licenses/mit/)


## Authors

- [@Om Ninave](https://github.com/Omninave28)
- Intern @BYTEUPRISE
- ninaveom@gmail.com
- www.linkedin.com/in/om-ninave-b47568272

