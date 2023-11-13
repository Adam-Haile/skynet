# SkyNet - Language Models for Games
### DevArtech (Adam Haile)

[Rules for Skyjo](https://www.geekyhobbies.com/how-to-play-skyjo-card-game-rules-and-instructions/)
Breakdown and rules can also be found in [main.ipynb](https://github.com/DevArtech/skynet/blob/main/main.ipynb)
![Screenshot of Game](/SkyjoGameScreenshot.png)
The goal of SkyNet is to make a language model which can take the game state as a string, as well as the desired action, and return a value which can be parsed into the action taken by the neural network for the game. The model will be trained by recording game states from a wide variety of games played by premade algorithms, and then finetuned by human playing to further improve the model's ability to play.
