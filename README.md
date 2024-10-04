# Food Ordering Chatbot

## Project Overview
The Food Ordering Chatbot is a web-based application that enables users to interact with a restaurant's menu and manage their orders efficiently. The chatbot uses Dialogflow for natural language processing and is backed by a FastAPI backend connected to a MySQL database.

## Features
- **New Order**: Initiate a new order.
- **Add Order Items**: Add items to the current order.
- **Remove Order Items**: Remove items from the current order.
- **Track Order**: Check the status of an ongoing order.
- **Confirm Order**: Finalize the order.
- **Check Menu**: View available food items.

## Technologies Used
- **Frontend**: HTML, CSS
- **Backend**: Python, FastAPI
- **Database**: MySQL
- **Natural Language Processing**: Dialogflow
- **Deployment**: Docker (optional), GitHub Actions for CI/CD

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/food-ordering-chatbot.git
   cd food-ordering-chatbot
  ```
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your MySQL database and configure the connection in `db_connection.py`.

5. Run the FastAPI application:
   ```bash
   uvicorn main:app --reload
   ```

## Key Learnings
- Gained hands-on experience with FastAPI and Dialogflow.
- Implemented CRUD operations with MySQL.
- Learned about CI/CD best practices using GitHub Actions.

## Future Developments
- Add user authentication and authorization for a personalized experience.
- Integrate payment processing to allow users to pay directly through the chatbot.
- Enhance the user interface for better user experience.
- Implement analytics to track user interactions and preferences.
