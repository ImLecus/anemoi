# anemoi
An air quality monitor

This project uses OpenAQ API to obtain worldwide air quality data. It displays as a website with an interactive map using Leaflet. There you can see real time data of the air quality of any zone in the world. It also uses a backend server written in Python and C to fetch, process and store the data from the OpenAQ API.

## Start the monitor

### Frontend
In your terminal, write:

```sh
cd frontend/anemoi
npm run dev 
```

### Backend
> [!WARNING]
> You will need to provide your own OpenAQ API key 

In your terminal, write:

```sh
cd backend
mv .env.example .env
python -v venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python anemoi-server.py
```

