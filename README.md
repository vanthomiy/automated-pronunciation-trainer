# Automated Pronunciation Trainer
This repository contains an automated pronunciation trainer, developed by vanthomiy. The trainer is designed to help users improve their pronunciation skills through a combination of Blazor UI for user interaction, Flask backend for calculating WER and user scores, and Whisper Speech to Text from Open AI.

## Features
The automated pronunciation trainer offers the following features:

- Blazor UI for user interaction
- Flask backend for calculating WER and user scores
- Whisper Speech to Text from Open AI
- Handles different users
- Dynamically increases the level (A1, A2, B1, B2, C1, C2) to pronounce
- Built with MudBlazor library
- Choose between different whisper models
- Add noise to the recording to make it harder
Requirements
## To use the automated pronunciation trainer, you will need the following:
- Blazor
- Flask
- Getting Started
## To get started with the automated pronunciation trainer project, follow these steps:

1. Clone the repository to your local machine.
2. Install the required dependencies for the Flask backend. You can do this by running the following command in the terminal from the root directory of the project:

  ```
  pip install -r requirements.txt
  ```

3. Run the Flask backend. To do this, navigate to the backend folder in the terminal and run the following command:

  ```
  python app.py
  ```
4. Install the required dependencies for the Blazor UI. You can do this by running the following command in the terminal from the root directory of the project:
  ```
  dotnet restore
  ```
5. Run the Blazor UI. To do this, navigate to the frontend folder in the terminal and run the following command:
  ```
  dotnet run
  ```
6. Access the trainer in your web browser by navigating to http://localhost:5000.

These steps should get you up and running with the automated pronunciation trainer project. If you run into any issues or errors, refer to the documentation or raise an issue in the project's repository.

![Blazor UI](https://github.com/vanthomiy/automated-pronunciation-trainer/blob/main/documentation/app-screenshot-1.png)

## Possible Improvements
There are several ways in which the automated pronunciation trainer project could be improved:

- Generating texts on the fly: The current version of the trainer relies on a pre-existing set of texts for users to practice their pronunciation. Adding functionality to generate new texts on the fly, based on user preferences or other parameters, would enhance the user experience and keep them engaged.

- Using a real database: The current version of the trainer does not use a real database, which may limit its scalability and performance. Implementing a real database solution, such as PostgreSQL or MongoDB, would provide a more robust and efficient system.

- Increase/Decrease noise: The trainer currently offers the ability to add noise to the recording to make it harder, but it doesn't allow for the ability to increase or decrease the noise. Adding this functionality would provide more flexibility for users and allow them to tailor their experience to their skill level.

- Adding Single Sign-On (SSO) for authentication is another potential improvement for the automated pronunciation trainer project. SSO allows users to authenticate themselves to multiple applications and systems with a single set of credentials.

Overall, these improvements would enhance the usability and functionality of the automated pronunciation trainer and provide a more comprehensive and engaging learning experience for users.

## Contributing
- Contributions to this project are welcome. If you would like to contribute, please follow these steps:

- Fork the repository.
- Create a new branch for your changes.
- Make your changes and test them thoroughly.
- Submit a pull request with a detailed description of your changes.
## Credits
The automated pronunciation trainer was developed by vanthomiy. It was built using the MudBlazor library, Flask, and Whisper Speech to Text from Open AI.

License
This project is licensed under the MIT License. See the LICENSE file for more information.
