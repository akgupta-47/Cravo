# Step 1: Create a new index
from database import ES

index_settings = {
    "settings": {
        "analysis": {
            "analyzer": {
                "ngram_analyzer": {  # Custom analyzer name
                    "tokenizer": "ngram_tokenizer",
                    "filter": ["lowercase"],  # Optional: make searches case-insensitive
                }
            },
            "tokenizer": {
                "ngram_tokenizer": {
                    "type": "ngram",
                    "min_gram": 3,  # Minimum character length for tokens (e.g., "cho")
                    "max_gram": 10,  # Maximum character length (e.g., "choco cru")
                    "token_chars": ["letter", "digit"],  # Split on letters/numbers only
                }
            },
        }
    },
    "mappings": {
        "properties": {
            "name": {
                "type": "text",
                "analyzer": "ngram_analyzer",  # Use ngram for indexing
                "search_analyzer": "standard",  # Use standard for querying (optional)
            },
            "description": {"type": "text", "analyzer": "ngram_analyzer"},
        }
    },
}

ES.indices.create(index="products_ngram", body=index_settings)

# Step 2: Reindex data
ES.reindex(body={"source": {"index": "products"}, "dest": {"index": "products_ngram"}})

# Step 3: Swap aliases (optional but recommended)
ES.indices.put_alias(index="products_ngram", name="products")
ES.indices.delete(index="products")  # Delete the old index
