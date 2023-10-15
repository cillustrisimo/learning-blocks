1. Create your project folder
2. Create your virtual environment. 'pipenv': `pip install pipenv` then `pipenv shell`
3. Install fastapi, uvicorn -> `pipenv install fastapi uvicorn`
4. Create a script: main.js
5. Setup
6. Install requests => `pipenv install requests`
7. Start the server by running `uvicorn app:app --reload` 

In main.py file:


Add 'from starlette.responses import StreamingResponse' which is used to send the css file in memory to Response.

Add 'from fastapi.middleware.cors import CORSMiddleware' to allow setting CORS 

Add 'from aries_api import aries_api' to import the class that has your functions


In def download_csv()

We create an areas object, passing the school id to it, as requested.

Then call the aries.get_current_grades_csv_io method that get response from the API and convert to CSV.


We then create iterate local function that helps the StreamingResponse loop through the in-memory csv file created.

We proceed by returning this as response, which is then used on the frontend.



In aries_api.py class:

Add 'import io'

get_current_grades_csv_io function was created to store the csv inside memory using the the io module.
## More documentation soon!!!
### Ideas
- https://youtube.com/shorts/MCzA3vFG6ag?feature=share
<img align="right" alt="GIF" src="https://i.pinimg.com/originals/e4/26/70/e426702edf874b181aced1e2fa5c6cde.gif" />