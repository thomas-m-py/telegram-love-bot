import uvicorn


if __name__ == "__main__":
    uvicorn.run(app="src.bot.web:app", reload=True, workers=1, port=8001)
