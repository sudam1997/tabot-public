# Use the official Python 3.10 image as the base image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy your application code to the container
COPY . /app

# Install your Python packages
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt
# RUN python -m pip install openai==0.28.1
# RUN python -m pip install pymongo==4.5.0
# RUN python -m pip install python-dotenv==1.0.0
# RUN python -m pip install redis==5.0.1

# Define the command to run your application
CMD ["python","-m", "remove_idleConversations.py"]

# sudo docker build --network host -t remove-conversation-python:ucsc .