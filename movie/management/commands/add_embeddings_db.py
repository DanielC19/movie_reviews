from django.core.management.base import BaseCommand
from movie.models import Movie
import json
import os
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

class Command(BaseCommand):
    help = 'Modify path of images'

    def handle(self, *args, **kwargs):
        _ = load_dotenv('openAI.env')
        client = OpenAI(
            # This is the default and can be omitted
            api_key=os.environ.get('openAI_api_key'),
        )
        def get_embedding(text, model="text-embedding-3-small"):
            text = text.replace("\n", " ")
            return client.embeddings.create(input = [text], model=model).data[0].embedding

        movies = Movie.objects.all()

        for i in range(len(movies)):
            emb = get_embedding(movies[i].description)
            movies[i].emb = emb
            movies[i].save()