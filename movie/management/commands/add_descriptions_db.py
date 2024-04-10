from django.core.management.base import BaseCommand
from movie.models import Movie
import json
import os
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

class Command(BaseCommand):
    help = 'Load movies from movie_descriptions.json into the Movie model'

    def handle(self, *args, **kwargs):
        _ = load_dotenv('openAI.env')
        client = OpenAI(
            # This is the default and can be omitted
            api_key=os.environ.get('openAI_api_key'),
        )

        def get_completion(prompt, model="gpt-3.5-turbo"):
            messages = [{"role": "user", "content": prompt}]
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0,
            )
            return response.choices[0].message.content

        instruction = "Vas a actuar como un aficionado del cine que sabe describir de forma clara, concisa y precisa \
        cualquier película en menos de 200 palabras. La descripción debe incluir el género de la película y cualquier \
        información adicional que sirva para crear un sistema de recomendación."

        movies = Movie.objects.all()

        for i in range(len(movies)):
            prompt =  f"{instruction} Has una descripción de la película {movies[i].title}"
            response = get_completion(prompt)
            movies[i].description = response
            movies[i].save()
