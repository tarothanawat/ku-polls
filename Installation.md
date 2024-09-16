## Installation

1. Open your terminal and enter the following commands.
   ```
   https://github.com/tarothanawat/ku-polls.git
   ```
2. Route to repository.
   ```
   cd ku-polls
   ```

3. Install virtual environment (If you haven't already.).
   ```
   pip install virtualenv
   ```
4. Create a virtual env.
   ```
   python -m venv venv
   ```
5. Activate venv.
   
   for MacOS and Linux
   ```
   source venv/bin/activate
   ```
   for Windows
   ```
   .\venv\Scripts\activate
   ```
6. Install the required packages.
   ```
   pip3 install -r requirements.txt
   ```
7. Create the .env by copying the sample.env

   for Linux or MacOS
   ```
   cp sample.env .env
   ```
   for Windows:
   ```
   copy sample.env .env
   ```
   7.1 Edit your .env SECRET_KEY by creating your own key.
   Get your key by using Django shell.
   ```
   python manage.py shell
   ```
   ```
   from django.core.management.utils import get_random_secret_key
   ```
   ```
   print(get_random_secret_key())
   ```
   Replace SECRET_KEY with your generated key in the .env file.
   ![image](https://github.com/user-attachments/assets/3058a042-155c-4c47-95f0-7b90b824fa55)

   
   
9. Migrate settings and data tables.
   ```
   python manage.py migrate
   ```
10. Load polls data.
   ```
   python manage.py loaddata data/polls-v4.json data/users.json
   ```
[See how to run the application](README.md#Running-the-Application)
