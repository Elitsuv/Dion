import discord
from discord.ext import commands
import pandas as pd
import jax.numpy as jnp
from jax import jit
from sklearn.feature_extraction.text import TfidfVectorizer
import asyncio
import os
import random

# JIT compiled function for ultra-fast vectorized cosine similarity
@jit
def get_similarities(X_matrix, user_vector):
    # Since TF-IDF vectors are L2-normalized, dot product is exactly the cosine similarity
    return jnp.dot(X_matrix, user_vector)

class Chatbot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dataset_path = r"C:\Users\jeezh\OneDrive\Desktop\dion\chatbot_dataset.csv"
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.df = None
        self.X_matrix = None
        self.is_ready = False
        
        # Load dataset asynchronously on init
        self.bot.loop.create_task(self.load_dataset())

    async def load_dataset(self):
        try:
            print("🧠 Loading Human Conversational Dataset & Jax Tensor Core...")
            # Run blocking pandas/sklearn operations in a separate thread
            self.df, self.X_matrix = await asyncio.to_thread(self._sync_load_data)
            self.is_ready = True
            print(f"✅ Jax Chatbot Engine ready. Loaded {len(self.df)} conversations.")
        except Exception as e:
            print(f"❌ Failed to load chatbot dataset: {e}")

    def _sync_load_data(self):
        if not os.path.exists(self.dataset_path):
            raise FileNotFoundError(f"Dataset not found at {self.dataset_path}")
            
        df = pd.read_csv(self.dataset_path)
        # Ensure string types
        df['pattern'] = df['pattern'].astype(str)
        df['response'] = df['response'].astype(str)
        
        # Fit TF-IDF
        X_scipy = self.vectorizer.fit_transform(df['pattern']).toarray()
        
        # Convert to Jax array
        X_matrix = jnp.array(X_scipy)
        return df, X_matrix

    async def get_best_response(self, user_text: str):
        if not self.is_ready or not user_text.strip():
            return None
            
        try:
            # Vectorize user input
            user_vec = await asyncio.to_thread(self.vectorizer.transform, [user_text.lower()])
            user_vec_arr = jnp.array(user_vec.toarray()).T  # transpose to match (features, 1)

            # Compute similarities using Jax
            similarities = get_similarities(self.X_matrix, user_vec_arr).flatten()
            
            # Find best match
            best_idx = int(jnp.argmax(similarities))
            best_score = float(similarities[best_idx])
            
            # Dynamic human threshold
            if best_score > 0.15:
                return self.df.iloc[best_idx]['response']
            else:
                fallbacks = [
                    "That's interesting! Tell me more.",
                    "I'm not quite sure I catch your drift, but I'm listening!",
                    "Could you rephrase that? I'm still getting used to human chatter.",
                    "Haha, yeah. Anyway, how's your day going?",
                    "I hear you! Anything else on your mind?"
                ]
                return random.choice(fallbacks)
                
        except Exception as e:
            print(f"Chatbot Engine Error: {e}")
            return "Oops, my systems glitched for a second!"

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        content_lower = message.content.lower()
        is_mentioned = self.bot.user.mentioned_in(message)
        starts_with_dion = content_lower.startswith("dion")
        
        clean_content = message.content
        if starts_with_dion:
            clean_content = message.content[4:].strip()
            if not clean_content:
                await message.reply("Hey! I'm Dion. What's up?")
                return

        if is_mentioned or starts_with_dion:
            if message.content.startswith(self.bot.command_prefix):
                return
                
            if not self.is_ready:
                await message.reply("Hold on a sec, my conversational database is still loading!")
                return
                
            async with message.channel.typing():
                response = await self.get_best_response(clean_content)
                if response:
                    await message.reply(response)

async def setup(bot):
    await bot.add_cog(Chatbot(bot))
