# Intellicombat RL Trainer
This project covers the needs of Teegarden-Project (a video game in Unity) regarding the training, normalization and preprocessing of combat logs from the video game using combined Reinforcement Learning (part simulated logs, part real) as well as the export and conversion to Keras and ONNX models respectively.

## Usage

- NOTE: if you want to check the features on the production environment, use the kubeconfig file and the following command to enter in the ai-training-microservice pod:

```bash
## to get the pod name:
kubectl --kubeconfig=C:\Users\Gabriel\.kube\teegarden.yaml get pods -A   
## execute bash inside the pod:
kubectl --kubeconfig=C:\Users\Gabriel\.kube\teegarden.yaml exec -it POD_NAME -n teegarden -- /bin/bash
```
### 1. Simulated logs generation
To simulate a large number of logs and avoid biases with real logs or in order to test different models and behaviors, we will access to```/intellicombat_training_logs_manager``` and run ```python3 main.py [NUMBER OF SIMULATIONS]```. We will find the simulations inside ```/intellicombat_training_logs_manager/training_simulated_logs```.

### 2. Real logs conversion
To convert real video game logs to the format suitable for RL, we must include within the folder ```/intellicombat_training_logs_manager/raw_logs``` our combat logs dataset (this part is for test purposes since our real use of this conversion will be to receive them via a REST API from the GameClient).

Later, we will run ```python3 convert_log_to_rl_format.py```. The logs converted will be stored at ```/intellicombat_training_logs_manager/training_converted_real_logs```.

### 3. Preprocessing, training and model export.
Inside ```/intellicombat_rl_trainer```, We will have the script ```trainer.sh``` that once executed with bash will take care of all the work. The model in different formats will be exported in ```/intellicombat_rl_trainer/model```.

Remember to run ```pip install -r requirements.txt``` in order to get the optimal version of each needed library.

### 4. Integration with the project elements

Go to the Teegarden API-Infra repo and follow the instructions in order to deploy the infrastructure.

Check if the API works properly using the Postman collection (you can find it in the API-Infra repo).

Don't forget to populate the database with real or simulated combat logs.

Finally, download the game client and test the game.

## More elements of the project
- [Teegarden-Project-GameClient](https://github.com/Gguardiola/Teegarden-Project-GameClient)
- [Teegarden-Project-API-Infra](https://github.com/Gguardiola/Teegarden-Project-API-Infra)